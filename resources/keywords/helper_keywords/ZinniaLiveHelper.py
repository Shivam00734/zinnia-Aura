import ast
import time
import re
from time import sleep
from robot.api.deco import library, keyword
from robot.libraries.BuiltIn import BuiltIn
from resources.keywords.api_keywords.ApiKeywords import ApiKeywords
from resources.keywords.api_keywords.LifeCadApi import LifeCadApi
from resources.keywords.api_keywords.OnBaseApi import OnBaseApi
from resources.keywords.data_creation_keywords.GenerateDTCC import GenerateDTCC
from resources.keywords.db_keywords.EventValidation import EventValidation
from resources.utilities.ExcelUtilities import ExcelUtilities
from resources.utilities.FileUtils import FileUtils
from resources.utilities.ReadConfig import ReadConfig


@library
class ZinniaLiveHelper:
    read_config = ReadConfig()
    api_keywords = ApiKeywords()
    generate_dtcc = GenerateDTCC()
    event_validate = EventValidation()
    excel = ExcelUtilities()
    file = FileUtils()
    lifecad_api = LifeCadApi()
    bi = BuiltIn()
    onbase_api = OnBaseApi()

    @keyword
    def authenticate_user_and_get_token(self):
        return self.api_keywords.authenticate_user(
            "https://login.qa.zinnia.com/oauth/token",
            "https://qa.api.zinnia.io",
            "client_credentials",
            "UuMribrP3e8zVhfHy6wPJ25lVYh1CWN3",
            "WQ4ZBFI0RaYnhlhrZBdw4ltrMk8IKT9bDm1DX_U28doSk4F4Au5KiAsoBCSNYWix"
        )

    @keyword
    def get_caseid_from_case_management_api(self, token, test_case_id):
        url = self.api_keywords.create_url("BaseUrlQa", "CaseIDEndPoint")
        contract_no = self.api_keywords.get_contract_number(test_case_id)
        for _ in range(12):
            response = self.api_keywords.case_management_api_response(url, token, contract_no)
            case_id = self.api_keywords.get_id_from_response(response)
            case_id_for_nigo = self.api_keywords.get_case_id_from_response(response)
            if case_id and case_id_for_nigo:
                return case_id, case_id_for_nigo, contract_no
            sleep(30)
        return None, None, contract_no

    @keyword
    def get_response_from_case_detail_api(self, token, case_id):
        url_for_case_detail_api = self.api_keywords.create_url("BaseUrlQa", "ResponseEndPoint", case_id)
        response_case_detail_api = self.api_keywords.case_detail_api_response(url_for_case_detail_api, token)
        return response_case_detail_api

    @keyword
    def validate_case_overview_status(self, expected_case_overview_status, token, case_id,
                                      expected_stage_status, stage_id):
        # --- Fetch API Response ---
        case_detail_response = self.get_response_from_case_detail_api(token, case_id)
        actual_case_overview_status = self.api_keywords.get_case_overview_status(case_detail_response)

        should_check_case_status = bool(expected_case_overview_status)
        should_check_stage_status = bool(expected_stage_status and stage_id)

        if not should_check_case_status and not should_check_stage_status:
            self.bi.log_to_console("⚠️  Skipping validation: No expected overview or stage status provided.")
            return case_detail_response

        # --- Validate Case Overview Status ---
        if should_check_case_status:
            status_match = self.bi.run_keyword_and_return_status(
                "Should Be Equal As Strings", actual_case_overview_status, expected_case_overview_status
            )
            if not status_match:
                raise AssertionError(
                    f"❌ Case Overview Status Mismatch: Expected '{expected_case_overview_status}', but got '{actual_case_overview_status}'"
                )

            self.bi.log_to_console("\n✅ Case Overview Status Validation Passed")
            self.bi.log_to_console(f"   ✔ Expected: '{expected_case_overview_status}'")
            self.bi.log_to_console(f"   ✔ Actual  : '{actual_case_overview_status}'")
            self.bi.log_to_console("--------------------------------------------------")

            self.bi.log("✅ Case Overview Status Validation Passed")
            self.bi.log(f"   ✔ Expected: '{expected_case_overview_status}'")
            self.bi.log(f"   ✔ Actual  : '{actual_case_overview_status}'")
            self.bi.log("--------------------------------------------------")

        # --- Validate Stage Status ---
        if should_check_stage_status:
            stage_ids = self.parse_list_string(stage_id.strip())
            expected_stage_statuses = self.parse_list_string(expected_stage_status.strip())

            for sid in stage_ids:
                stage_status_raw = self.api_keywords.get_stage_status(case_detail_response, sid)

                # Normalize to list
                actual_stage_statuses = (
                    [] if stage_status_raw is None
                    else stage_status_raw if isinstance(stage_status_raw, list)
                    else [stage_status_raw]
                )

                for expected_status in expected_stage_statuses:
                    if expected_status not in actual_stage_statuses:
                        raise AssertionError(
                            f"❌ Stage '{sid}' status mismatch: Expected '{expected_stage_statuses}', but got '{actual_stage_statuses}'"
                        )

                self.bi.log(
                    f"Stage '{sid}' status match: Expected: {expected_stage_statuses}, Actual: {actual_stage_statuses}")
                self.bi.log_to_console(f"✅ Stage '{sid}' status match!")
                self.bi.log_to_console(f"   ✔ Expected: {expected_stage_statuses}")
                self.bi.log_to_console(f"   ✔ Actual  : {actual_stage_statuses}")
                self.bi.log_to_console("--------------------------------------------------")

        return case_detail_response

    @keyword
    def validate_stage_status(self, response, expected_stage_status, stage_id):
        if not expected_stage_status:
            self.bi.log("Expected stage status is not provided. Skipping stage status validation.")
            self.bi.log_to_console("Expected stage status is not provided. Skipping stage status validation.")
            return

        actual_status = self.api_keywords.get_stage_status(response, stage_id)

        if expected_stage_status != actual_status:
            raise AssertionError(
                f"Stage status mismatch! Expected: '{expected_stage_status}', Actual: '{actual_status}'"
            )

        self.bi.log(f"Stage status match! Expected: '{expected_stage_status}', Actual: '{actual_status}'")
        self.bi.log("-----------------------------------------------------------")
        self.bi.log_to_console(f"Stage status match! Expected: '{expected_stage_status}', Actual: '{actual_status}'")
        self.bi.log_to_console("-----------------------------------------------------------")

    @keyword
    def parse_list_string(self, raw):
        cleaned = re.sub(r'(?<=\[|\s|,)([a-zA-Z_][\w]*)(?=,|\s|\])', r'"\1"', raw)
        return ast.literal_eval(cleaned)

    @keyword
    def validate_all_steps(self, token, case_id, stage_id, expected_step_status):

        # --- Skip validation if expected_step_status is empty ---
        if not expected_step_status or not expected_step_status.strip():
            print("Expected step status is empty. Skipping step validation.")
            return self.get_response_from_case_detail_api(token, case_id)

        # --- Parse stage ID and expected step status ---
        stage_ids = self.parse_list_string(stage_id.strip())

        try:
            expected_step_status_list = ast.literal_eval(expected_step_status)
            if not isinstance(expected_step_status_list, list):
                raise ValueError("Expected step status must be a list of dictionaries.")
        except Exception as e:
            raise AssertionError(f"Invalid format for expected_step_status: {e}")

        if len(stage_ids) != len(expected_step_status_list):
            raise AssertionError("Mismatch between number of stage IDs and step status dictionaries.")

        response = self.get_response_from_case_detail_api(token, case_id)
        for i, sid in enumerate(stage_ids):
            step_status_dict = expected_step_status_list[i]
            try:
                self.api_keywords.check_step_validation(response, sid, step_status_dict)
                self.api_keywords.print_step_validation(response, sid, step_status_dict)
            except AssertionError as e:
                raise AssertionError(f"Step validation failed for stage '{sid}': {str(e)}")

        return response

    @keyword
    def get_actual_policy_status_code_via_api(self, company_hierarchy_id, contract_number):
        actual_policy_status = self.api_keywords.get_actual_policy_status_code(company_hierarchy_id, contract_number)
        return actual_policy_status

    def get_expected_lifecad_policy_status_code(self, testcase_id):
        expected_policy_status = self.api_keywords.get_expected_policy_status_code(testcase_id)
        return expected_policy_status

    @keyword
    def validate_lifecad_policy_status_code(self, test_case_id, contract_number):
        hierarchy_id = self.api_keywords.get_company_hierarchy_id(test_case_id)
        actual_status = self.get_actual_policy_status_code_via_api(hierarchy_id, contract_number)
        expected_status = self.get_expected_lifecad_policy_status_code(test_case_id)

        if expected_status != actual_status:
            raise AssertionError(
                f"Policy status code mismatch! Expected: '{expected_status}', Actual: '{actual_status}'")
        self.bi.log("-----------------------------------------------------------")
        self.bi.log(f"Policy status code match! Expected: '{expected_status}', Actual: '{actual_status}'")
        self.bi.log_to_console("-----------------------------------------------------------")
        self.bi.log_to_console(f"Policy status code match! Expected: '{expected_status}', Actual: '{actual_status}'")

    @keyword
    def validate_nigo_cases(self, response, stage_id, expected_exception, expected_mapped_step):
        exception_id = self.api_keywords.check_exceptions_exist(response, expected_exception)
        mapped_id = self.api_keywords.get_step_mapped_exception_id(response, stage_id, expected_mapped_step)
        return exception_id, mapped_id

    @keyword
    def get_expected_value(self, actual_id):
        if isinstance(actual_id, list) and actual_id:
            return actual_id[0]

    @keyword
    def validate_nigo_exception_ids(self, exception_id, mapped_id):


        actual_mapped_id = self.get_expected_value(mapped_id)

        # Ensure exception_id is a list
        if isinstance(exception_id, list):
            if actual_mapped_id not in exception_id:
                raise AssertionError(
                    f"Expected Nigo Exception ID mismatch! '{actual_mapped_id}' not found in {exception_id}")
        else:
            # Convert to list if passed as string (just in case)
            exception_id = [exception_id]
            if actual_mapped_id not in exception_id:
                raise AssertionError(
                    f"Expected Nigo Exception ID mismatch! '{actual_mapped_id}' not found in {exception_id}")

        self.bi.log(f"Expected Nigo exception ID match! Found '{actual_mapped_id}' in '{exception_id}'")
        self.bi.log("-----------------------------------------------------------")
        self.bi.log_to_console(f"Expected Nigo exception ID match! Found '{actual_mapped_id}' in '{exception_id}'")
        self.bi.log_to_console("-----------------------------------------------------------")

    @keyword
    def validate_kafka_event_id(self, response, expected):
        expected_event_name = expected['expected_eventname_for_exception']
        if not expected_event_name or expected_event_name.strip() == "":
            return
        self.event_validate.validate_event_name_from_db(response, expected_event_name)

    @keyword
    def process_task_from_onbase(self, expected, nigo_id, client_code):
        onbase_nigo_id = self.raise_nigo_from_onbase(expected, nigo_id, client_code)
        task_id = self.onbase_api.create_task_on_onbase_link_with_multiple_nigos(client_code, nigo_id,
                                                                                 expected[
                                                                                     'expected_taskWVclassname'],
                                                                                 expected[
                                                                                     'expected_task_type_suitability'],
                                                                                 onbase_nigo_id[0])
        self.onbase_api.manage_task_from_onbase(client_code, task_id, expected['expected_managed_task'])
        self.resolve_nigos_from_onbase(expected, onbase_nigo_id, client_code)

        return task_id

    @keyword
    def process_nigo_from_onbase(self, expected, nigo_id, client_code):
        dtgs = expected.get('onbase_dtg', '').split(',')
        categories = expected.get('onbase_category', '').split(',')
        reasons = expected.get('onbase_nigo_reason', '').split(',')
        detail_reasons = expected.get('onbase_nigo_detail_reason', '').split(',')
        updates = expected.get('update_nigo', '').split(',')

        # Handle optional NIGO resolution and status
        statuses = expected.get('onbase_nigo_status', '').split(',')
        resolutions = expected.get('onbase_nigo_resolution', '').split(',')
        onbase_nigo_id = None

        # If there is only one DTG, make it a list to handle it in the loop as well
        if len(dtgs) == 1:
            dtgs = [dtgs[0]]
            categories = [categories[0]]
            reasons = [reasons[0]]
            detail_reasons = [detail_reasons[0]]
            updates = [updates[0]]

            # If NIGO status and resolution are not provided, skip update logic
            if not statuses[0] or not resolutions[0]:
                statuses = ['']  # Keep an empty value so the loop works
                resolutions = ['']  # Same for resolutions
        else:
            # For multiple DTGs, ensure the lists are aligned
            if len(statuses) != len(dtgs):
                statuses = statuses * len(dtgs)
            if len(resolutions) != len(dtgs):
                resolutions = resolutions * len(dtgs)

        # Loop through each DTG (whether it's one or multiple)
        for i in range(len(dtgs)):
            onbase_nigo_id = self.onbase_api.create_nigo_from_onbase(
                nigo_id,
                client_code,
                dtgs[i],
                categories[i],
                reasons[i],
                detail_reasons[i]
            )

            # If status and resolution are provided, update the NIGO
            if updates[i].upper() in ['TRUE', 'YES', '1']:
                if statuses[i] and resolutions[i]:  # Check if status and resolution are provided
                    self.onbase_api.update_nigo_from_onbase(
                        onbase_nigo_id,
                        client_code,
                        statuses[i],
                        resolutions[i]
                    )

        time.sleep(1)
        return onbase_nigo_id

    # Separate function for this
    @keyword
    def raise_nigo_from_onbase(self, expected, nigo_id, client_code):
        dtgs = expected.get('onbase_dtg', '').split(',')
        categories = expected.get('onbase_category', '').split(',')
        reasons = expected.get('onbase_nigo_reason', '').split(',')
        detail_reasons = expected.get('onbase_nigo_detail_reason', '').split(',')

        created_nigo_ids = []

        # Handle optional fields
        if len(dtgs) == 1:
            dtgs = [dtgs[0]]
            categories = [categories[0]]
            reasons = [reasons[0]]
            detail_reasons = [detail_reasons[0]]

        for i in range(len(dtgs)):
            onbase_nigo_id = self.onbase_api.create_nigo_from_onbase(
                nigo_id,
                client_code,
                dtgs[i],
                categories[i],
                reasons[i],
                detail_reasons[i]
            )
            created_nigo_ids.append(onbase_nigo_id)

        time.sleep(1)
        return created_nigo_ids

    @keyword
    def resolve_nigos_from_onbase(self, expected, nigo_ids, client_code):
        statuses = expected.get('onbase_nigo_status', '').split(',')
        resolutions = expected.get('onbase_nigo_resolution', '').split(',')

        if len(statuses) != len(nigo_ids):
            statuses = statuses * len(nigo_ids)
        if len(resolutions) != len(nigo_ids):
            resolutions = resolutions * len(nigo_ids)

        for i in range(len(nigo_ids)):
            if statuses[i] and resolutions[i]:
                self.onbase_api.update_nigo_from_onbase(
                    nigo_ids[i],
                    client_code,
                    statuses[i],
                    resolutions[i]
                )

    @keyword
    def get_status_and_task_type_from_case_detail_api(self, response_api, externalTaskId):
        specific_id = str(externalTaskId)
        task_info = {key: task[key] for task in response_api["tasks"] if task["externalTaskId"] == specific_id for key
                     in
                     ["status", "taskType"]}
        return task_info

    @keyword
    def validate_task_status_and_task_type(self, response_case_detail_api, task_id, expected_status_and_task_type_str,
                                           do_assert=False):
        time.sleep(10)

        try:
            expected_dict = ast.literal_eval(expected_status_and_task_type_str)
        except Exception as e:
            print(f"Failed to parse expected string into dict: {e}")
            return False

        actual_status_and_task_type = self.get_status_and_task_type_from_case_detail_api(response_case_detail_api,
                                                                                         task_id)

        match = str(actual_status_and_task_type) == str(expected_dict)

        if match:

            self.bi.log_to_console(
                f"✅ Match found - Actual Status and Expected Status: {actual_status_and_task_type}")
            self.bi.log_to_console(f"✅ Expected Status and Task Type: {expected_dict}")
            self.bi.log_to_console(f"✅ Actual: {actual_status_and_task_type}")
            self.bi.log_to_console(f"✅ Expected: {expected_dict}")
            self.bi.log(f"\n✅ Match found - Actual Status and Expected Status are same")
            self.bi.log(f"✅ Actual status and task type: {actual_status_and_task_type}")
            self.bi.log(f"✅ Expected status and task type: {expected_dict}")
        elif do_assert:
            # Final try with assertion if not matched
            self.bi.should_be_equal_as_strings(
                str(actual_status_and_task_type), str(expected_dict),
                f"❌ Actual: {actual_status_and_task_type} != Expected: {expected_dict}"
            )

        return match

    @keyword
    def validate_onbase_raised_nigo_status_from_case_detail_api(self, expected, response_case_detail_api):
        expected_onbase_nigo = expected['expected_onbase_nigo']
        actual_onbase_nigo = self.get_exception_category_reason_and_detailed_reason(
            response_case_detail_api
        )
        self.validate_nigo_status(expected_onbase_nigo, actual_onbase_nigo)

    @keyword
    def get_exception_category_reason_and_detailed_reason(self, response):
        category_types = ['NEW', 'RESOLVED', 'OVERRIDDEN']

        list_of_exceptions = []

        for item in response.get("exceptions", []):

            if item['status'] in category_types:
                status = item["status"]
                category = item["category"]
                reason = item["reason"]
                detailed_reason = item["detailedReason"]

                exception_dict = {
                    'status': status,
                    'category': category,
                    'reason': reason,
                    'detailedReason': detailed_reason
                }

                list_of_exceptions.append(exception_dict)

        return list_of_exceptions

    @keyword
    def validate_nigo_status(self, expected, actual_categories):
        expected = ast.literal_eval(expected)
        try:
            assert expected == actual_categories, f"Validation FAILED: Expected {expected} but got {actual_categories}"
            self.bi.log("✅ Expected and actual NIGO values are the same.\n")
            self.bi.log(f"Expected NIGO: {expected}")
            self.bi.log(f"Actual NIGO: {actual_categories}")
            self.bi.log_to_console("✅ Expected and actual NIGO values are the same.\n")
            self.bi.log_to_console(f"Expected NIGO: {expected}")
            self.bi.log_to_console(f"Actual NIGO: {actual_categories}")
        except AssertionError as e:
            print(e)

    @keyword
    def validate_task_raised_from_onbase(self, expected, response_case_detail_api, task_id, token, zl_case_id):
        expected_onbase_nigo = expected['expected_onbase_nigo']
        expected_task_status_and_type = expected['expected_task_status_and_type']
        actual_onbase_nigo = self.get_exception_category_reason_and_detailed_reason(
            response_case_detail_api
        )
        self.validate_nigo_status(expected_onbase_nigo, actual_onbase_nigo)
        self.validate_with_task_status_and_task_with_retries(
            token, zl_case_id, task_id, expected_task_status_and_type, delay_seconds=5
        )

    @keyword
    def get_status_of_tasks_present_in_case_detail(self, response):
        if 'tasks' in response and response['tasks'] is not None:
            self.bi.log_to_console("\nTask section is present in the case detail api")
            self.bi.log("\nTask section is present in the case detail api")
            return True
        else:
            self.bi.log_to_console("\nTask section is not present in the case detail api")
            self.bi.log("\nTask section is not present in the case detail api")
            self.bi.fail("Task section is missing or None in the case detail response")

    @keyword
    def validate_with_task_status_and_task_with_retries(self, token, case_id, task_id,
                                                        expected_status_and_task_type, delay_seconds=5):
        status = False
        for i in range(5):
            is_last_try = i == 4
            response = self.get_response_from_case_detail_api(token, case_id)
            status = self.validate_task_status_and_task_type(
                response, task_id, expected_status_and_task_type, do_assert=is_last_try
            )
            if status:
                break
            if not status and not is_last_try:
                time.sleep(delay_seconds)
        return status

    @keyword
    def validate_suitability_task_status_and_queuename(self, client_code, case_id_for_nigo, token, expected,
                                                       zl_case_id):

        def get_expected(key):
            value = expected.get(key, '')
            return value.strip() if isinstance(value, str) else value

        # Step 0: Process NIGO if required inputs are present
        if any(get_expected(k) for k in ['onbase_dtg', 'onbase_category', 'onbase_nigo_reason']):
            onbase_nigo_id = self.process_nigo_from_onbase(expected, case_id_for_nigo, client_code)
        else:
            onbase_nigo_id = None

        # Step 1: Create Task
        task_wv_classname = get_expected('expected_taskWVclassname')
        task_type_suitability = get_expected('expected_task_type_suitability')
        if task_wv_classname and task_type_suitability:
            task_id = self.onbase_api.create_task_on_onbase_link_with_multiple_nigos(
                client_code, case_id_for_nigo, task_wv_classname, task_type_suitability, onbase_nigo_id
            )

        else:
            self.bi.log("Skipping task creation — expected_taskWVclassname or expected_task_type_suitability not provided.")
            return

        # Step 2: Add/Update Case Attributes
        attribute_key = get_expected('attribute_key')
        attribute_value = get_expected('attribute_value')
        if task_wv_classname and attribute_key and attribute_value:
            self.onbase_api.add_update_case_or_task_attributes(
                client_code, task_wv_classname, task_id, attribute_key, attribute_value
            )

        # Step 3: Manage Task
        managed_task = get_expected("expected_managed_task")
        if managed_task:
            self.onbase_api.manage_task_from_onbase(client_code, task_id, managed_task)

        # Step 4 & 5: Find task attributes and validate
        if task_wv_classname:
            find_tasks_attributes_response = self.onbase_api.find_tasks_attributes(client_code, task_id,
                                                                                   task_wv_classname)
            actual_queuename_and_suitability_status = self.get_queuename_and_suitability_status(
                find_tasks_attributes_response
            )

            expected_queuename_and_suitability_status = expected.get("expected_queuename_and_suitability_status")

            if expected_queuename_and_suitability_status:
                # Convert from string to dict if necessary
                if isinstance(expected_queuename_and_suitability_status, str):
                    try:
                        expected_queuename_and_suitability_status = ast.literal_eval(
                            expected_queuename_and_suitability_status)
                    except (ValueError, SyntaxError):
                        raise ValueError(
                            "Failed to parse expected_queuename_and_suitability_status as a Python dict string.")

                self.bi.log(f"Actual QueueName/Suitability: {actual_queuename_and_suitability_status}")
                self.bi.log(f"Expected QueueName/Suitability: {expected_queuename_and_suitability_status}")
                self.bi.log_to_console(f"Actual QueueName/Suitability: {actual_queuename_and_suitability_status}")
                self.bi.log_to_console(f"Expected QueueName/Suitability: {expected_queuename_and_suitability_status}")

                assert actual_queuename_and_suitability_status == expected_queuename_and_suitability_status, \
                    f"Mismatch!\nActual: {actual_queuename_and_suitability_status}\nExpected: {expected_queuename_and_suitability_status}"
            else:
                self.bi.log(
                    "Skipping queue/suitability assertion — expected_queuename_and_suitability_status not provided.")

        # Step 6: Validate task status
        expected_task_status_and_type = get_expected("expected_task_status_and_type")
        if expected_task_status_and_type:
            self.validate_with_task_status_and_task_with_retries(
                token, zl_case_id, task_id, expected_task_status_and_type, delay_seconds=5
            )
        else:
            self.bi.log("Skipping task status validation — expected_task_status_and_type not provided.")

    @keyword
    def get_queuename_and_suitability_status(self, response):
        results = {}

        def search_keys(api_response):
            if isinstance(api_response, dict):
                for key, value in api_response.items():
                    if key == 'queueName' or key == 'suitabilityStatus':
                        results[key] = value
                    elif isinstance(value, (dict, list)):
                        search_keys(value)
            elif isinstance(api_response, list):
                for item in api_response:
                    search_keys(item)

        search_keys(response)
        return results

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
                self.bi.log_to_console("Both expected documents found! NB Purchase w App and Attachments found!")
                break
            else:
                attempts += 1
                if attempts >= max_attempts:
                    self.bi.log_to_console("Timeout! Expected documents not found after 10 minutes. Exiting.")
                    break
                self.bi.log_to_console(
                    f"Attempt {attempts}/{max_attempts}: Expected documents not found. Retrying in 2 minutes...")
                time.sleep(120)

    @keyword
    def get_exception_id_case_detail_api_response(self, response, expected):
        matching_id = next((
            int(exception["externalId"])
            for exception in response.get("exceptions", [])
            if exception.get("category") == expected.get('onbase_category')
               and exception.get("reason") == expected.get('onbase_nigo_reason')
               and exception.get("detailedReason") == expected.get('onbase_nigo_detail_reason')
               and "externalId" in exception
        ), None)
        assert matching_id is not None, "No exception matched the given criteria"
        return matching_id

    @keyword
    def event_validation(self, response, expected, client_code, flow_type, company_hierarchy_id, policy_no):
        if flow_type == 'resolve_nigo_created_from_dtcc':
            exception_id = self.get_exception_id_case_detail_api_response(response, expected)
            self.onbase_api.update_nigo_from_onbase(exception_id, client_code, expected.get('onbase_nigo_status'),
                                                    expected.get('onbase_nigo_resolution'))
            time.sleep(5)


        elif flow_type == 'case_status_changed_from_lifecad':
            lc_username = self.read_config.get_encrypt_value_by_key('LCTokenUser')
            lc_password = self.read_config.get_encrypt_value_by_key('LCTokenPassword')
            status = self.lifecad_api.update_contract_status_from_lifecad(lc_username, lc_password,
                                                                          company_hierarchy_id, policy_no)
            if status.get('newStatusCode') == 'W':
                self.bi.log("Status updated to CANCELLED")
                self.bi.log_to_console("Status updated to CANCELLED")

    @keyword
    def get_normalized_inputs(self, test_id, client, automation_flow):
        return (
            self.file.normalize_input_value(test_id),
            self.file.normalize_input_value(client),
            self.file.normalize_input_value(automation_flow)
        )

    @keyword
    def dispatch_flow_handler(self, flow_type, context):
        flow_handlers = {
            'task_validation': self.process_task_validation_flow,
            'nigo_raise_from_onbase': self.process_nigo_raise_from_onbase_flow
        }
        handler = flow_handlers.get(flow_type)
        if handler:
            handler(context)

    @keyword
    def process_task_validation_flow(self, context):
        self.task_id = self.process_task_from_onbase(
            context['expected'], context['nigo_id'], context['client_code']
        )

    @keyword
    def process_nigo_raise_from_onbase_flow(self, context):
        self.process_nigo_from_onbase(
            context['expected'], context['nigo_id'], context['client_code']
        )

    @keyword
    def run_case_overview_validation(self, expected, token, zl_case_id):
        return self.validate_case_overview_status(
            expected.get('expected_case_overview'),
            token,
            zl_case_id,
            expected.get('expected_stage_status'),
            expected.get('stage_id')
        )

    @keyword
    def run_flow_specific_validations(self, flow_type, context):
        expected = context['expected']
        response = context['response']
        token = context['token']
        zl_case_id = context['zl_case_id']
        client_code = context['client_code']
        nigo_id = context['nigo_id']

        self.event_validation(
            response, expected, client_code, flow_type,
            context['company_hierarchy_id'], context['policy_no']
        )

        if flow_type == 'task_status':
            self.get_status_of_tasks_present_in_case_detail(response)
            if expected.get('expected_taskWVclassname'):
                self.validate_suitability_task_status_and_queuename(
                    client_code, nigo_id, token, expected, zl_case_id
                )

        elif flow_type == 'nigo_raise_from_onbase':
            self.validate_onbase_raised_nigo_status_from_case_detail_api(expected, response)

        elif flow_type == 'task_validation':
            self.validate_task_raised_from_onbase(
                expected, response, self.task_id, token, zl_case_id
            )

    @keyword
    def run_step_status_validation(self, token, zl_case_id, expected):
        self.validate_all_steps(
            token, zl_case_id, expected.get('stage_id'), expected.get('expected_step_status')
        )

    @keyword
    def run_nigo_exception_validation_if_needed(self, context):
        test_case_id = context['test_case_id']
        response = context['response']
        expected = context['expected']
        case_status = self.generate_dtcc.check_case_status_from_excel(test_case_id)

        if case_status == 'NIGO':
            exception_id, mapped_id = self.validate_nigo_cases(
                response,
                expected.get('stage_id'),
                expected.get('expected_exception'),
                expected.get('expected_exception_mapped_step')
            )
            self.validate_nigo_exception_ids(exception_id, mapped_id)
