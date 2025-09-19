import json
import requests
from robot.api.deco import library, keyword
from robot.libraries.BuiltIn import BuiltIn

from resources.vo.FilePropertiesVo import FilePropertiesVo
from selenium.webdriver.chrome.options import Options
from selenium import webdriver
from selenium.webdriver.common.by import By
import time
from urllib.parse import urlparse, parse_qs
import logging
from datetime import datetime, timedelta


@library
class QueueManagementApi:
    fileProperties = FilePropertiesVo()
    auth_url = "https://login.qa.zinnia.com/authorize"
    token_url = "https://login.qa.zinnia.com"
    client_id = "8LHNwcZrMwxIoAeUxYpBCRTXB6dgB2fX"
    client_secret = "burCPt4345XW8mlhetVUck9e9I2CcXY9X11fQDMGgStzmzvUtcNacwbEFzaF1JbO"
    redirect_uri = "https://oauth.pstmn.io/v1/callback"
    audience = "https://qa.api.zinnia.io"
    username = "atharva.nidhonkar@zinnia.com"
    case_id = "CA0000369867"
    url_create_task = f"https://qa-bpm.se2.com/case/v2/cases/{case_id}/tasks"
    url_get_tasks_by_assignee = "https://qa-bpm.se2.com/case/v1/tasks/assigned"
    url_update_task_api = "https://qa-bpm.se2.com/case/v2/cases/"
    url_get_tasks_unassigned = "https://qa-bpm.se2.com/case/v1/tasks/unassigned"
    logging.basicConfig(level=logging.INFO)
    logger = logging.getLogger(__name__)

    @keyword
    def open_browser_to_authorization_url(self, auth_url, client_id, redirect_uri, audience):

        chrome_options = Options()
        chrome_options.add_argument("--headless")
        
        # Suppress GCM (Google Cloud Messaging) errors and other unwanted messages
        chrome_options.add_argument("--disable-background-networking")
        chrome_options.add_argument("--disable-background-timer-throttling")
        chrome_options.add_argument("--disable-backgrounding-occluded-windows")
        chrome_options.add_argument("--disable-features=TranslateUI")
        chrome_options.add_argument("--disable-ipc-flooding-protection")
        chrome_options.add_argument("--no-default-browser-check")
        chrome_options.add_argument("--no-first-run")
        chrome_options.add_argument("--disable-default-apps")
        chrome_options.add_argument("--disable-sync")
        chrome_options.add_argument("--disable-background-mode")
        chrome_options.add_argument("--disable-component-update")
        chrome_options.add_argument("--disable-logging")
        chrome_options.add_argument("--log-level=3")
        chrome_options.add_argument("--silent")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-gpu-sandbox")
        chrome_options.add_argument("--disable-software-rasterizer")
        chrome_options.add_argument("--disable-infobars")
        chrome_options.add_argument("--disable-notifications")
        chrome_options.add_experimental_option("excludeSwitches", ["enable-automation", "enable-logging"])
        chrome_options.add_experimental_option('useAutomationExtension', False)

        driver = webdriver.Chrome(options=chrome_options)

        authorization_url = f"{auth_url}?response_type=code&client_id={client_id}&redirect_uri={redirect_uri}&audience={audience}"

        driver.get(authorization_url)

        driver.maximize_window()

        return driver

    @keyword
    def login_to_oauth(self, driver, username):

        username_field = driver.find_element(By.ID, "username")
        username_field.clear()
        username_field.send_keys(username)

        submit_button = driver.find_element(By.XPATH, "//button[@type='submit']")
        submit_button.click()

        time.sleep(30)

    @keyword
    def get_authorization_code_from_url(self, driver):

        url = driver.current_url

        parsed_url = urlparse(url)
        query_params = parse_qs(parsed_url.query)
        auth_code = query_params.get("code", [None])[0]

        driver.quit()

        if not auth_code:
            raise Exception("Authorization code not found in URL.")

        return auth_code

    @keyword
    def generate_oauth_token(self, token_url, client_id, client_secret, redirect_uri, auth_code):
        headers = {
            "Content-Type": "application/x-www-form-urlencoded"
        }

        payload = {
            "client_id": client_id,
            "client_secret": client_secret,
            "redirect_uri": redirect_uri,
            "grant_type": "authorization_code",
            "code": auth_code
        }

        response = requests.post(f"{token_url}/oauth/token", headers=headers, data=payload)

        if response.status_code != 200:
            raise Exception(f"Token request failed: {response.status_code}, {response.text}")

        response_data = response.json()
        token = response_data.get("access_token")

        if not token:
            raise Exception("Access token not found in response.")

        return token

    @keyword
    def create_task_from_queue_management(self, url, token):
        future_date = (datetime.now() + timedelta(days=2)).strftime("%Y-%m-%d")

        payload = {
            "source": "BPM.Redemption",
            "taskType": "WithdrawalFormInputTask",
            "status": "NEW",
            "impededReason": "scheduler test",
            "impededTillDate": future_date,
        }
        json_payload = json.dumps(payload)

        headers = {
            'Content-Length': str(len(json_payload)),
            'Content-Type': 'application/json',
            'Accept': 'application/json',
            'Host': 'qa-bpm.se2.com',
            'Authorization': f'Bearer {token}'
        }

        try:
            response = requests.post(url, headers=headers, data=json_payload)

            if response.status_code != 200:
                raise AssertionError(
                    f"Expected status code 200 but got {response.status_code}. Response: {response.text}")

            response_data = response.json()
            if "id" not in response_data:
                raise AssertionError("Response does not contain expected 'taskId' field.")

            return response_data

        except requests.exceptions.RequestException as e:
            raise AssertionError(f"Error sending POST request: {e}")

    @keyword
    def get_available_tasks_queue_management(self, url, token):
        headers = {
            'Accept': 'application/json',
            'Authorization': f'Bearer {token}'
        }

        try:
            response = requests.get(url, headers=headers)

            if response.status_code == 200:
                print("API call successful.")
                print("Response:", response.json())
                return response.json()
            else:
                print("API call failed. Status code:", response.status_code)
                print("Response:", response.text)
                return response.text
        except Exception as e:
            print("Error making API call:", e)

    @keyword
    def get_tasks_by_assignee_queue_management(self, url, token):
        headers = {
            'Accept': 'application/json',
            'Authorization': f'Bearer {token}'
        }

        try:
            response = requests.get(url, headers=headers)
            response.raise_for_status()

            data = response.json()

            if not data:
                raise ValueError("API response is empty. Expected task data.")
            return data

        except requests.exceptions.HTTPError as http_err:
            print(f"HTTP error occurred: {http_err}")
            raise
        except requests.exceptions.RequestException as req_err:
            print(f"Request error occurred: {req_err}")
            raise
        except ValueError as val_err:
            print(f"Validation error: {val_err}")
            raise
        except Exception as err:
            print(f"Unexpected error: {err}")
            raise

    @keyword
    def update_task_queue_management(self, url, token, status_for_update_task):

        future_date = datetime.now() + timedelta(days=30)
        formatted_date = future_date.strftime("%Y-%m-%dT%H:%M:%S.") + f"{future_date.microsecond:07d}"

        payload = {
            "source": "BPM.Redemption",
            "taskType": "WithdrawalFormInputTask",
            "status": status_for_update_task,
            "impededReason": "scheduler test",
            "impededTillDate": formatted_date
        }
        json_payload = json.dumps(payload)

        headers = {
            'Content-Length': str(len(json_payload)),
            'Content-Type': 'application/json',
            'Accept': 'application/json',
            'Host': 'qa-bpm.se2.com',
            'Authorization': f'Bearer {token}'
        }

        try:
            response = requests.put(url, headers=headers, data=json_payload)

            if response.status_code != 200:
                raise AssertionError(
                    f"Failed to update task. Expected status 200 but got {response.status_code}. Response: {response.text}")

            response_data = response.json()
            if not response_data:
                raise AssertionError("Empty JSON response received after task update.")

            BuiltIn().log(f"Task successfully updated to status: {status_for_update_task}")
            BuiltIn().log_to_console(f"Task successfully updated to status: {status_for_update_task}")

            return response_data

        except requests.exceptions.RequestException as req_err:
            raise AssertionError(f"HTTP request failed: {req_err}")

        except ValueError as val_err:
            raise AssertionError(f"Failed to parse JSON response: {val_err}")

        except Exception as err:
            raise AssertionError(f"Unexpected error occurred: {err}")

    @keyword
    def claim_next_task_queue_management(self, url, token):
        headers = {
            'Accept': 'application/json',
            'Authorization': f'Bearer {token}'
        }

        try:
            response = requests.patch(url, headers=headers)

            assert response.status_code == 200, (
                f"[FAIL] Claim Task API failed. Status code: {response.status_code}, Response: {response.text}"
            )
            return response.json()

        except Exception as e:
            print("[ERROR] Exception during Claim Task API call:", e)
            raise

    @keyword
    def is_task_id_available_in_get_tasks_by_assignee(self, json_response):
        for id_value in json_response:
            if id_value['id']:
                return id_value['id'], True
            else:
                return False

    @keyword
    def extract_task_id_from_response(self, json_response):

        if not isinstance(json_response, dict):
            raise AssertionError(f"Expected response to be a dictionary, but got {type(json_response)}.")

        if "id" not in json_response:
            raise AssertionError("Response does not contain expected 'id' field.")

        task_id = json_response["id"]

        if not task_id:
            raise AssertionError("Task ID is empty or null in the response.")

        return task_id

    @keyword
    def extract_task_status_from_response(self, json_response, expected_task_status):

        if not isinstance(json_response, dict):
            raise AssertionError(f"Expected response to be a dictionary, but got {type(json_response)}.")

        if "status" not in json_response:
            raise AssertionError("Response does not contain expected 'status' field.")

        actual_task_status = json_response["status"]

        if actual_task_status == expected_task_status:
            raise AssertionError("Task status is empty or null in the response.")

        BuiltIn().log_to_console(f"Task successfully updated to {expected_task_status}")

    @keyword
    def start_task_queue_management(self, url, token):
        headers = {
            'Accept': 'application/json',
            'Authorization': f'Bearer {token}'
        }

        try:
            response = requests.get(url, headers=headers)

            assert response.status_code == 200, f"Expected status code 200 but got {response.status_code}"

            json_response = response.json()
            assert isinstance(json_response, dict), "Expected JSON response to be a dictionary"

            return json_response

        except AssertionError as ae:
            print("Assertion failed:", ae)
            raise

        except Exception as e:
            print("Error making API call:", e)
            raise

    @keyword
    def get_tasks_unassigned_queue_management(self, url, token):
        headers = {
            'Accept': 'application/json',
            'Authorization': f'Bearer {token}'
        }

        try:
            response = requests.get(url, headers=headers)

            if response.status_code == 200:
                print("API call successful.")
                print("Response:", response.json())
                return response.json()
            else:
                print("API call failed. Status code:", response.status_code)
                print("Response:", response.text)
                return response.text
        except Exception as e:
            print("Error making API call:", e)

    @keyword
    def unassigned_specific_task_queue_management(self, url, token):
        headers = {
            'Accept': 'application/json',
            'Authorization': f'Bearer {token}'
        }

        try:
            response = requests.delete(url, headers=headers)

            if response.status_code != 200:
                raise AssertionError(
                    f"Expected status code 200 but got {response.status_code}. Response: {response.text}"
                )

            response_data = response.json()

            if "status" not in response_data or response_data["status"] != "SUCCESS":
                raise AssertionError(
                    f"Expected response to contain 'status' with value 'SUCCESS'. Got: {response_data}"
                )

            return response_data

        except requests.exceptions.RequestException as req_err:
            raise AssertionError(f"HTTP request error: {req_err}")

        except ValueError as val_err:
            raise AssertionError(f"Error parsing response JSON: {val_err}")

        except Exception as e:
            raise AssertionError(f"Unexpected error occurred: {e}")

    @keyword
    def automate_oauth_authorization_and_token_retrieval(self):
        driver = self.open_browser_to_authorization_url(self.auth_url, self.client_id, self.redirect_uri, self.audience)

        self.login_to_oauth(driver, self.username)

        auth_code = self.get_authorization_code_from_url(driver)

        token = self.generate_oauth_token(self.token_url, self.client_id, self.client_secret, self.redirect_uri,
                                          auth_code)

        return token

    @keyword
    def queue_management_process(self, flow_type):
        if flow_type == "queue_create_task":
            token = self.automate_oauth_authorization_and_token_retrieval()
            response_create_task_api = self.create_task_from_queue_management(self.url_create_task, token)
            self.extract_task_id_from_response(response_create_task_api)

        elif flow_type == "queue_retrival_of_assigned_task":
            token = self.automate_oauth_authorization_and_token_retrieval()
            response_get_tasks_assignee = self.get_tasks_by_assignee_queue_management(self.url_get_tasks_by_assignee,
                                                                                      token)
            if response_get_tasks_assignee:
                for task in response_get_tasks_assignee:
                    task_id = task["id"]
                    print(f"Assigned Task ID: {task_id}")

                    url_for_unassigned_task = f"https://qa.api.zinnia.io/case/v1/tasks/{task_id}/assignments"
                    self.unassigned_specific_task_queue_management(url_for_unassigned_task, token)
            else:
                response_create_task_api = self.create_task_from_queue_management(
                    self.url_create_task, token
                )
                new_task_id = self.extract_task_id_from_response(response_create_task_api)
                if new_task_id and new_task_id.strip() != "":
                    url_for_claim_task = f"https://qa-bpm.se2.com/case/v1/tasks/{new_task_id}/claim"
                    self.claim_next_task_queue_management(url_for_claim_task, token)
                    print(f"Claimed Task ID: {new_task_id}")
                else:
                    raise Exception("Task creation failed, unable to claim task.")

        elif flow_type == "queue_update_task":
            token = self.automate_oauth_authorization_and_token_retrieval()
            response_create_task_api = self.create_task_from_queue_management(
                self.url_create_task, token
            )
            new_task_id = self.extract_task_id_from_response(response_create_task_api)
            url_update = f"{self.url_update_task_api}{self.case_id}/tasks/{new_task_id}"
            response_update_task_api = self.update_task_queue_management(url_update, token, "INPROGRESS")
            self.extract_task_status_from_response(response_update_task_api, "INPROGRESS")

            response_update_task_api = self.update_task_queue_management(url_update, token, "IMPEDED")
            self.extract_task_status_from_response(response_update_task_api, "IMPEDED")

        elif flow_type == "queue_claim_next_task":
            token = self.automate_oauth_authorization_and_token_retrieval()
            response_create_task_api = self.create_task_from_queue_management(
                self.url_create_task, token
            )
            new_task_id = self.extract_task_id_from_response(response_create_task_api)
            url_for_claim_task = f"https://qa-bpm.se2.com/case/v1/tasks/{new_task_id}/claim"
            self.claim_next_task_queue_management(url_for_claim_task, token)


        elif flow_type == "queue_start_task":
            token = self.automate_oauth_authorization_and_token_retrieval()
            response_create_task_api = self.create_task_from_queue_management(
                self.url_create_task, token
            )
            new_task_id = self.extract_task_id_from_response(response_create_task_api)
            url_for_claim_task = f"https://qa-bpm.se2.com/case/v1/tasks/{new_task_id}/claim"
            response_claim_task = self.claim_next_task_queue_management(url_for_claim_task, token)
            claimed_task_id = self.extract_task_id_from_response(response_claim_task)

            url_for_start_task = f"https://qa.api.zinnia.io/case/v2/tasks/{claimed_task_id}"

            response_start_task = self.start_task_queue_management(url_for_start_task, token)

            task_id = self.extract_task_id_from_response(response_start_task)

            url_for_update_task = f"{self.url_update_task_api}{self.case_id}/tasks/{task_id}"

            BuiltIn().log(f"Updating {task_id} to INPROGRESS")
            BuiltIn().log_to_console(f"Updating {task_id} to INPROGRESS")
            response_update_task_api = self.update_task_queue_management(url_for_update_task, token, "INPROGRESS")
            self.extract_task_status_from_response(response_update_task_api, "INPROGRESS")

            BuiltIn().log(f"Updating {task_id} to IMPEDED")
            BuiltIn().log_to_console(f"Updating {task_id} to IMPEDED")
            response_update_task_api = self.update_task_queue_management(url_for_update_task, token, "INPROGRESS")
            self.extract_task_status_from_response(response_update_task_api, "IMPEDED")

