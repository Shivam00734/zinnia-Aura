import time
import pandas as pd
from robot.api.deco import keyword, library
from robot.libraries.BuiltIn import BuiltIn
from SeleniumLibrary import SeleniumLibrary
from resources.keywords.core_logic_keywords.EappValidation import EappValidation
from resources.keywords.data_creation_keywords.GenerateAttachment import GenerateAttachment
from resources.keywords.data_creation_keywords.GenerateDTCC import GenerateDTCC
from resources.utilities.ExcelUtilities import ExcelUtilities
from resources.utilities.FileUtils import FileUtils
from resources.utilities.ReadConfig import ReadConfig
from resources.vo.FilePropertiesVo import FilePropertiesVo

@library
class EappHelper:
    url = "http://sbtopetpapp01q/etpweb/Forms/frmEAPP.aspx"
    browser = "headlesschrome"
    excel = ExcelUtilities()
    file = FileUtils()
    read_config = ReadConfig()
    Eapp_helper = EappValidation()
    selenium = SeleniumLibrary()
    attachment_generator = GenerateAttachment()
    fileProperties = FilePropertiesVo()
    generate_dtcc = GenerateDTCC()
    contract_number_dict = {}

    def __init__(self):
        self.selLib = BuiltIn().get_library_instance("SeleniumLibrary")

    @keyword
    def get_dtcc_output_sheet(self, input_text):
        text_to_path_mapping = {
            "Output_data": 'output_data',
        }
        return text_to_path_mapping.get(input_text, "Invalid input")

    @keyword
    def validate_etp_and_get_contract_number(self):
        global row_count
        sheet_name = self.get_dtcc_output_sheet("Output_data")
        excel_sheet_path = self.read_config.getValueByKey('ZinniaLiveTestDataND')
        self.Eapp_helper.open_browser_with_ETP_Dashboard_url(EappHelper.url, EappHelper.browser)
        self.process_test_cases_etp_validation(excel_sheet_path, sheet_name)


    @keyword
    def process_test_cases_etp_validation(self, file_path, sheet_name):

        data = pd.read_excel(file_path, sheet_name=sheet_name)

        test_case_col = '${test_case_id}'
        company_col = '${company_name}'
        date_col = '${dtcc_file_creation_date}'
        app_control_col = '${app_control_number}'
        required_flag_col = '${dtcc_required}'


        required_columns = [test_case_col, company_col, date_col, app_control_col, required_flag_col]
        for col in required_columns:
            if col not in data.columns:
                raise KeyError(f"[ERROR] Required column '{col}' not found in the Excel sheet")


        filtered_data = data[data[required_flag_col].astype(str).str.strip().str.upper() == "YES"]


        if filtered_data.empty:
            print("[INFO] No rows found where dtcc_required == 'YES'. Skipping processing.")
            return


        test_case_ids = filtered_data[test_case_col].dropna().tolist()

        for test_case_id in test_case_ids:
            try:

                row = filtered_data[filtered_data[test_case_col] == test_case_id].iloc[0]
            except IndexError:
                print(f"[WARNING] No row found for test case ID: {test_case_id}")
                continue

            try:

                company_name = row[company_col]
                contract_created_date = row[date_col]
                application_control_number = row[app_control_col]


                self.Eapp_helper.enter_the_contract_create_date(contract_created_date)
                self.Eapp_helper.choose_company_name(company_name)
                self.Eapp_helper.select_no_of_records_from_dropdown()
                self.Eapp_helper.click_on_refresh_button()
            except Exception as e:
                print(f"[ERROR] UI interaction failed for test case {test_case_id}: {e}")
                continue

            try:

                assert application_control_number is not None, f"App control number is missing for test case {test_case_id}"
            except AssertionError as ae:
                print(f"[ASSERT FAIL] {ae}")
                continue

            try:

                time.sleep(0.5)
                self.get_actual_ETP_info_and_save_in_excel(application_control_number, test_case_id, file_path)
            except AssertionError as ae:
                print(f"[ASSERT FAIL] {ae}")

    @keyword
    def get_actual_etp_information(self, app_control_number, test_case_id):
        return self.get_etp_info_from_etp_dashboard(app_control_number, test_case_id)

    @keyword
    def get_etp_info_from_etp_dashboard(self, app_control_number, test_case_id):
        actual_etp_info = self.Eapp_helper.get_actual_ETP_info(app_control_number, test_case_id)
        self.selenium.close_browser()
        return actual_etp_info

    @keyword
    def get_actual_ETP_info_and_save_in_excel(self, app_control_number, test_case_id, file_path):
        actual_contract_info = self.Eapp_helper.get_actual_ETP_info(app_control_number, test_case_id)
        time.sleep(0.5)
        contract_number = actual_contract_info.get('contract_number')

        time.sleep(0.5)
        self.contract_number_dict[test_case_id] = contract_number

        self.excel.write_value_to_excel_by_column_name(file_path, self.generate_dtcc.excel_output_sheet_name,
                                                       test_case_id,
                                                       '${contract_number}',
                                                       contract_number)

    @keyword
    def validate_etp_and_upload_attachment(self):
        time.sleep(300)
        EappHelper.validate_etp_and_get_contract_number(self)
        self.attachment_generator.verify_creation_of_nb_application_case_in_onbase_and_upload_xml_file_and_attachment(
            self.contract_number_dict)
        time.sleep(600)


