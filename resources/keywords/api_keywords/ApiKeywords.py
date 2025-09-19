import ast
import base64
import json
import re
import time
import requests
from robot.api.deco import library, keyword
from robot.libraries.BuiltIn import BuiltIn

from resources.utilities.ExcelUtilities import ExcelUtilities
from resources.utilities.FileUtils import FileUtils
from resources.utilities.ReadConfig import ReadConfig


@library
class ApiKeywords:
    read_config = ReadConfig()
    file = FileUtils()
    excelSheet = ExcelUtilities()

    def __init__(self):
        self.selLib = BuiltIn().get_library_instance("SeleniumLibrary")

    @keyword
    def get_policy_status_code(self, company_hierarchy_id, contract_number):
        data = self.get_LifeCadPolicyInfo_response(company_hierarchy_id, contract_number)
        if 'value' in data and len(data['value']) > 0:
            policy_status_code = data['value'][0].get('PolicyStatusCode')
            return policy_status_code

    @keyword
    def get_company_hierarchy_id(self, test_id):
        excel_file_path = self.excelSheet.getExcelSheetPath()
        expected_company_hierarchy_id = self.excelSheet.get_value_from_excel_by_column_name(excel_file_path,
                                                                                            "Input_data", test_id,
                                                                                            "company_hierarchy_id")

        # expected_company_hierarchy_id = self.excelSheet.getValueFromExcel(excel_file_path, 0, test_id, 13)
        return expected_company_hierarchy_id

    @keyword
    def convert_lifecad_api_status_to_ui_status(self, status_from_api):
        if status_from_api == "-":
            return "App Entry".lower()
        elif status_from_api == "K":
            return "Pnd-Await Funds".lower()
        elif status_from_api == "E":
            return "Pending Issue".lower()
        elif status_from_api == "A":
            return "Active".lower()
        else:
            raise ValueError('Policy status not found in response.')

    @keyword
    def get_expected_policy_status_code(self, test_id):
        excel_file_path = self.excelSheet.getExcelSheetPath()
        expected_lifecad_policy_status = self.excelSheet.get_value_from_excel_by_column_name(excel_file_path,
                                                                                             "Input_data", test_id,
                                                                                             "lifecad_policy_status")

        # expected_lifecad_policy_status = self.excelSheet.getValueFromExcel(excel_file_path, 0, test_id, 12)
        return expected_lifecad_policy_status.lower()

    @keyword
    def get_actual_policy_status_code(self, company_hierarchy_id, contract_number):
        try:
            actual_status = self.get_policy_status_code(company_hierarchy_id, contract_number)
            assert actual_status is not None, "API failed: policy status is None"
            actual_status = actual_status.lower()
            status_mapping = {
                "-": "app entry",
                "k": "pnd_await funds",
                "e": "pending issue",
                "a": "active"
            }
            return status_mapping.get(actual_status, "error: unknown policy status")
        except AssertionError as e:
            return "error: policy status unavailable"

    @keyword
    def get_LifeCadPolicyInfo_API(self, company_hierarchy_id, contract_number):
        url = self.read_config.getValueByKey('LifeCadPolicyValidatorApiUrl')
        auth = self.read_config.getValueByKey('LifeCadAuthorization')
        params = {
            '$format': 'json',
            '$filter': f"(CompanyHierarchyId eq {company_hierarchy_id}) and ContractNumber eq '{contract_number}'"
        }
        headers = {
            'Authorization': f"{auth}"
        }
        response = requests.get(url, params=params, headers=headers)
        return response

    @keyword
    def get_LifeCadPolicyInfo_response(self, company_hierarchy_id, contract_number):
        response = self.get_LifeCadPolicyInfo_API(company_hierarchy_id, contract_number)
        assert response.status_code == 200, f"Expected Status code 200, but found {response.status_code}"
        return response.json()

    @keyword
    def update_contract_status_from_lifecad(self, username, password, company_hierarchy_id, contract_number):
        url = self.read_config.getValueByKey('LifecadContractStatusUpdateAPI')
        company_hierarchy_id = str(company_hierarchy_id)
        contract_number = str(contract_number)
        int_company_hierarchy_id = int(company_hierarchy_id)
        credentials = f"{username}:{password}".encode("utf-8")
        b64_credentials = base64.b64encode(credentials).decode("utf-8")

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
                raise ValueError(f"Bad Request (400): {response.text}")

            else:
                print(f"POST request failed. Status code: {response.status_code}")
                raise RuntimeError(f"Request failed with status {response.status_code}: {response.text}")

        except requests.exceptions.RequestException as e:
            raise RuntimeError(f"Request error: {e}")

    @keyword
    def get_client_code(self, testcaseId):
        excel_file_path = self.excelSheet.getExcelSheetPath()
        client_code = self.excelSheet.get_value_from_excel_by_column_name(excel_file_path, "output_data", testcaseId,
                                                                          "${client_code}")

        # client_code = self.excelSheet.getValueFromExcel(excel_file_path, 0, testcaseId, 5)
        client_code = client_code.upper()
        return client_code

    @keyword
    def authenticate_user(self, url, audience, grant_type, client_id, client_secret):
        headers = {
            'Content-Type': 'application/x-www-form-urlencoded'
        }
        payload = {
            'audience': audience,
            'grant_type': grant_type,
            'client_id': client_id,
            'client_secret': client_secret
        }
        response = requests.post(url, headers=headers, data=payload)
        response_data = response.json()
        if 'access_token' in response_data:
            return response_data['access_token']
        else:
            raise ValueError('Token not found in response.')

    @keyword
    def case_detail_api_response(self, url, token):
        headers = {
            'Accept': 'application/json',
            'Authorization': f'Bearer {token}'
        }

        try:
            response = requests.get(url, headers=headers)

            if response.status_code == 200:
                return response.json()
            else:
                print("API call failed. Status code:", response.status_code)
                return response.text
        except Exception as e:
            print("Error making API call:", e)

    @keyword
    def case_management_api_response(self, url, token, contract_no):
        headers = {
            'Content-Type': 'application/json',
            'Authorization': f'Bearer {token}'
        }
        payload = {
            "policyNumber": f"{contract_no}"
        }
        response = requests.post(url, headers=headers, data=json.dumps(payload))
        response_data = response.json()
        return response_data

    @keyword
    def create_url(self, baseurl, endpoint, caseId=None):
        if caseId is None:
            url = self.read_config.getValueByKey(baseurl) + self.read_config.getValueByKey(endpoint)
        else:
            url = self.read_config.getValueByKey(baseurl) + self.read_config.getValueByKey(
                endpoint) + caseId
        return url

    @keyword
    def convert_dict_to_json(self, input_dict):
        return json.dumps(input_dict)

    @keyword
    def get_stage_status(self, response, category_id):
        category_id = category_id.strip()
        for item in response['stages']:
            if item['id'] == category_id:
                return item['stageStatus']

    @keyword
    def lifecad_event_received_case_detail_api(self, response_data, specific_event):

        filtered_events = [event for event in response_data["events"] if event["eventName"] == specific_event]
        event_count = len(filtered_events)

        if filtered_events:
            for event in filtered_events:
                BuiltIn().log_to_console(
                    f"ID: {event['id']}, Source: {event['source']}, Event Name: {event['eventName']}")
            BuiltIn().log_to_console(f"\nThe event '{specific_event}' appears {event_count} times.")
        else:
            BuiltIn().log_to_console(f"\nNo events found with the name '{specific_event}'.")

    @keyword
    def get_case_overview_status(self, response):
        return response['caseStatus']

    @keyword
    def get_id_from_response(self, response):
        for item in response['data']:
            return item['id']

    @keyword
    def get_case_id_from_response(self, response):
        for key in response['data']:
            for item in key['identifiers']:
                if item['identifier'] == "caseID":
                    return item['value']

    @keyword
    def get_zlcase_id_from_case_management_response(self, response):
        for key in response['data']:
            for item in key['identifiers']:
                if item['identifier'] == "zlCaseId":
                    return item['value']

    @keyword
    def get_case_id_from_response_service_from_request(self, response):
        for key in response['data']:
            for item in key['identifiers']:
                if item['identifier'] == "zlCaseId":
                    return item['value']

    @keyword
    def get_step_stage_status(self, response, stage, category_id):
        for item in response['stages']:
            if item['id'] == stage:
                for step in item['steps']:
                    if step['id'] == category_id:
                        return step['stepStatus']

    @keyword
    def get_contract_number(self, testcaseId):
        excel_file_path = self.excelSheet.getExcelSheetPath()
        contract_no = self.excelSheet.get_value_from_excel_by_column_name(
            excel_file_path, "output_data", testcaseId, "${contract_number}"
        )

        assert contract_no, f"Contract number not found for test case ID: '{testcaseId}'"

        return contract_no

    @keyword
    def extract_ids(self, response, stage_id):
        ids = []
        for item in response['stages']:
            if item["id"] == stage_id:
                for step in item["steps"]:
                    ids.append(step["id"])
        return ids

    @keyword
    def print_step_validation(self, response, stage_id, expected_step_status):
        if isinstance(expected_step_status, str):
            try:
                expected_step_status = ast.literal_eval(expected_step_status)
            except Exception as e:
                raise ValueError(f"Expected step status is not a valid dictionary string: {e}")

        step_id_list = self.extract_ids(response, stage_id)

        for step_id in step_id_list:
            if step_id in expected_step_status:
                actual_value = self.get_step_stage_status(response, stage_id, step_id)
                expected_value = expected_step_status[step_id]

                if actual_value == expected_value:
                    message = (
                        f"✅ Step status match! Expected: '{step_id}' : '{expected_value}', "
                        f"Actual: '{step_id}' : '{actual_value}'"
                    )
                else:
                    message = (
                        f"❌ Step status mismatch! Expected: '{step_id}' : '{expected_value}', "
                        f"Actual: '{step_id}' : '{actual_value}'"
                    )
            else:
                message = f"⚠️ No expected status found for step '{step_id}'"

            BuiltIn().log(message)
            BuiltIn().log_to_console(message)

    @keyword
    def check_step_validation(self, response, stage_id, expected_step_status):
        import json
        import ast
        from robot.libraries.BuiltIn import BuiltIn

        error = False

        if isinstance(response, str):
            try:
                response = json.loads(response)
            except json.JSONDecodeError:
                raise ValueError("Response is not valid JSON")

        if isinstance(expected_step_status, str):
            try:
                expected_step_status = ast.literal_eval(expected_step_status)
            except Exception as e:
                raise ValueError(f"Expected step status is not a valid dictionary string: {e}")

        step_id_list = self.extract_ids(response, stage_id)

        for step_id in step_id_list:
            if step_id in expected_step_status:
                actual_value = self.get_step_stage_status(response, stage_id, step_id)
                expected_value = expected_step_status[step_id]

                # Check if expected value is a list or a single value
                if isinstance(expected_value, list):
                    if actual_value not in expected_value:
                        error = True
                        BuiltIn().log(
                            f"Step status mismatch! Expected one of: {expected_value}, Actual: '{actual_value}' for Step: '{step_id}'")
                        BuiltIn().log_to_console(
                            f"Step status mismatch! Expected one of: {expected_value}, Actual: '{actual_value}' for Step: '{step_id}'")
                else:
                    if actual_value != expected_value:
                        error = True
                        BuiltIn().log(
                            f"Step status mismatch! Expected: '{expected_value}', Actual: '{actual_value}' for Step: '{step_id}'")
                        BuiltIn().log_to_console(
                            f"Step status mismatch! Expected: '{expected_value}', Actual: '{actual_value}' for Step: '{step_id}'")

        if error:
            raise AssertionError("One or more step statuses did not match expected values.")

    @keyword
    def get_nigo_id(self, response_data):
        nigo_id = response_data.get("exceptions", [{}])[0].get("id", None)
        return nigo_id

    @keyword
    def create_notes_from_onbase(self, lob, description, comment, taskOrCaseId,
                                 nigoId):  # lob, description, comment, taskOrCaseId, nigoId
        url = 'https://onbaseintegrationmanagerqa.se2.com:443/api/OnBase/CreateNote'

        lob_lowercase = lob.lower()
        taskOrCaseId = int(taskOrCaseId)
        nigoId = int(nigoId)

        payload = {
            "notes": [
                {
                    "lob": lob_lowercase,
                    "description": description,
                    "comment": comment,
                    "taskOrCaseId": taskOrCaseId,
                    "nigoId": nigoId
                }
            ]
        }

        json_payload = json.dumps(payload)

        content_length = str(len(json_payload))

        headers = {
            'Content-Length': content_length,
            'Host': '10.204.30.105:80',
            'Content-Type': 'application/json',
            'Accept': 'application/json'
        }

        try:
            response = requests.post(url, headers=headers, data=json_payload)

            if response.status_code == 200:
                response_data = response.json()

                if "notes" in response_data and response_data["notes"]:
                    note_id = response_data["notes"][0].get("noteId")
                    return note_id
                else:
                    raise ValueError("Note ID not found in the response.")

            elif response.status_code == 400:
                BuiltIn().log("POST request failed with status code 400.")
                raise ValueError(f"Bad Request (400): {response.text}")

            else:
                print(f"POST request failed. Status code: {response.status_code}")
                raise RuntimeError(f"Request failed with status {response.status_code}: {response.text}")

        except requests.exceptions.RequestException as e:
            raise RuntimeError(f"Request error: {e}")

    @keyword
    def create_nigo(self, url, caseId, lob, dtg, category, reason, detailedReason):

        caseId = int(caseId)

        print(url, caseId, lob, dtg, category, reason, detailedReason)
        payload = {
            "lob": lob,
            "caseID": caseId,
            "dtg": dtg,
            "category": category,
            "reason": reason,
            "detailedReason": detailedReason
        }

        json_payload = json.dumps(payload)

        content_length = str(len(json_payload))

        headers = {
            'Content-Length': content_length,
            'Host': '10.204.30.105:80',
            'Content-Type': 'application/json',
            'Accept': 'application/json'
        }

        try:
            response = requests.post(url, headers=headers, data=json_payload)

            if response.status_code == 200:
                response_data = response.json()
                if 'nigoId' in response_data:
                    return response_data['nigoId']

            elif response.status_code == 400:
                print("POST request failed with status code 400.")
                raise ValueError(f"Bad Request (400): {response.text}")

            else:
                BuiltIn().log(f"POST request failed. Status code: {response.status_code}")
                raise RuntimeError(f"Request failed with status {response.status_code}: {response.text}")

        except requests.exceptions.RequestException as e:
            raise RuntimeError(f"Request error: {e}")

    @keyword
    def update_nigo(self, url, lob, nigoId, nigoStatus, resolution):
        nigoId = int(nigoId)
        payload = {
            "lob": lob,
            "nigoId": nigoId,
            "nigoStatus": nigoStatus,
            "resolution": resolution
        }

        json_payload = json.dumps(payload)

        content_length = str(len(json_payload))

        headers = {
            'Content-Length': content_length,
            'Host': '10.204.30.105:80',
            'Content-Type': 'application/json',
            'Accept': 'application/json'
        }

        try:

            response = requests.post(url, headers=headers, data=json_payload)

            if response.status_code == 200:
                BuiltIn().log(f"POST request successful.")

            else:
                BuiltIn().log(f"POST request failed. Status code: {response.status_code}")

        except requests.exceptions.RequestException as e:
            print("Error sending POST request:", e)

    @keyword
    def fetch_task_id_from_case_detail_response(self, response_data):
        task_id = next(
            (task["id"] for task in response_data["tasks"] if task["taskType"] == "NB Application Validation"), None)
        return task_id

    @keyword
    def get_new_exception_category_reason_and_detailed_reason(self, response):
        list_of_exceptions = []
        for item in response["exceptions"]:
            if item['status'] == 'NEW':
                status = item["status"]
                category = item["category"]
                reason = item["reason"]
                detailedReason = item["detailedReason"]
                exception_dict = {
                    'status': status,
                    'category': category,
                    'reason': reason,
                    'detailedReason': detailedReason
                }
                list_of_exceptions.append(exception_dict)
        return list_of_exceptions

    @keyword
    def get_resolved_exception_category_reason_and_detailed_reason(self, response):
        list_of_exceptions = []
        for item in response["exceptions"]:
            if item['status'] == 'RESOLVED':
                status = item["status"]
                category = item["category"]
                reason = item["reason"]
                detailedReason = item["detailedReason"]
                exception_dict = {
                    'status': status,
                    'category': category,
                    'reason': reason,
                    'detailedReason': detailedReason
                }
                list_of_exceptions.append(exception_dict)
        return list_of_exceptions

    @keyword
    def get_actual_exception_status_category_reason_and_detailed_reason(self, response, status):
        list_of_exceptions = []
        for item in response["exceptions"]:
            if item['status'] == status:
                status = item["status"]
                category = item["category"]
                reason = item["reason"]
                detailedReason = item["detailedReason"]
                exception_dict = {
                    'status': status,
                    'category': category,
                    'reason': reason,
                    'detailedReason': detailedReason
                }
                list_of_exceptions.append(exception_dict)
        return list_of_exceptions

    @keyword
    def get_onbase_tasktype_and_status(self, response):
        list_of_tasks = []
        for item in response["tasks"]:
            tasktype = item['taskType']
            status = item['status']
            tasktype_status_dict = {
                'status': status,
                'tasktype': tasktype
            }
            list_of_tasks.append(tasktype_status_dict)
        return list_of_tasks

    @keyword
    def get_exception_id_from_case_detail_api(self, response):
        for item in response["exceptions"]:
            if item['status'] == 'NEW' and item['reason'] == 'Agent product training status':
                return item['externalId']

    @keyword
    def get_notes_count_present_on_ui(self, response):
        notes_count = 0
        for item in response['notes']:
            if item['internal'] == 'false' and item['author'] != 'ECMweb03':
                notes_count += 1
        return notes_count

    @keyword
    def get_status_of_tasks_present_in_case_detail(self, response):
        if response['tasks']:
            return True
        else:
            return False

    @keyword
    def create_task_on_onbase(self, url, lob, caseId, taskWVClassName, taskType, nigoId):
        nigoId = int(nigoId)
        caseId = int(caseId)
        headers = {
            'Content-Type': 'application/json',
            'Accept': 'application/json'
        }
        payload = {
            "lob": lob,
            "caseId": caseId,
            "taskWVClassName": taskWVClassName,
            "taskType": taskType,
            "attributeValues": {},
            "nigoIds": [
                nigoId
            ]
        }

        json_payload = json.dumps(payload)
        try:
            response = requests.post(url, headers=headers, data=json_payload)

            if response.status_code == 200:
                print("POST request successful.")
                response_data = response.json()
                if 'taskId' in response_data:
                    return response_data['taskId']
            else:
                print("POST request failed. Status code:", response.status_code)
        except requests.exceptions.RequestException as e:
            print("Error sending POST request:", e)

    @keyword
    def add_update_case_or_task_attributes(self, url, lob, taskWVClassName, taskId, attributeKey, attributeValue):
        headers = {
            'Content-Type': 'application/json',
            'Accept': 'application/json'
        }
        payload = {
            "lob": lob,
            "taskOrCaseClassName": taskWVClassName,
            "taskOrCaseId": taskId,
            "attributeValuePair": {
                f"{attributeKey}": attributeValue
            }
        }
        json_payload = json.dumps(payload)
        try:
            response = requests.post(url, headers=headers, data=json_payload)

            if response.status_code == 200:
                print("POST request successful.")
            else:
                print("POST request failed. Status code:", response.status_code)
        except requests.exceptions.RequestException as e:
            print("Error sending POST request:", e)

    @keyword
    def manage_task_from_onbase(self, url, lob, taskId, queueNameStatus):
        headers = {
            'Content-Type': 'application/json',
            'Accept': 'application/json'
        }
        payload = {
            "lob": lob,
            "taskID": taskId,
            "queueName": queueNameStatus
        }
        json_payload = json.dumps(payload)
        try:
            response = requests.post(url, headers=headers, data=json_payload)

            if response.status_code == 200:
                print("POST request successful.")
            else:
                print("POST request failed. Status code:", response.status_code)
        except requests.exceptions.RequestException as e:
            print("Error sending POST request:", e)

    @keyword
    def find_tasks_attributes(self, url, lob, taskId, taskWVClassName):
        headers = {
            'Content-Type': 'application/json',
            'Accept': 'application/json'
        }
        payload = {
            "lob": lob,
            "taskID": taskId,
            "attributes": {},
            "taskClassName": taskWVClassName
        }
        json_payload = json.dumps(payload)
        try:
            response = requests.post(url, headers=headers, data=json_payload)
            if response.status_code == 200:
                print("POST request successful.")
                return response.json()
            else:
                print("POST request failed. Status code:", response.status_code)
        except requests.exceptions.RequestException as e:
            print("Error sending POST request:", e)

    @keyword
    def get_queuename_and_suitability_status(self, response):
        results = {}

        def search_keys(api_response):
            if isinstance(api_response, dict):
                for key, value in api_response.items():
                    if key == 'queueName' or key == 'suitabilityStatus':
                        results[key] = value
                    elif isinstance(value, dict):
                        search_keys(value)
                    elif isinstance(value, list):
                        for item in value:
                            search_keys(item)

        search_keys(response)
        return results

    @keyword
    def get_status_and_task_type_from_case_detail_api(self, response_api, externalTaskId):
        specific_id = str(externalTaskId)
        task_info = {key: task[key] for task in response_api["tasks"] if task["externalTaskId"] == specific_id for key
                     in
                     ["status", "taskType"]}
        return task_info

    @keyword
    def create_task_on_onbase_link_with_multiple_nigos(self, url, lob, caseId, taskWVClassName, taskType, *args):
        nigo_ls = []
        for index, arg in enumerate(args, start=1):
            try:
                int_value = int(arg)
                nigo_ls.append(int_value)
            except ValueError:
                print(f"Warning: Could not convert '{arg}' to an integer. It will be skipped.")
        caseId = int(caseId)
        headers = {
            'Content-Type': 'application/json',
            'Accept': 'application/json'
        }
        payload = {
            "lob": lob,
            "caseId": caseId,
            "taskWVClassName": taskWVClassName,
            "taskType": taskType,
            "attributeValues": {},
            "nigoIds": nigo_ls
        }

        json_payload = json.dumps(payload)
        try:
            response = requests.post(url, headers=headers, data=json_payload)

            if response.status_code == 200:
                print("POST request successful.")
                response_data = response.json()
                if 'taskId' in response_data:
                    return response_data['taskId']
            else:
                print("POST request failed. Status code:", response.status_code)
        except requests.exceptions.RequestException as e:
            print("Error sending POST request:", e)

    @keyword
    def get_step_details_by_stage_id(self, api_response, input_id, expected_response):
        if isinstance(api_response, str):
            api_response = ast.literal_eval(api_response)

        if isinstance(expected_response, str):
            expected_response = ast.literal_eval(expected_response)

        if not isinstance(api_response, list):
            api_response = [api_response]
        if not isinstance(expected_response, list):
            expected_response = [expected_response]

        step_details_list = []

        if isinstance(api_response, list):
            for response in api_response:
                if isinstance(response, dict):
                    stages = response.get("stages", [])
                    for stage in stages:
                        if isinstance(stage, dict) and stage.get("id") == input_id:
                            steps = stage.get("steps", [])
                            for step in steps:
                                instance_info = step.get("instanceInfo", {})
                                if instance_info:
                                    step_details_list.append({
                                        "id": step.get("id"),
                                        "identifier": instance_info.get("identifier"),
                                        "stepStatus": step.get("stepStatus"),
                                        "multiInstance": step.get("multiInstance")
                                    })
                else:
                    BuiltIn().log_to_console(f"Skipping non-dictionary response in api_response: {response}")
        BuiltIn().log_to_console("**********************************")
        BuiltIn().log_to_console(f"{step_details_list}")
        BuiltIn().log_to_console("**********************************")
        if step_details_list:

            if len(step_details_list) != len(expected_response):
                BuiltIn().log_to_console(
                    f"Error: The number of steps does not match. Actual: {len(step_details_list)}, Expected: {len(expected_response)}")
                raise AssertionError("The number of items in actual response does not match the expected response.")

            BuiltIn().log_to_console(f"Comparing results for id '{input_id}':")
            for actual_detail, expected_detail in zip(step_details_list, expected_response):
                BuiltIn().log_to_console("-----------------------------------------------------------")
                BuiltIn().log_to_console(f"Actual Result:")
                BuiltIn().log_to_console(f"id: {actual_detail['id']}")
                BuiltIn().log_to_console(f"identifier: {actual_detail['identifier']}")
                BuiltIn().log_to_console(f"stepStatus: {actual_detail['stepStatus']}")
                BuiltIn().log_to_console(f"multiInstance: {actual_detail['multiInstance']}\n")

                BuiltIn().log_to_console(f"Expected Result:")
                BuiltIn().log_to_console(f"id: {expected_detail['id']}")
                BuiltIn().log_to_console(f"identifier: {expected_detail['identifier']}")
                BuiltIn().log_to_console(f"stepStatus: {expected_detail['stepStatus']}")
                BuiltIn().log_to_console(f"multiInstance: {expected_detail['multiInstance']}")
                BuiltIn().log_to_console("-----------------------------------------------------------")

                if actual_detail != expected_detail:
                    BuiltIn().log_to_console(f"Error: Actual detail does not match expected detail for id {input_id}.")
                    raise AssertionError(
                        f"Actual detail does not match expected detail: {actual_detail} != {expected_detail}")

            BuiltIn().log_to_console("The API response and expected response match!")
        else:
            BuiltIn().log_to_console(f"No details found for id '{input_id}'")
            raise AssertionError(f"No details found for id '{input_id}'")

        return step_details_list

    @keyword
    def check_detailed_reason_exists(self, api_response, input_reason):
        flag = False
        if 'exceptions' in api_response and isinstance(api_response['exceptions'], list):
            for exception in api_response['exceptions']:
                if 'detailedReason' in exception and exception['detailedReason'] == input_reason:
                    BuiltIn().log_to_console("-----------------------------------------------------------")
                    BuiltIn().log_to_console(f"Exception is : {exception}")
                    BuiltIn().log_to_console("-----------------------------------------------------------")
                    flag = True

        if not flag:
            BuiltIn().log_to_console("-----------------------------------------------------------")
            BuiltIn().log_to_console(f"{input_reason} is not present in the response")
            raise AssertionError(f"No detailsReason as {input_reason} found")


    @keyword
    def check_exceptions_exist(self, api_response, expected_exceptions):

        import ast
        from robot.libraries.BuiltIn import BuiltIn

        exception_ids = []

        try:
            # Convert string input into list of dicts
            expected_exceptions_list = ast.literal_eval(expected_exceptions)
            if not isinstance(expected_exceptions_list, list):
                raise ValueError("Expected input must be a stringified list of dictionaries.")
        except (ValueError, SyntaxError) as e:
            BuiltIn().log_to_console(f"Invalid format for expected_exceptions: {e}")
            raise

        # Ensure response has 'exceptions'
        if 'exceptions' not in api_response or not isinstance(api_response['exceptions'], list):
            raise AssertionError("API response does not contain a valid 'exceptions' list.")

        for expected in expected_exceptions_list:
            match_found = False
            for actual in api_response['exceptions']:
                if all(item in actual.items() for item in expected.items()):
                    # Extract only expected keys from actual
                    filtered_actual = {key: actual.get(key) for key in expected.keys()}

                    BuiltIn().log_to_console("-----------------------------------------------------------")
                    BuiltIn().log_to_console("Exception details match!")
                    BuiltIn().log_to_console(f"Expected: {expected}")
                    BuiltIn().log_to_console(f"Actual:   {filtered_actual}")
                    BuiltIn().log_to_console("-----------------------------------------------------------")

                    BuiltIn().log("-----------------------------------------------------------")
                    BuiltIn().log("Exception details match!")
                    BuiltIn().log(f"Expected: {expected}")
                    BuiltIn().log(f"Actual:   {filtered_actual}")
                    BuiltIn().log("-----------------------------------------------------------")
                    exception_ids.append(actual['id'])
                    match_found = True
                    break
            if not match_found:
                BuiltIn().log_to_console(f"Expected exception not found: {expected}")
                raise AssertionError(f"Missing expected exception: {expected}")
        print("exception_ids", exception_ids)
        return exception_ids

    @keyword
    def parse_list_string(self,raw):
        cleaned = re.sub(r'(?<=\[|\s|,)([a-zA-Z_][\w]*)(?=,|\s|\])', r'"\1"', raw)
        return ast.literal_eval(cleaned)
    @keyword
    def get_step_mapped_exception_id(self, response, stage_id, step_id):

        mapped_exceptions_ids = []

        try:

            stage_ids = self.parse_list_string(stage_id)
            step_ids = self.parse_list_string(step_id)
            if not isinstance(stage_ids, list) or not isinstance(step_ids, list):
                raise ValueError("stage_id and step_id must be stringified lists.")
        except (ValueError, SyntaxError) as e:
            BuiltIn().log_to_console(f"Invalid format for stage_id or step_id: {e}")
            raise

        for item in response.get('stages', []):
            if item.get("id") in stage_ids:
                for step in item.get("steps", []):
                    if step.get("id") in step_ids:
                        if step.get("mappedExceptions"):
                            mapped_exceptions_ids.extend(step["mappedExceptions"])

        return mapped_exceptions_ids

    @keyword
    def get_particular_step_details_by_stage_and_step_id(self, api_response, stage_id, step_id, expected_response):
        if isinstance(api_response, str):
            api_response = ast.literal_eval(api_response)

        if isinstance(expected_response, str):
            expected_response = ast.literal_eval(expected_response)

        if not isinstance(expected_response, list):
            expected_response = [expected_response]

        if not isinstance(api_response, list):
            api_response = [api_response]

        step_details_list = []
        eventRef = []

        if isinstance(api_response, list):
            for response in api_response:
                if isinstance(response, dict):
                    stages = response.get("stages", [])
                    for stage in stages:
                        if isinstance(stage, dict) and stage.get("id") == stage_id:
                            steps = stage.get("steps", [])
                            for step in steps:
                                if step.get("id") == step_id:
                                    step_details_list.append({
                                        "stage_id": stage_id,
                                        "step_id": step.get("id"),
                                        "stepStatus": step.get("stepStatus"),
                                    })
                                    eventRef.append(step.get("eventRef"))
                else:
                    BuiltIn().log_to_console(f"Skipping non-dictionary response in api_response: {response}")

        if step_details_list:
            if len(step_details_list) != len(expected_response):
                BuiltIn().log_to_console(
                    f"Error: The number of steps does not match. Actual: {len(step_details_list)}, Expected: {len(expected_response)}"
                )
                return False, eventRef

            BuiltIn().log_to_console(f"Comparing results for stage ID '{stage_id}' and step ID '{step_id}':")
            for actual_detail, expected_detail in zip(step_details_list, expected_response):
                BuiltIn().log_to_console("-----------------------------------------------------------")
                BuiltIn().log_to_console(f"Actual Result: {actual_detail}")
                BuiltIn().log_to_console(f"Expected Result: {expected_detail}")
                BuiltIn().log_to_console("-----------------------------------------------------------")

                if actual_detail != expected_detail:
                    BuiltIn().log_to_console(
                        f"Error: Actual detail does not match expected detail for stage '{stage_id}', step '{step_id}'."
                    )
                    return False, eventRef

            BuiltIn().log_to_console("The API response and expected response match.")
            return True, eventRef
        else:
            BuiltIn().log_to_console(f"No details found for stage ID '{stage_id}' and step ID '{step_id}'")
            return False, eventRef

    @keyword
    def validate_event_lifecad_contractstatus_event_ids(self, api_response, expected_ids):

        if isinstance(api_response, str):
            api_response = ast.literal_eval(api_response)

        valid_event_ids = [
            event["id"] for event in api_response.get("events", [])
            if event.get("id") in expected_ids

        ]

        expected_ids.sort()
        valid_event_ids.sort()

        BuiltIn().log_to_console(f"Expected IDs: {expected_ids}")
        BuiltIn().log_to_console(f"Valid Event IDs: {valid_event_ids}")

        if expected_ids == valid_event_ids:
            BuiltIn().log_to_console("All expected event IDs are present and match the conditions.")
            return True
        else:
            missing_ids = list(set(expected_ids) - set(valid_event_ids))
            BuiltIn().log_to_console(f"Missing expected event IDs: {missing_ids}")
            return False

    @keyword
    def check_onbase_document_present_in_case_detail_api(self, response_json):
        max_attempts = 5
        attempts = 0

        while attempts < max_attempts:
            found_nb_purchase = any(
                doc for doc in response_json["documents"]
                if "NB Purchase w App" in doc["name"] and doc["source"] == "Policy"
            )

            found_attachment = any(
                doc for doc in response_json["documents"]
                if "Attachment ZLATTACHMENT" in doc["name"] and doc["source"] == "Policy"
            )
            if found_nb_purchase and found_attachment:
                BuiltIn().log_to_console("Both expected documents found! NB Purchase w App and Attachments found!")
                break
            else:
                attempts += 1
                if attempts >= max_attempts:
                    BuiltIn().log_to_console("Timeout! Expected documents not found after 10 minutes. Exiting.")
                    break
                BuiltIn().log_to_console(
                    f"Attempt {attempts}/{max_attempts}: Expected documents not found. Retrying in 2 minutes...")
                time.sleep(120)

    @keyword
    def check_sed_document_present_in_case_detail_api(self, response_json):
        max_attempts = 5
        attempts = 0

        while attempts < max_attempts:
            found_sed_document = any(
                doc for doc in response_json["documents"]
                if "Policy Page" in doc["name"] and doc["source"] == "Correspondence"
            )

            if found_sed_document:
                BuiltIn().log_to_console("Expected documents found! SED document found!")
                break
            else:
                attempts += 1
                if attempts >= max_attempts:
                    BuiltIn().log_to_console("Timeout! Expected documents not found after 10 minutes. Exiting.")
                    break
                BuiltIn().log_to_console(
                    f"Attempt {attempts}/{max_attempts}: Expected documents not found. Retrying in 2 minutes...")
                time.sleep(120)
