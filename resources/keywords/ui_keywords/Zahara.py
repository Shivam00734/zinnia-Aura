from robot.api.deco import keyword, library
from robot.libraries.BuiltIn import BuiltIn
from resources.locators import ZinniaLive_web_locators
from resources.keywords.api_keywords.ZaharaApi import ZaharaApi
from resources.keywords.core_logic_keywords.AccordeXmlUpdate import AccordeXmlUpdate
from resources.locators import ZaharaLocators
from resources.utilities.ExcelUtilities import ExcelUtilities
from resources.utilities.FileUtils import FileUtils
from resources.utilities.ReadConfig import ReadConfig
from resources.utilities.WebUtils import WebUtils
import pyautogui
from resources.locators import ZaharaLocators
from resources.vo.FilePropertiesVo import FilePropertiesVo

# from resources.Reporting.ReportingSetup import ReportingSetup


@library
class Zahara:
    url = "https://qa-zahara-ui.zinnia.io/#/app/policy"
    # browser = "headlesschrome"
    browser = "chrome"
    webutils = WebUtils()
    excel = ExcelUtilities()
    xml_updater  = AccordeXmlUpdate()
    read_config = ReadConfig()
    fileProperties = FilePropertiesVo()
    file = FileUtils()
    zahara_api  = ZaharaApi()

    @keyword
    def validate_policy_status(self, expected_policy_status):
        locator = ZaharaLocators.validate_policy_active_txt.format(expected_policy_status)
        
        # Try to wait for the expected status with retry logic
        max_retries = 4
        retry_interval = 30  # seconds
        
        for retry in range(max_retries):
            try:
                BuiltIn().log(f"Attempt {retry + 1}/{max_retries}: Waiting for policy status '{expected_policy_status}'")
                BuiltIn().log_to_console(f"Attempt {retry + 1}/{max_retries}: Waiting for policy status '{expected_policy_status}'")
                
                self.webutils.wait_until_element_visible(locator, timeout=retry_interval)
                actual_policy_status = self.webutils.get_text(locator)
                
                if expected_policy_status == actual_policy_status:
                    BuiltIn().log(f"The policy has been successfully created and activated on Zahara")
                    BuiltIn().log(f"The policy has been successfully created and activated on Zahara")
                    return
                else:
                    BuiltIn().log(f"Status mismatch - Expected: '{expected_policy_status}', Actual: '{actual_policy_status}'")
                    BuiltIn().log_to_console(f"Status mismatch - Expected: '{expected_policy_status}', Actual: '{actual_policy_status}'")
                    
            except Exception as e:
                BuiltIn().log(f"Attempt {retry + 1} failed: {str(e)}")
                BuiltIn().log_to_console(f"Attempt {retry + 1} failed: {str(e)}")
                
                # Log current page status for debugging
                try:
                    # Try to find any status-related elements for debugging
                    status_elements = self.webutils.get_all_text_elements_containing("status", case_sensitive=False)
                    if status_elements:
                        BuiltIn().log(f"Current status elements found: {status_elements}")
                        BuiltIn().log_to_console(f"Current status elements found: {status_elements}")
                except:
                    pass
                
                if retry < max_retries - 1:  # Don't refresh on the last attempt
                    BuiltIn().log("Refreshing page and retrying...")
                    BuiltIn().log_to_console("Refreshing page and retrying...")
                    self.webutils.wait_and_click(ZaharaLocators.zahara_refresh_btn)
                    self.webutils.sleep_time(10)  # Wait for page to refresh
        
        # If we get here, all retries failed
        raise AssertionError(
            f"Policy creation or activation failed on Zahara. Expected status '{expected_policy_status}' not found after {max_retries} attempts.")


    @keyword
    def create_policy(self, old_xml_name, expect_poly_status, client, client_plan_code):
        BuiltIn().log("Perform Policy Creation Process")
        BuiltIn().log_to_console("Perform Policy Creation Process")
        BuiltIn().log("-----------------------------------------------------------")
        BuiltIn().log_to_console("-----------------------------------------------------------")

        old_xml_file_name = self.file.normalize_input_value(old_xml_name)
        expected_policy_status = self.file.normalize_input_value(expect_poly_status)

        self.webutils.open_browser_with_url(Zahara.url, Zahara.browser)
        user_id = self.read_config.getValueByKey('zinnia_live_user_email')
        self.webutils.wait_and_input_text(ZinniaLive_web_locators.zl_user_input, user_id)
        self.webutils.wait_and_click(ZinniaLive_web_locators.zl_user_submit_btn)
        self.webutils.sleep_time(3)

        if self.webutils.is_element_visible(ZinniaLive_web_locators.zl_user_pass_input):
            user_pass = self.read_config.getValueByKey('zinnia_live_pass')
            self.webutils.wait_and_input_text(ZinniaLive_web_locators.zl_user_pass_input, user_pass)
            self.webutils.wait_and_click(ZinniaLive_web_locators.zl_user_pass_submit_btn)

        new_policy_number, payee_name = self.create_policy_on_zahara(old_xml_file_name, expected_policy_status, client, client_plan_code)
        return new_policy_number, payee_name

    @keyword
    def login_to_zahara_and_perform_transaction_process(self, policy_number, client_plan_code, expected_policy_status_code):
        self.webutils.open_browser_with_url(Zahara.url, Zahara.browser)
        user_id = self.read_config.getValueByKey('zinnia_live_user_email')
        self.webutils.wait_and_input_text(ZinniaLive_web_locators.zl_user_input, user_id)
        self.webutils.wait_and_click(ZinniaLive_web_locators.zl_user_submit_btn)
        self.webutils.sleep_time(3)

        if self.webutils.is_element_visible(ZinniaLive_web_locators.zl_user_pass_input):
            user_pass = self.read_config.getValueByKey('zinnia_live_pass')
            self.webutils.wait_and_input_text(ZinniaLive_web_locators.zl_user_pass_input, user_pass)
            self.webutils.wait_and_click(ZinniaLive_web_locators.zl_user_pass_submit_btn)

        self.perform_multi_phone_change_transaction(policy_number, client_plan_code, expected_policy_status_code)

    @keyword
    def login_to_zahara_and_perform_multi_email_change_transaction_process(self, policy_number, client_plan_code, expected_policy_status_code):
        self.webutils.open_browser_with_url(Zahara.url, Zahara.browser)
        user_id = self.read_config.getValueByKey('zinnia_live_user_email')
        self.webutils.wait_and_input_text(ZinniaLive_web_locators.zl_user_input, user_id)
        self.webutils.wait_and_click(ZinniaLive_web_locators.zl_user_submit_btn)
        self.webutils.sleep_time(3)

        if self.webutils.is_element_visible(ZinniaLive_web_locators.zl_user_pass_input):
            user_pass = self.read_config.getValueByKey('zinnia_live_pass')
            self.webutils.wait_and_input_text(ZinniaLive_web_locators.zl_user_pass_input, user_pass)
            self.webutils.wait_and_click(ZinniaLive_web_locators.zl_user_pass_submit_btn)

        self.perform_multi_email_change_transaction(policy_number, client_plan_code, expected_policy_status_code)






    @keyword
    def create_policy_for_specific_client(self, old_xml_name, expect_poly_status, client, client_plan_code, client_tran_initiate_date, client_life_cycle_date, validate_client_effe_date):
        BuiltIn().log("Perform Policy Creation Process")
        BuiltIn().log_to_console("Perform Policy Creation Process")
        BuiltIn().log("-----------------------------------------------------------")
        BuiltIn().log_to_console("-----------------------------------------------------------")

        old_xml_file_name = self.file.normalize_input_value(old_xml_name)
        expected_policy_status = self.file.normalize_input_value(expect_poly_status)

        self.webutils.open_browser_with_url(Zahara.url, Zahara.browser)
        user_id = self.read_config.getValueByKey('zinnia_live_user_email')
        self.webutils.wait_and_input_text(ZinniaLive_web_locators.zl_user_input, user_id)
        self.webutils.wait_and_click(ZinniaLive_web_locators.zl_user_submit_btn)
        self.webutils.sleep_time(3)

        if self.webutils.is_element_visible(ZinniaLive_web_locators.zl_user_pass_input):
            user_pass = self.read_config.getValueByKey('zinnia_live_pass')
            self.webutils.wait_and_input_text(ZinniaLive_web_locators.zl_user_pass_input, user_pass)
            self.webutils.wait_and_click(ZinniaLive_web_locators.zl_user_pass_submit_btn)

        new_policy_number, payee_name = self.create_policy_on_zahara_with_effective_date_client_specific(old_xml_file_name, expected_policy_status, client, client_plan_code, client_tran_initiate_date, client_life_cycle_date, validate_client_effe_date)
        return new_policy_number, payee_name

    @keyword
    def create_policy_with_effective_date(self, old_xml_name, expect_poly_status, client, plan_code):
        BuiltIn().log("Perform Policy Creation Process")
        BuiltIn().log_to_console("Perform Policy Creation Process")
        BuiltIn().log("-----------------------------------------------------------")
        BuiltIn().log_to_console("-----------------------------------------------------------")

        old_xml_file_name = self.file.normalize_input_value(old_xml_name)
        expected_policy_status = self.file.normalize_input_value(expect_poly_status)

        self.webutils.open_browser_with_url(Zahara.url, Zahara.browser)
        user_id = self.read_config.getValueByKey('zinnia_live_user_email')
        self.webutils.wait_and_input_text(ZinniaLive_web_locators.zl_user_input, user_id)
        self.webutils.wait_and_click(ZinniaLive_web_locators.zl_user_submit_btn)
        self.webutils.sleep_time(3)

        if self.webutils.is_element_visible(ZinniaLive_web_locators.zl_user_pass_input):
            user_pass = self.read_config.getValueByKey('zinnia_live_pass')
            self.webutils.wait_and_input_text(ZinniaLive_web_locators.zl_user_pass_input, user_pass)
            self.webutils.wait_and_click(ZinniaLive_web_locators.zl_user_pass_submit_btn)

        new_policy_number, payee_name = self.create_policy_on_zahara_with_effective_date(old_xml_file_name, expected_policy_status, client, plan_code)
        return new_policy_number, payee_name

    @keyword
    def create_policy_on_zahara(self, old_xml_file_name, expected_policy_status_code, client_code, plan_code):
        expected_policy_status = self.file.normalize_input_value(expected_policy_status_code)
        client = self.file.normalize_input_value(client_code)
        client_plan_code = self.file.normalize_input_value(plan_code)

        new_policy_number = None
        payee_name = None

        self.webutils.sleep_time(15)

        if client in ["Everly"]:
            new_policy_number, payee_name, updated_xml_content = self.xml_updater.generate_new_policy_xml_everly_client(
                old_xml_file_name)
            self.xml_updater.upload_policy(updated_xml_content)

        elif client in ["WELB"]:
            new_policy_number, payee_name, updated_xml_content = self.xml_updater.generate_new_policy_xml_welb_client(
                old_xml_file_name)
            self.xml_updater.upload_policy(updated_xml_content)

        self.webutils.sleep_time(10)
        self.webutils.wait_and_click(ZaharaLocators.refresh_btn)
        self.webutils.wait_and_input_text(ZaharaLocators.search_input, new_policy_number)
        self.webutils.wait_and_click(ZaharaLocators.search_result_xpath.format(doc_number=new_policy_number))
        self.webutils.wait_and_click(ZaharaLocators.trans_summary_tab)

        if client in ["Everly"]:
            lifecycle_date = "2025-02-04"
            self.zahara_api.call_lifecycle_api(new_policy_number, lifecycle_date, client_plan_code)
            self.webutils.wait_and_click(ZaharaLocators.trans_summary_tab)
            self.webutils.sleep_time(5)
            self.webutils.wait_and_click(ZaharaLocators.zahara_refresh_btn)
            self.validate_policy_status(expected_policy_status)

            self.webutils.sleep_time(480)
            lifecycle_date_validate = "02/04/2025"
            locator = ZaharaLocators.validate_lifecycle_update_date.format(lifecycle_date_validate)
            refresh_btn_locator = ZaharaLocators.zahara_refresh_btn
            self.webutils.wait_until_element_visible_with_retries(locator, 25, 30, refresh_btn_locator)

        elif client in ["WELB"]:
            xml_effective_date = "2025-02-04"
            self.zahara_api.initiate_transaction_on_zahara(new_policy_number, xml_effective_date, client_plan_code)

            self.webutils.sleep_time(10)
            lifecycle_date = "2025-02-04"
            self.zahara_api.call_lifecycle_api(new_policy_number, lifecycle_date, client_plan_code)
            self.webutils.wait_and_click(ZaharaLocators.trans_summary_tab)
            self.webutils.sleep_time(5)
            self.webutils.wait_and_click(ZaharaLocators.zahara_refresh_btn)
            self.validate_policy_status(expected_policy_status)

            self.webutils.sleep_time(60)
            lifecycle_date_validate = "04/02/2025"
            locator = ZaharaLocators.validate_lifecycle_update_date.format(lifecycle_date_validate)
            refresh_btn_locator = ZaharaLocators.zahara_refresh_btn
            self.webutils.wait_until_element_visible_with_retries(locator, 39, 30, refresh_btn_locator)

            self.webutils.sleep_time(10)
            custom_lifecycle_date = "2026-02-01"
            self.process_lifecycle_for_systematic_withdrawal_processing_after_transaction_initiate(new_policy_number,
                                                                                                          custom_lifecycle_date,
                                                                                                          client_plan_code)

            self.webutils.sleep_time(300)
            lifecycle_date_validate = "02/01/2026"
            locator = ZaharaLocators.validate_lifecycle_effective_date.format(lifecycle_date_validate)
            refresh_btn_locator = ZaharaLocators.zahara_refresh_btn
            self.webutils.wait_until_element_visible_with_retries(locator, 29, 30, refresh_btn_locator)

        self.webutils.close_browser()
        return new_policy_number, payee_name


    @keyword
    def perform_multi_phone_change_transaction(self, policy_number, client_plan_code, expected_policy_status_code):
        expected_policy_status = self.file.normalize_input_value(expected_policy_status_code)

        self.webutils.wait_and_click(ZaharaLocators.refresh_btn)
        self.webutils.wait_and_input_text(ZaharaLocators.search_input, policy_number)
        self.webutils.wait_and_click(ZaharaLocators.search_result_xpath.format(doc_number=policy_number))
        self.webutils.wait_and_click(ZaharaLocators.trans_summary_tab)

        lifecycle_date = self.file.get_cst_date("%Y-%m-%d")
        self.zahara_api.call_lifecycle_api(policy_number, lifecycle_date, client_plan_code)
        self.webutils.wait_and_click(ZaharaLocators.trans_summary_tab)
        self.webutils.sleep_time(5)
        self.webutils.wait_and_click(ZaharaLocators.zahara_refresh_btn)
        self.validate_policy_status(expected_policy_status)

        self.webutils.sleep_time(5)
        lifecycle_date_validate = self.file.get_current_date_format_windows_with_two_digit()
        locator = ZaharaLocators.validate_lifecycle_update_date.format(lifecycle_date_validate)
        refresh_btn_locator = ZaharaLocators.zahara_refresh_btn
        self.webutils.wait_until_element_visible_with_retries(locator, 25, 30, refresh_btn_locator)

        self.webutils.close_browser()

    @keyword
    def perform_multi_email_change_transaction(self, policy_number, client_plan_code, expected_policy_status_code):
        expected_policy_status = self.file.normalize_input_value(expected_policy_status_code)

        self.webutils.wait_and_click(ZaharaLocators.refresh_btn)
        self.webutils.wait_and_input_text(ZaharaLocators.search_input, policy_number)
        self.webutils.wait_and_click(ZaharaLocators.search_result_xpath.format(doc_number=policy_number))
        self.webutils.wait_and_click(ZaharaLocators.trans_summary_tab)


        lifecycle_date = self.file.get_cst_date("%Y-%m-%d")
        self.zahara_api.call_lifecycle_api(policy_number, lifecycle_date, client_plan_code)
        self.webutils.wait_and_click(ZaharaLocators.trans_summary_tab)
        self.webutils.sleep_time(5)
        self.webutils.wait_and_click(ZaharaLocators.zahara_refresh_btn)
        self.validate_policy_status(expected_policy_status)

        self.webutils.sleep_time(5)
        lifecycle_date_validate = self.file.get_current_date_format_windows_with_two_digit()
        locator = ZaharaLocators.validate_lifecycle_update_date.format(lifecycle_date_validate)
        refresh_btn_locator = ZaharaLocators.zahara_refresh_btn
        self.webutils.wait_until_element_visible_with_retries(locator, 25, 30, refresh_btn_locator)

        self.webutils.close_browser()


    @keyword
    def create_policy_on_zahara_with_effective_date(self, old_xml_file_name, expected_policy_status_code, client_id, plan_code):
        expected_policy_status = self.file.normalize_input_value(expected_policy_status_code)
        client = self.file.normalize_input_value(client_id)
        client_plan_code = self.file.normalize_input_value(plan_code)

        new_policy_number = None
        payee_name = None

        self.webutils.sleep_time(15)

        if client in ["Everly", "Farmer"]:
            new_policy_number, payee_name, updated_xml_content = self.xml_updater.generate_new_policy_xml_everly_client(
                old_xml_file_name)
            self.xml_updater.upload_policy(updated_xml_content)

        elif client in ["WELB"]:
            new_policy_number, payee_name, updated_xml_content = self.xml_updater.generate_new_policy_xml_welb_client(
                old_xml_file_name)
            self.xml_updater.upload_policy(updated_xml_content)

        self.webutils.sleep_time(8)
        self.webutils.wait_and_click(ZaharaLocators.refresh_btn)
        self.webutils.sleep_time(10)
        self.webutils.wait_and_input_text(ZaharaLocators.search_input, new_policy_number)
        self.webutils.wait_and_click(ZaharaLocators.search_result_xpath.format(doc_number=new_policy_number))
        self.webutils.wait_and_click(ZaharaLocators.trans_summary_tab)

        if client in ["WELB"]:
            xml_effective_date = "2024-01-02"
            self.zahara_api.initiate_transaction_on_zahara(new_policy_number, xml_effective_date, client_plan_code)

            self.webutils.sleep_time(10)
            lifecycle_date = "2024-02-01"
            self.zahara_api.call_lifecycle_api(new_policy_number, lifecycle_date, client_plan_code)

            self.webutils.sleep_time(10)
            self.webutils.wait_and_click(ZaharaLocators.zahara_refresh_btn)
            self.validate_policy_status(expected_policy_status)

            self.webutils.sleep_time(60)
            lifecycle_date_validate = "01/02/2024"
            locator = ZaharaLocators.validate_lifecycle_effective_date.format(lifecycle_date_validate)
            refresh_btn_locator = ZaharaLocators.zahara_refresh_btn
            self.webutils.wait_until_element_visible_with_retries(locator, 39, 30, refresh_btn_locator)


        elif client in ["Everly"]:
            self.webutils.sleep_time(10)
            lifecycle_date = "2024-01-01"
            self.zahara_api.call_lifecycle_api(new_policy_number, lifecycle_date, client_plan_code)

            self.webutils.sleep_time(10)
            self.webutils.wait_and_click(ZaharaLocators.zahara_refresh_btn)
            self.validate_policy_status(expected_policy_status)

            self.webutils.sleep_time(480)
            lifecycle_date_validate = "01/01/2024"
            locator = ZaharaLocators.validate_lifecycle_update_date.format(lifecycle_date_validate)
            refresh_btn_locator = ZaharaLocators.zahara_refresh_btn
            self.webutils.wait_until_element_visible_with_retries(locator, 25, 30, refresh_btn_locator)

        elif client in ["Farmer"]:
            self.webutils.sleep_time(10)
            lifecycle_date = "2026-03-20"
            self.zahara_api.call_lifecycle_api(new_policy_number, lifecycle_date, client_plan_code)

            self.webutils.sleep_time(15)
            self.webutils.wait_and_click(ZaharaLocators.zahara_refresh_btn)
            self.validate_policy_status(expected_policy_status)

            self.webutils.sleep_time(5)
            lifecycle_date_validate = "04/20/2025"
            locator = ZaharaLocators.validate_lifecycle_update_date.format(lifecycle_date_validate)
            refresh_btn_locator = ZaharaLocators.zahara_refresh_btn
            self.webutils.wait_until_element_visible_with_retries(locator, 25, 30, refresh_btn_locator)

        self.webutils.close_browser()
        return new_policy_number, payee_name

    @keyword
    def create_policy_on_zahara_with_effective_date_client_specific(self, old_xml_file_name, expected_policy_status_code, client_id, plan_code, client_tran_initiate_date, client_life_cycle_date, validate_client_effe_date):
        expected_policy_status = self.file.normalize_input_value(expected_policy_status_code)
        client = self.file.normalize_input_value(client_id)
        client_plan_code = self.file.normalize_input_value(plan_code)

        new_policy_number = None
        payee_name = None

        self.webutils.sleep_time(15)


        if client in ["Everly"]:
            new_policy_number, payee_name, updated_xml_content = self.xml_updater.generate_new_policy_xml_everly_client(
                old_xml_file_name)
            self.xml_updater.upload_policy(updated_xml_content)

        elif client in ["WELB"]:
            new_policy_number, payee_name, updated_xml_content = self.xml_updater.generate_new_policy_xml_welb_client(
                old_xml_file_name)
            self.xml_updater.upload_policy(updated_xml_content)

        self.webutils.sleep_time(5)
        self.webutils.wait_and_click(ZaharaLocators.refresh_btn)
        self.webutils.sleep_time(10)
        self.webutils.wait_and_input_text(ZaharaLocators.search_input, new_policy_number)
        self.webutils.wait_and_click(ZaharaLocators.search_result_xpath.format(doc_number=new_policy_number))
        self.webutils.wait_and_click(ZaharaLocators.trans_summary_tab)

        if client in ["WELB"]:
            self.zahara_api.initiate_transaction_on_zahara(new_policy_number, client_tran_initiate_date, client_plan_code)

            self.webutils.sleep_time(10)
            self.zahara_api.call_lifecycle_api(new_policy_number, client_life_cycle_date, client_plan_code)

            self.webutils.sleep_time(10)
            self.webutils.wait_and_click(ZaharaLocators.zahara_refresh_btn)
            self.validate_policy_status(expected_policy_status)

            self.webutils.sleep_time(60)
            locator = ZaharaLocators.validate_lifecycle_effective_date.format(validate_client_effe_date)
            refresh_btn_locator = ZaharaLocators.zahara_refresh_btn
            self.webutils.wait_until_element_visible_with_retries(locator, 39, 30, refresh_btn_locator)


        elif client in ["Everly"]:
            self.webutils.sleep_time(10)
            self.zahara_api.call_lifecycle_api(new_policy_number, client_life_cycle_date, client_plan_code)

            self.webutils.sleep_time(10)
            self.webutils.wait_and_click(ZaharaLocators.zahara_refresh_btn)
            self.validate_policy_status(expected_policy_status)

            self.webutils.sleep_time(60)
            locator = ZaharaLocators.validate_lifecycle_update_date.format(validate_client_effe_date)
            refresh_btn_locator = ZaharaLocators.zahara_refresh_btn
            self.webutils.wait_until_element_visible_with_retries(locator, 39, 30, refresh_btn_locator)

        self.webutils.close_browser()
        return new_policy_number, payee_name


    @keyword
    def process_lifecycle_post_loan_processing(self, new_policy_number, lifecycle_date, client_plan_code):
        self.zahara_api.call_lifecycle_api(new_policy_number, lifecycle_date, client_plan_code)

        BuiltIn().log(f"Lifecycle successfully completed post loan processing.")
        BuiltIn().log_to_console(f"Lifecycle successfully completed post loan processing.")

    @keyword
    def process_lifecycle_post_loan_repayment_processing(self, new_policy_number, lifecycle_date, plan_code):
        self.zahara_api.call_lifecycle_api(new_policy_number, lifecycle_date, plan_code)

        BuiltIn().log(f"Lifecycle successfully completed post loan repayment processing.")
        BuiltIn().log_to_console(f"Lifecycle successfully completed post loan repayment processing.")

    @keyword
    def process_lifecycle_for_fund_allocation_processing(self, new_policy_number, lifecycle_date, plan_code):
        self.zahara_api.call_lifecycle_api(new_policy_number, lifecycle_date, plan_code)

        BuiltIn().log(f"Lifecycle successfully completed for fund allocation processing.")
        BuiltIn().log_to_console(f"Lifecycle successfully completed for fund allocation processing.")

    @keyword
    def process_lifecycle_for_bene_change_processing(self, new_policy_number, lifecycle_date, plan_code):
        self.zahara_api.call_lifecycle_api(new_policy_number, lifecycle_date, plan_code)

        BuiltIn().log(f"Lifecycle successfully completed for beneficiary change processing.")
        BuiltIn().log_to_console(f"Lifecycle successfully completed for beneficiary change processing.")

    @keyword
    def process_lifecycle_for_fund_transfer_processing(self, new_policy_number, lifecycle_date, plan_code):
        self.zahara_api.call_lifecycle_api(new_policy_number, lifecycle_date, plan_code)

        BuiltIn().log(f"Lifecycle successfully completed for fund transfer processing.")
        BuiltIn().log_to_console(f"Lifecycle successfully completed for fund transfer processing.")

    @keyword
    def process_lifecycle_for_systematic_withdrawal_processing(self, new_policy_number, lifecycle_date, plan_code):
        self.zahara_api.call_lifecycle_api(new_policy_number, lifecycle_date, plan_code)

        BuiltIn().log(f"Lifecycle successfully completed for systematic withdrawal processing.")
        BuiltIn().log_to_console(f"Lifecycle successfully completed for systematic withdrawal processing.")

    @keyword
    def process_lifecycle_for_systematic_withdrawal_processing_after_transaction_initiate(self, new_policy_number, lifecycle_date, plan_code):
        self.zahara_api.call_lifecycle_api(new_policy_number, lifecycle_date, plan_code)

        BuiltIn().log(f"Lifecycle successfully completed for systematic withdrawal processing post transaction initiate.")
        BuiltIn().log_to_console(f"Lifecycle successfully completed for systematic withdrawal processing post transaction initiate.")

    @keyword
    def process_lifecycle_for_systematic_RMD_processing(self, new_policy_number, lifecycle_date, plan_code):
        self.zahara_api.call_lifecycle_api(new_policy_number, lifecycle_date, plan_code)

        BuiltIn().log(f"Lifecycle successfully completed for systematic RMD processing.")
        BuiltIn().log_to_console(f"Lifecycle successfully completed for systematic RMD processing.")

    @keyword
    def process_lifecycle_for_systematic_rmd_update_processing(self, new_policy_number, lifecycle_date, plan_code):
        self.zahara_api.call_lifecycle_api(new_policy_number, lifecycle_date, plan_code)

        BuiltIn().log(f"Lifecycle successfully completed for systematic rmd manage processing.")
        BuiltIn().log_to_console(f"Lifecycle successfully completed for systematic rmd manage processing.")

    @keyword
    def process_lifecycle_for_systematic_withdrawal_update_processing(self, new_policy_number, lifecycle_date, plan_code):
        self.zahara_api.call_lifecycle_api(new_policy_number, lifecycle_date, plan_code)

        BuiltIn().log(f"Lifecycle successfully completed for systematic withdrawal manage processing.")
        BuiltIn().log_to_console(f"Lifecycle successfully completed for systematic withdrawal manage processing.")

    @keyword
    def process_lifecycle_for_systematic_premium_update_processing(self, new_policy_number, lifecycle_date, plan_code):
        self.zahara_api.call_lifecycle_api(new_policy_number, lifecycle_date, plan_code)

        BuiltIn().log(f"Lifecycle successfully completed for systematic premium manage processing.")
        BuiltIn().log_to_console(f"Lifecycle successfully completed for systematic premium manage processing.")

    @keyword
    def process_lifecycle_systematic_rmd_autopay_cancel_processing(self, new_policy_number, lifecycle_date, plan_code):
        self.zahara_api.call_lifecycle_api(new_policy_number, lifecycle_date, plan_code)

        BuiltIn().log(f"Lifecycle successfully completed for systematic RMD autopay cancel processing.")
        BuiltIn().log_to_console(f"Lifecycle successfully completed for systematic RMD autopay cancel processing.")


    @keyword
    def process_lifecycle_systematic_withdrawal_autopay_cancel_processing(self, new_policy_number, lifecycle_date, plan_code):
        self.zahara_api.call_lifecycle_api(new_policy_number, lifecycle_date, plan_code)

        BuiltIn().log(f"Lifecycle successfully completed for systematic withdrawal autopay cancel processing.")
        BuiltIn().log_to_console(f"Lifecycle successfully completed for systematic withdrawal autopay cancel processing.")

















