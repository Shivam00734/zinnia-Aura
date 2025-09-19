import json

class TestDataLib:

    def load_json_data(self, file_path):
        with open(file_path, 'r') as f:
            return json.load(f)

    def get_user_by_index(self, data, index):
        return data["users"][index]