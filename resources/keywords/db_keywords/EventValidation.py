import pymongo
import os
from dotenv import load_dotenv
from robot.libraries.BuiltIn import BuiltIn
from robot.api.deco import library, keyword

load_dotenv()
MONGO_URI = os.getenv("MONGO_URI")

@library
class EventValidation:

    @keyword
    def get_event_id_from_case_detail_api(self, response_data, event_name):
        for event in response_data.get('events', []):
            if event.get('eventName') == event_name:
                return event.get('id')
        return None

    @keyword
    def get_event_name_by_event_id_from_database(self, database_name, collection_name, event_id):
        try:
            client = pymongo.MongoClient(MONGO_URI)
            db = client[database_name]
            collection = db[collection_name]

            document = collection.find_one({"_id": event_id})
            for key in document:
                if key == 'type':
                    return document['type']

        except Exception as e:
            print("Error:", e)
            return None
        finally:
            client.close()



    @keyword
    def validate_event_name_from_db(self, response_data, event_name):
        event_id_from_case_detail_api = self.get_event_id_from_case_detail_api(response_data, event_name)

        assert event_id_from_case_detail_api is not None, f"Event ID for event name '{event_name}' not found in the API response."

        event_name_from_database = self.get_event_name_by_event_id_from_database("otp_fdb", "event_store",
                                                                            event_id_from_case_detail_api)

        assert event_name_from_database is not None, f"Event name for event ID '{event_id_from_case_detail_api}' not found in the database."

        assert event_name == event_name_from_database, f"Assertion failed! Event name '{event_name}' does not match database event name '{event_name_from_database}'."

        BuiltIn().log_to_console(f"Event name '{event_name}' matches database event name '{event_name_from_database}'.")








