from robot.api.deco import library, keyword
from resources.keywords.helper_keywords.ZinniaLiveHelper import ZinniaLiveHelper
from resources.utilities.ExcelUtilities import ExcelUtilities
from resources.utilities.FileUtils import FileUtils
from resources.keywords.api_keywords.QueueManagementApi import QueueManagementApi


@library
class ZinniaLiveValidation:
    def __init__(self):
        self.zl_validation = ZinniaLiveHelper()
        self.excel = ExcelUtilities()
        self.file = FileUtils()
        self.zl_queue_management = QueueManagementApi()
        self.task_id = None

    @keyword
    def validate_zinnia_live_case_flow(self, test_id, client, automation_flow, company_hierarchy_id):
        test_case_id, client_code, flow_type = self.zl_validation.get_normalized_inputs(test_id, client, automation_flow)
        token = self.zl_validation.authenticate_user_and_get_token()
        expected = self.excel.get_expected_data_by_test_case_id(test_case_id)

        zl_case_id, nigo_id, policy_no = self.zl_validation.get_caseid_from_case_management_api(token, test_case_id)

        context = {
            'test_case_id': test_case_id,
            'client_code': client_code,
            'flow_type': flow_type,
            'company_hierarchy_id': company_hierarchy_id,
            'expected': expected,
            'nigo_id': nigo_id,
            'policy_no': policy_no,
            'zl_case_id': zl_case_id,
            'token': token
        }

        self.zl_validation.dispatch_flow_handler(flow_type, context)

        response = self.zl_validation.run_case_overview_validation(expected, token, zl_case_id)
        context['response'] = response

        self.zl_validation.run_flow_specific_validations(flow_type, context)
        self.zl_validation.run_step_status_validation(token, zl_case_id, expected)

        self.zl_queue_management.queue_management_process(flow_type)
        self.zl_validation.run_nigo_exception_validation_if_needed(context)
        self.zl_validation.validate_kafka_event_id(context['response'],expected)

