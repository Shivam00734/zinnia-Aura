import json

import requests
from robot.api.deco import library, keyword
from robot.libraries.BuiltIn import BuiltIn

from resources.utilities.ExcelUtilities import ExcelUtilities
from resources.utilities.FileUtils import FileUtils
from resources.utilities.ReadConfig import ReadConfig


@library
class OnBaseApi:
    excelSheet = ExcelUtilities()
    read_config = ReadConfig()
    file = FileUtils()

    @keyword
    def validate_nb_application_case_status(self, input_file_path, testcase_id):
        project_dir = self.file.get_project_directory()
        input_file_path = project_dir + input_file_path

        # contract_number = self.excelSheet.getValueFromExcel(input_file_path, 1, testcase_id, 7)
        contract_number  = self.excelSheet.get_value_from_excel_by_column_name(input_file_path, "output_data", testcase_id, "${contract_number}")

        client_code  = self.excelSheet.get_value_from_excel_by_column_name(input_file_path, "output_data", testcase_id, "${client_code}")
        # client_code = self.excelSheet.getValueFromExcel(input_file_path, 0, testcase_id, 5)

        document_list_response = self.get_document_list(client_code, contract_number)

        nb_purchase_documents = [doc for doc in document_list_response['items']
                                 if doc['documentType'] == 'NB Purchase w App' or doc[
                                        'documentType'] == 'Annuity Application' or doc['documentType'] == 'Incoming Transfer']

        if nb_purchase_documents:
            nb_purchase_case_id = nb_purchase_documents[0]['caseId']

            if nb_purchase_case_id:
                case_details_response = self.get_case_details(client_code, nb_purchase_case_id)

                tasks = case_details_response.get('tasks', [])
                task_type_found = any(task['taskType'] == 'NB Application Validation' for task in tasks)

                if not task_type_found:
                    raise AssertionError("NB Application Validation task not found.")
                print("NB Application Validation case created!")

            else:
                raise AssertionError("NB Application Validation case not created!")

        else:
            raise AssertionError("NB Application Validation case not created!")

    @keyword
    def get_document_list(self, client_code, contract_number):
        url = self.read_config.getValueByKey('OnBaseGetDocumentListApi')
        params = {
            'request.clientCode': client_code,
            'request.contractNumber': contract_number
        }
        response = requests.get(url, params=params, headers={'Accept': 'application/json'})
        if response.status_code == 200:
            print("API call successful.")
            return response.json()
        else:
            print("API call failed. Status code:", response.status_code)
            print("Response:", response.text)
            raise Exception("API call failed. Status code:", response.status_code)

    @keyword
    def get_case_details(self, lob, case_id):
        url = self.read_config.getValueByKey('OnBaseGetCaseDetailsApi')
        params = {
            'request.lob': lob,
            'request.caseId': case_id
        }
        response = requests.get(url, params=params, headers={'Accept': 'application/json'})
        response.raise_for_status()
        return response.json()

    @keyword
    def add_update_case_or_task_attributes(self, lob, taskWVClassName, taskId, attributeKey, attributeValue):
        url = self.read_config.getValueByKey("onbase_add_update_case_or_task_attributes")
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
                return
            else:
                print("POST request failed. Status code:", response.status_code)
                print("Issue in add_update_case_or_task_attributes")
                print("Response:", response.text)
        except requests.exceptions.RequestException as e:
            print("Error sending POST request:", e)

    @keyword
    def create_task_on_onbase_link_with_multiple_nigos(self, lob, case_id, task_wv_class_name, task_type, *args):
        url = self.read_config.getValueByKey("onbase_create_task_api")
        nigo_ls = []
        for index, arg in enumerate(args, start=1):
            try:
                int_value = int(arg)
                nigo_ls.append(int_value)
            except ValueError:
                print(f"Warning: Could not convert '{arg}' to an integer. It will be skipped.")
        case_id = int(case_id)
        headers = {
            'Content-Type': 'application/json',
            'Accept': 'application/json'
        }
        payload = {
            "lob": lob,
            "caseId": case_id,
            "taskWVClassName": task_wv_class_name,
            "taskType": task_type,
            "attributeValues": {},
            "nigoIds": nigo_ls
        }
        json_payload = json.dumps(payload)
        try:
            response = requests.post(url, headers=headers, data=json_payload)

            if response.status_code == 200:
                response_data = response.json()
                if 'taskId' in response_data:
                    return response_data['taskId']
            else:
                print("POST request failed. Status code:", response.status_code)
                print("Issue in create_task_on_onbase_link_with_multiple_nigos")
                print("Response:", response.text)
        except requests.exceptions.RequestException as e:
            print("Error sending POST request:", e)

    @keyword
    def manage_task_from_onbase(self, lob, task_id, queue_name_status):
        if not queue_name_status:
            print(
                "Expected queuename not provided. Skipping manage task.")
            return

        url = self.read_config.getValueByKey("onbase_manage_task_api")
        headers = {
            'Content-Type': 'application/json',
            'Accept': 'application/json'
        }

        payload = {
            "lob": lob,
            "taskID": task_id,
            "queueName": queue_name_status
        }

        json_payload = json.dumps(payload)

        try:
            response = requests.post(url, headers=headers, data=json_payload)

            if response.status_code == 200:
                return
            else:
                print("POST request failed. Status code:", response.status_code)
                print("Issue in manage_task_from_onbase ")
                print("Response:", response.text)
        except requests.exceptions.RequestException as e:
            print("Error sending POST request:", e)

    @keyword
    def create_nigo_from_onbase(self, caseId, lob, dtg, category, reason, detailedReason):
        url = self.read_config.getValueByKey("onbase_create_nigo_url")
        caseId = int(caseId)
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
                print("Response:", response.text)
                raise ValueError(f"Bad Request (400): {response.text}")

            else:
                print(f"POST request failed. Status code: {response.status_code}")
                print("Issue in create_nigo_from_onbase")
                print("Response:", response.text)
                raise RuntimeError(f"Request failed with status {response.status_code}: {response.text}")

        except requests.exceptions.RequestException as e:
            print("Error sending POST request:", e)
            raise RuntimeError(f"Request error: {e}")

    @keyword
    def update_nigo_from_onbase(self, nigo_id, lob, nigo_status, resolution):
        url = self.read_config.getValueByKey("onbase_update_nigo_url")
        nigo_id = int(nigo_id)

        payload = {
            "lob": lob,
            "nigoId": nigo_id,
            "nigoStatus": nigo_status,
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
                BuiltIn().log("Nigo Updated Successfully")
                return

            else:
                print("POST request failed. Status code:", response.status_code)
                print("Issue in update_nigo_from_onbase")
                print("Response:", response.text)
        except requests.exceptions.RequestException as e:
            print("Error sending POST request:", e)

    @keyword
    def find_tasks_attributes(self, lob, taskId, taskWVClassName):
        url = self.read_config.getValueByKey("onbase_find_attributes_api")
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
                return response.json()
            else:
                print("POST request failed. Status code:", response.status_code)
                print("Issue in find_tasks_attributes")
                print("Response:", response.text)
        except requests.exceptions.RequestException as e:
            print("Error sending POST request:", e)