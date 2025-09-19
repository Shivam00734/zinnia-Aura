import base64
import json
import requests
from robot.api.deco import library, keyword
from resources.utilities.ExcelUtilities import ExcelUtilities
from resources.utilities.FileUtils import FileUtils
from resources.utilities.ReadConfig import ReadConfig


@library
class LifeCadApi:
    excelSheet = ExcelUtilities()
    read_config = ReadConfig()
    file = FileUtils()

    @keyword
    def update_contract_status_from_lifecad(self, username, password, company_hierarchy_id, contract_number):
        url = self.read_config.getValueByKey('lifecad_contract_status_updated_api')
        company_hierarchy_id = str(company_hierarchy_id)
        contract_number = str(contract_number)
        int_company_hierarchy_id = int(company_hierarchy_id)
        credentials = f"{username}:{password}".encode("utf-8")
        b64_credentials = base64.b64encode(credentials).decode("utf-8")
        print(b64_credentials)

        payload = {
            "requestHeader": {
                "externalId": "A",
                "externalUserId": username,
                "externalSystemId": "C",
                "externalUserCompHrchyId": company_hierarchy_id
            },
            "policyCommon": {
                "contractNumber": contract_number,
                "companyId": int_company_hierarchy_id
            },
            "targetStatusCode": "W"
        }

        json_payload = json.dumps(payload)

        headers = {
            "Authorization": f"Basic {b64_credentials}",
            "Content-Type": "application/json",
        }

        try:
            response = requests.post(url, headers=headers, data=json_payload)

            if response.status_code == 200:
                print("API call successful.")
                print("Response:", response.json())
                response_data = response.json()
                if response_data.get("status", {}).get("statusCode") == "Success":
                    status_message = response_data["status"]["statusMessage"]
                    old_status_code = response_data["oldStatusCode"]
                    new_status_code = response_data["newStatusCode"]

                    result = {
                        "statusMessage": status_message,
                        "oldStatusCode": old_status_code,
                        "newStatusCode": new_status_code
                    }
                    return result
                else:
                    raise ValueError("Note ID not found in the response.")

            elif response.status_code == 400:
                print("POST request failed with status code 400.")
                print("Response:", response.text)
                raise ValueError(f"Bad Request (400): {response.text}")

            else:
                print(f"POST request failed. Status code: {response.status_code}")
                print("Response:", response.text)
                raise RuntimeError(f"Request failed with status {response.status_code}: {response.text}")

        except requests.exceptions.RequestException as e:
            print("Error sending POST request:", e)
            raise RuntimeError(f"Request error: {e}")