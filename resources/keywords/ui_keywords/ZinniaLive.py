from robot.api.deco import keyword, library
from resources.keywords.api_keywords.ZaharaApi import ZaharaApi
from resources.keywords.ui_keywords.Zahara import Zahara
from resources.locators import ZinniaLive_web_locators
from resources.utilities.ExcelUtilities import ExcelUtilities
from resources.utilities.FileUtils import FileUtils
from resources.utilities.ReadConfig import ReadConfig
from resources.utilities.WebUtils import WebUtils
from robot.libraries.BuiltIn import BuiltIn
from resources.vo.FilePropertiesVo import FilePropertiesVo

# from resources.Reporting.ReportingSetup import ReportingSetup


@library
class ZinniaLive:
    url = "https://qa.zinnialive.com/cases"
    # url = "https://operations-digital-experience-monorepo-git-fea-db1017-zinnia-xd.vercel.app/"
    # browser = "headlesschrome"
    browser = "chrome"
    webutils = WebUtils()
    excel = ExcelUtilities()
    read_config = ReadConfig()
    fileProperties = FilePropertiesVo()
    file = FileUtils()
    zahara = Zahara()
    zahara_api  = ZaharaApi()

    @keyword
    def validate_loan_amount(self, expected_amount):
        locator = ZinniaLive_web_locators.validate_loan_amt_text.format(expected_amount)
        self.webutils.wait_until_element_visible(locator, timeout=60)
        actual_amount = self.webutils.get_text(locator)

        if expected_amount != actual_amount:
            raise AssertionError(
                f"Loan amount on loan summary does not match! Expected: '{expected_amount}', Actual: '{actual_amount}'")
        BuiltIn().log(f"Loan amount on loan summary match! Expected: '{expected_amount}', Actual: '{actual_amount}'")
        BuiltIn().log_to_console(
            f"Loan amount on loan summary match! Expected: '{expected_amount}', Actual: '{actual_amount}'")

    @keyword
    def validate_loan_autopay_amount(self, expected_amount):
        locator = ZinniaLive_web_locators.validate_loan_amt_text.format(expected_amount)
        self.webutils.wait_until_element_visible(locator, timeout=60)
        actual_amount = self.webutils.get_text(locator)

        if expected_amount != actual_amount:
            raise AssertionError(
                f"Loan autopay  amount on process summary page does not match! Expected: '{expected_amount}', Actual: '{actual_amount}'")
        BuiltIn().log(
            f"Loan autopay  amount on process summary page match! Expected: '{expected_amount}', Actual: '{actual_amount}'")
        BuiltIn().log_to_console(
            f"Loan autopay  amount on process summary page match! Expected: '{expected_amount}', Actual: '{actual_amount}'")

    @keyword
    def validate_new_loan_autopay_details(self, old_expected_amount, new_expected_amount):
        locator = ZinniaLive_web_locators.validate_loan_amt_text.format(old_expected_amount)
        self.webutils.wait_until_element_visible(locator, timeout=60)
        old_actual_amount = self.webutils.get_text(locator)

        if old_expected_amount != old_actual_amount:
            raise AssertionError(
                f"old loan autopay  amount on loan summary does not match! Expected: '{old_expected_amount}', Actual: '{old_actual_amount}'")
        BuiltIn().log(
            f"Old loan autopay  amount on loan summary match! Expected: '{old_expected_amount}', Actual: '{old_actual_amount}'")
        BuiltIn().log_to_console(
            f"Old loan autopay  amount on loan summary match! Expected: '{old_expected_amount}', Actual: '{old_actual_amount}'")

        locator1 = ZinniaLive_web_locators.validate_loan_amt_text.format(new_expected_amount)
        self.webutils.wait_until_element_visible(locator1, timeout=60)
        new_actual_amount = self.webutils.get_text(locator1)

        if new_expected_amount != new_actual_amount:
            raise AssertionError(
                f"New loan autopay  amount on loan summary does not match! Expected: '{new_expected_amount}', Actual: '{new_actual_amount}'")
        BuiltIn().log(
            f"New loan autopay  amount on loan summary match! Expected: '{new_expected_amount}', Actual: '{new_actual_amount}'")
        BuiltIn().log_to_console(
            f"New loan autopay  amount on loan summary match! Expected: '{new_expected_amount}', Actual: '{new_actual_amount}'")

    @keyword
    def validate_payment_frequency(self, payment_frequency):
        locator = ZinniaLive_web_locators.validate_loan_amt_text.format(payment_frequency)
        self.webutils.wait_until_element_visible(locator, timeout=60)
        actual_payment_frequency = self.webutils.get_text(locator)

        if payment_frequency != actual_payment_frequency:
            raise AssertionError(
                f"Payment frequency on process summary page does not match! Expected: '{payment_frequency}', Actual: '{actual_payment_frequency}'")
        BuiltIn().log(
            f"Payment frequency on process summary page match! Expected: '{payment_frequency}', Actual: '{actual_payment_frequency}'")
        BuiltIn().log_to_console(
            f"Payment frequency on process summary page match! Expected: '{payment_frequency}', Actual: '{actual_payment_frequency}'")

    @keyword
    def validate_premium_setup_process_completation(self, systematic_premium_amount):
        locator = ZinniaLive_web_locators.validate_systematic_premium.format(systematic_premium_amount)
        self.webutils.wait_until_element_visible(locator, timeout=60)
        actual_systematic_premium_amount = self.webutils.get_text(locator)

        if systematic_premium_amount != actual_systematic_premium_amount:
            raise AssertionError(
                f"Validation Failed: Systematic Premium Setup submission unsuccessful")
        BuiltIn().log(
            f"Validation Passed: Systematic Premium Setup submitted successfully")
        BuiltIn().log_to_console(
            f"Validation Passed: Systematic Premium Setup submitted successfully")

    @keyword
    def validate_old_new_payment_frequency(self, old_payment_frequency, new_payment_frequency):
        locator = ZinniaLive_web_locators.validate_loan_amt_text.format(old_payment_frequency)
        self.webutils.wait_until_element_visible(locator, timeout=60)
        old_actual_payment_frequency = self.webutils.get_text(locator)

        if old_payment_frequency != old_actual_payment_frequency:
            raise AssertionError(
                f"Old loan Payment frequency on process summary page does not match! Expected: '{old_payment_frequency}', Actual: '{old_actual_payment_frequency}'")
        BuiltIn().log(
            f"Old loan Payment frequency on process summary page match! Expected: '{old_payment_frequency}', Actual: '{old_actual_payment_frequency}'")
        BuiltIn().log_to_console(
            f"Old loan Payment frequency on process summary page match! Expected: '{old_payment_frequency}', Actual: '{old_actual_payment_frequency}'")

        locator1 = ZinniaLive_web_locators.validate_loan_amt_text.format(new_payment_frequency)
        self.webutils.wait_until_element_visible(locator1, timeout=60)
        new_actual_payment_frequency = self.webutils.get_text(locator1)

        if new_payment_frequency != new_actual_payment_frequency:
            raise AssertionError(
                f"New loan Payment frequency on process summary page does not match! Expected: '{new_payment_frequency}', Actual: '{new_actual_payment_frequency}'")
        BuiltIn().log(
            f"New loan Payment frequency on process summary page match! Expected: '{new_payment_frequency}', Actual: '{new_actual_payment_frequency}'")
        BuiltIn().log_to_console(
            f"New loan Payment frequency on process summary page match! Expected: '{new_payment_frequency}', Actual: '{new_actual_payment_frequency}'")

    @keyword
    def validate_effective_date(self, expected_date):
        locator = ZinniaLive_web_locators.validate_effective_date.format(expected_date)
        self.webutils.wait_until_element_visible(locator, timeout=60)
        actual_date = self.webutils.get_text(locator)

        if expected_date != actual_date:
            raise AssertionError(
                f"Effective date on process summary page does not match! Expected: '{expected_date}', Actual: '{actual_date}'")
        BuiltIn().log(f"Effective date on process summary page match! Expected: '{expected_date}', Actual: '{actual_date}'")
        BuiltIn().log_to_console(
            f"Effective date on process summary page match! Expected: '{expected_date}', Actual: '{actual_date}'")

    @keyword
    def validate_manage_next_payment_date(self, expected_date):
        locator = ZinniaLive_web_locators.validate_effective_date.format(expected_date)
        self.webutils.wait_until_element_visible(locator, timeout=60)
        actual_date = self.webutils.get_text(locator)

        if expected_date != actual_date:
            raise AssertionError(
                f"Next payment date on process summary page does not match! Expected: '{expected_date}', Actual: '{actual_date}'")
        BuiltIn().log(f"Next payment date on process summary page match! Expected: '{expected_date}', Actual: '{actual_date}'")
        BuiltIn().log_to_console(
            f"Next payment date on process summary page match! Expected: '{expected_date}', Actual: '{actual_date}'")

    @keyword
    def validate_fund_allocation_type(self, expected_fund_allocation_type):
        locator = ZinniaLive_web_locators.validate_fund_allocation.format(expected_fund_allocation_type)
        self.webutils.wait_until_element_visible(locator, timeout=60)
        actual_fund_allocation_type = self.webutils.get_text(locator)

        if expected_fund_allocation_type != actual_fund_allocation_type:
            raise AssertionError(
                f"Fund allocation type on loan summary does not match! Expected: '{expected_fund_allocation_type}', Actual: '{actual_fund_allocation_type}'")
        BuiltIn().log(
            f"Fund allocation type on loan summary match! Expected: '{expected_fund_allocation_type}', Actual: '{actual_fund_allocation_type}'")
        BuiltIn().log_to_console(
            f"Fund allocation type on loan summary match! Expected: '{expected_fund_allocation_type}', Actual: '{actual_fund_allocation_type}'")

    @keyword
    def validate_payee_name(self, expected_payee_name):
        locator = ZinniaLive_web_locators.validate_payee_name.format(expected_payee_name)
        self.webutils.wait_until_element_visible(locator, timeout=60)
        actual_payee_name = self.webutils.get_text(locator)

        if expected_payee_name != actual_payee_name:
            raise AssertionError(
                f"Payee name on process summary page does not match! Expected: '{expected_payee_name}', Actual: '{actual_payee_name}'")
        BuiltIn().log(
            f"Payee name on process summary page match! Expected: '{expected_payee_name}', Actual: '{actual_payee_name}'")
        BuiltIn().log_to_console(
            f"Payee name on process summary page match! Expected: '{expected_payee_name}', Actual: '{actual_payee_name}'")

    @keyword
    def validate_payment_method(self, expected_payment_method):
        locator = ZinniaLive_web_locators.validate_payment_method.format(expected_payment_method)
        self.webutils.wait_until_element_visible(locator, timeout=60)
        actual_payment_method = self.webutils.get_text(locator)

        if expected_payment_method != actual_payment_method:
            raise AssertionError(
                f"Payment method on process summary page does not match! Expected: '{expected_payment_method}', Actual: '{actual_payment_method}'")
        BuiltIn().log(
            f"Payment method on process summary page match! Expected: '{expected_payment_method}', Actual: '{actual_payment_method}'")
        BuiltIn().log_to_console(
            f"Payment method on process summary page match! Expected: '{expected_payment_method}', Actual: '{actual_payment_method}'")

    @keyword
    def validate_account_name_and_number(self, expected_account_name, expected_account_number):
        account_name_locator = ZinniaLive_web_locators.validate_account_name.format(expected_account_name)
        self.webutils.wait_until_element_visible(account_name_locator, timeout=60)
        actual_account_name = self.webutils.get_text(account_name_locator)

        if expected_account_name != actual_account_name:
            raise AssertionError(
                f"Account name on process summary page does not match! Expected: '{expected_account_name}', Actual: '{actual_account_name}'")

        BuiltIn().log(
            f"Account name on process summary page match! Expected: '{expected_account_name}', Actual: '{actual_account_name}'")
        BuiltIn().log_to_console(
            f"Account name on process summary page match! Expected: '{expected_account_name}', Actual: '{actual_account_name}'")

        account_number_locator = ZinniaLive_web_locators.validate_account_number.format(expected_account_number)
        self.webutils.wait_until_element_visible(account_number_locator, timeout=60)
        actual_account_number = self.webutils.get_text(account_number_locator)

        if expected_account_number != actual_account_number:
            raise AssertionError(
                f"Account number on loan summary does not match! Expected: '{expected_account_number}', Actual: '{actual_account_number}'")

        BuiltIn().log(
            f"Account number on loan summary match! Expected: '{expected_account_number}', Actual: '{actual_account_number}'")
        BuiltIn().log_to_console(
            f"Account number on loan summary match! Expected: '{expected_account_number}', Actual: '{actual_account_number}'")


    @keyword
    def validate_transfer_from_and_transfer_to_account(self, expected_transfer_from, expected_transfer_to):
        account_name_locator = ZinniaLive_web_locators.validate_transfer_from.format(expected_transfer_from)
        self.webutils.wait_until_element_visible(account_name_locator, timeout=60)
        actual_transfer_from = self.webutils.get_text(account_name_locator)

        if expected_transfer_from != actual_transfer_from:
            raise AssertionError(
                f"Transfer from account on process summary page does not match! Expected: '{expected_transfer_from}', Actual: '{actual_transfer_from}'")

        BuiltIn().log(
            f"Transfer from account on process summary page match! Expected: '{expected_transfer_from}', Actual: '{actual_transfer_from}'")
        BuiltIn().log_to_console(
            f"Transfer from account on on process summary page match! Expected: '{expected_transfer_from}', Actual: '{actual_transfer_from}'")

        account_number_locator = ZinniaLive_web_locators.validate_transfer_to.format(expected_transfer_to)
        self.webutils.wait_until_element_visible(account_number_locator, timeout=60)
        actual_transfer_to = self.webutils.get_text(account_number_locator)

        if expected_transfer_to != actual_transfer_to:
            raise AssertionError(
                f"Transfer to account on process summary does not match! Expected: '{expected_transfer_to}', Actual: '{actual_transfer_to}'")

        BuiltIn().log(
            f"Transfer to account on process summary match! Expected: '{expected_transfer_to}', Actual: '{actual_transfer_to}'")
        BuiltIn().log_to_console(
            f"Transfer to account on process summary match! Expected: '{expected_transfer_to}', Actual: '{actual_transfer_to}'")

    @keyword
    def validate_start_a_loan_submission(self, expected_loan_status):
        locator = ZinniaLive_web_locators.validate_start_loan_apply.format(expected_loan_status)
        self.webutils.wait_until_element_visible(locator, timeout=60)
        actual_loan_status = self.webutils.get_text(locator)

        if expected_loan_status != actual_loan_status:
            raise AssertionError(
                f"Validation Failed: Loan application submission unsuccessful.")
        BuiltIn().log(f"Validation Passed: Loan application submitted successfully.")
        BuiltIn().log_to_console(f"Validation Passed: Loan application submitted successfully.")

    @keyword
    def validate_loan_autopay_submission(self, expected_loan_status):
        locator = ZinniaLive_web_locators.validate_start_loan_apply.format(expected_loan_status)
        self.webutils.wait_until_element_visible(locator, timeout=60)
        actual_loan_status = self.webutils.get_text(locator)

        if expected_loan_status != actual_loan_status:
            raise AssertionError(
                f"Validation Failed: Loan repayment autopay request  submission unsuccessful.")
        BuiltIn().log(f"Validation Passed: Loan repayment autopay request  submitted successfully.")
        BuiltIn().log_to_console(f"Validation Passed: Loan repayment autopay request  submitted successfully.")\


    @keyword
    def validate_systematic_setup_submission(self, expected_loan_status):
        locator = ZinniaLive_web_locators.validate_start_loan_apply.format(expected_loan_status)
        self.webutils.wait_until_element_visible(locator, timeout=60)
        actual_loan_status = self.webutils.get_text(locator)

        if expected_loan_status != actual_loan_status:
            raise AssertionError(
                f"Validation Failed: Systematic withdrawal request submission unsuccessful.")
        BuiltIn().log(f"Validation Passed: Systematic withdrawal equest submitted successfully.")
        BuiltIn().log_to_console(f"Validation Passed: Systematic withdrawal request submitted successfully.")


    @keyword
    def validate_systematic_RMD_setup_submission(self, expected_loan_status):
        locator = ZinniaLive_web_locators.validate_start_loan_apply.format(expected_loan_status)
        self.webutils.wait_until_element_visible(locator, timeout=60)
        actual_loan_status = self.webutils.get_text(locator)

        if expected_loan_status != actual_loan_status:
            raise AssertionError(
                f"Validation Failed: Systematic RMD request submission unsuccessful.")
        BuiltIn().log(f"Validation Passed: Systematic RMD request submitted successfully.")
        BuiltIn().log_to_console(f"Validation Passed: Systematic RMD request submitted successfully.")

    @keyword
    def validate_update_loan_autopay_submission(self, expected_loan_status):
        locator = ZinniaLive_web_locators.validate_start_loan_apply.format(expected_loan_status)
        self.webutils.wait_until_element_visible(locator, timeout=60)
        actual_loan_status = self.webutils.get_text(locator)

        if expected_loan_status != actual_loan_status:
            raise AssertionError(
                f"Validation Failed: Loan repayment autopay update request submission unsuccessful.")
        BuiltIn().log(f"Validation Passed: Loan repayment autopay update request submitted successfully.")
        BuiltIn().log_to_console(f"Validation Passed: Loan repayment autopay update request submitted successfully.")

    @keyword
    def validate_fund_transfer_submission(self, expected_loan_status):
        locator = ZinniaLive_web_locators.validate_start_loan_apply.format(expected_loan_status)
        self.webutils.wait_until_element_visible(locator, timeout=60)
        actual_loan_status = self.webutils.get_text(locator)

        if expected_loan_status != actual_loan_status:
            raise AssertionError(
                f"Validation Failed: Fund transfer request submission unsuccessful.")
        BuiltIn().log(f"Validation Passed: Fund transfer request submitted successfully.")
        BuiltIn().log_to_console(f"Validation Passed: Fund transfer request submitted successfully.")

    @keyword
    def validate_update_systematic_rmd_submission(self, expected_loan_status):
        locator = ZinniaLive_web_locators.validate_start_loan_apply.format(expected_loan_status)
        self.webutils.wait_until_element_visible(locator, timeout=60)
        actual_loan_status = self.webutils.get_text(locator)

        if expected_loan_status != actual_loan_status:
            raise AssertionError(
                f"Validation Failed: Systematic RMD autopay update request submission unsuccessful.")
        BuiltIn().log(f"Validation Passed: Systematic RMD autopay update request submitted successfully.")
        BuiltIn().log_to_console(f"Validation Passed: Systematic RMD autopay update request submitted successfully.")

    @keyword
    def validate_update_systematic_withdrawal_submission(self, expected_loan_status):
        locator = ZinniaLive_web_locators.validate_start_loan_apply.format(expected_loan_status)
        self.webutils.wait_until_element_visible(locator, timeout=60)
        actual_loan_status = self.webutils.get_text(locator)

        if expected_loan_status != actual_loan_status:
            raise AssertionError(
                f"Validation Failed: Systematic withdrawal autopay update request submission unsuccessful.")
        BuiltIn().log(f"Validation Passed: Systematic withdrawal autopay update request submitted successfully.")
        BuiltIn().log_to_console(f"Validation Passed: Systematic withdrawal autopay update request submitted successfully.")


    @keyword
    def validate_update_systematic_premium_submission(self, expected_loan_status):
        locator = ZinniaLive_web_locators.validate_start_loan_apply.format(expected_loan_status)
        self.webutils.wait_until_element_visible(locator, timeout=60)
        actual_loan_status = self.webutils.get_text(locator)

        if expected_loan_status != actual_loan_status:
            raise AssertionError(
                f"Validation Failed: Systematic premium autopay update request submission unsuccessful.")
        BuiltIn().log(f"Validation Passed: Systematic premium autopay update request submitted successfully.")
        BuiltIn().log_to_console(f"Validation Passed: Systematic premium autopay update request submitted successfully.")

    @keyword
    def validate_cancel_loan_autopay_submission(self, expected_loan_status):
        locator = ZinniaLive_web_locators.validate_start_loan_apply.format(expected_loan_status)
        self.webutils.wait_until_element_visible(locator, timeout=60)
        actual_loan_status = self.webutils.get_text(locator)

        if expected_loan_status != actual_loan_status:
            raise AssertionError(
                f"Validation Failed: Loan autopay cancellation request submission unsuccessful.")
        BuiltIn().log(f"Validation Passed: Loan autopay cancellation request submitted successfully.")
        BuiltIn().log_to_console(f"Validation Passed: Loan autopay cancellation request submitted successfully.")

    @keyword
    def validate_fund_allocation_submission(self, expected_loan_status):
        locator = ZinniaLive_web_locators.validate_start_loan_apply.format(expected_loan_status)
        self.webutils.wait_until_element_visible(locator, timeout=60)
        actual_loan_status = self.webutils.get_text(locator)

        if expected_loan_status != actual_loan_status:
            raise AssertionError(
                f"Validation Failed: Fund allocation request submission unsuccessful.")
        BuiltIn().log(f"Validation Passed: Fund allocation request submitted successfully.")
        BuiltIn().log_to_console(f"Validation Passed: Fund allocation request submitted successfully.")

    @keyword
    def validate_preferred_communication_change_submission(self, expected_loan_status):
        locator = ZinniaLive_web_locators.validate_start_loan_apply.format(expected_loan_status)
        self.webutils.wait_until_element_visible(locator, timeout=60)
        actual_loan_status = self.webutils.get_text(locator)

        if expected_loan_status != actual_loan_status:
            raise AssertionError(
                f"Validation Failed: Preferred communication change request submission unsuccessful.")
        BuiltIn().log(f"Validation Passed: Preferred communication change request submitted successfully.")
        BuiltIn().log_to_console(f"Validation Passed: Preferred communication change request submitted successfully.")

    @keyword
    def validate_bene_change_submission(self, expected_loan_status):
        locator = ZinniaLive_web_locators.validate_start_loan_apply.format(expected_loan_status)
        self.webutils.wait_until_element_visible(locator, timeout=60)
        actual_loan_status = self.webutils.get_text(locator)

        if expected_loan_status != actual_loan_status:
            raise AssertionError(
                f"Validation Failed: beneficiary change request submission unsuccessful.")
        BuiltIn().log(f"Validation Passed: beneficiary change request submitted successfully.")
        BuiltIn().log_to_console(f"Validation Passed: beneficiary change request submitted successfully.")

    @keyword
    def validate_cancel_systematic_rmd__autopay_submission(self, expected_loan_status):
        locator = ZinniaLive_web_locators.validate_start_loan_apply.format(expected_loan_status)
        self.webutils.wait_until_element_visible(locator, timeout=60)
        actual_loan_status = self.webutils.get_text(locator)

        if expected_loan_status != actual_loan_status:
            raise AssertionError(
                f"Validation Failed: Systematic RMD cancellation request submission unsuccessful.")
        BuiltIn().log(f"Validation Passed: Systematic RMD cancellation request submitted successfully.")
        BuiltIn().log_to_console(f"Validation Passed: Systematic RMD cancellation request submitted successfully.")

    @keyword
    def validate_cancel_systematic_withdrawal_autopay_submission(self, expected_loan_status):
        locator = ZinniaLive_web_locators.validate_start_loan_apply.format(expected_loan_status)
        self.webutils.wait_until_element_visible(locator, timeout=60)
        actual_loan_status = self.webutils.get_text(locator)

        if expected_loan_status != actual_loan_status:
            raise AssertionError(
                f"Validation Failed: Systematic withdrawal cancellation request submission unsuccessful.")
        BuiltIn().log(f"Validation Passed: Systematic withdrawal cancellation request submitted successfully.")
        BuiltIn().log_to_console(f"Validation Passed: Systematic withdrawal cancellation request submitted successfully.")

    @keyword
    def validate_one_type_loan__repayment_submission(self, expected_loan_status):
        locator = ZinniaLive_web_locators.validate_start_loan_apply.format(expected_loan_status)
        self.webutils.wait_until_element_visible(locator, timeout=60)
        actual_loan_status = self.webutils.get_text(locator)

        if expected_loan_status != actual_loan_status:
            raise AssertionError(
                f"Validation Failed: New One-Time Loan Repayment Process was unsuccessful.")
        BuiltIn().log(f"Validation Passed: New One-Time Loan Repayment Process completed successfully.")
        BuiltIn().log_to_console(f"Validation Passed: New One-Time Loan Repayment Process completed successfully.")

    @keyword
    def login_to_zinnia_live_and_start_a_loan(self, policy_number, expected_payee_name, start_loan_amount, payment_mode_select,
                                              expected_fund_allocation_type, expected_account_name,
                                              expected_account_number, plan_code):

        BuiltIn().log("Perform Start A Loan Process")
        BuiltIn().log_to_console("Perform Start A Loan Process")
        BuiltIn().log("-----------------------------------------------------------")
        BuiltIn().log_to_console("-----------------------------------------------------------")
        
        # DEBUG: Add detailed logging
        BuiltIn().log_to_console(f"DEBUG: Attempting to open ZinniaLive URL: {ZinniaLive.url}")
        BuiltIn().log_to_console(f"DEBUG: Using browser: {ZinniaLive.browser}")
        
        try:
            self.webutils.open_browser_with_url(ZinniaLive.url, ZinniaLive.browser)
            BuiltIn().log_to_console("DEBUG: Browser opened successfully")
        except Exception as e:
            BuiltIn().log_to_console(f"DEBUG: Browser opening failed: {str(e)}")
            raise
            
        # DEBUG: Add policy sync delay
        BuiltIn().log_to_console("DEBUG: Waiting 10 seconds for policy sync between Zahara and ZinniaLive...")
        self.webutils.sleep_time(10)
        
        user_id = self.read_config.getValueByKey('zinnia_live_user_email')
        BuiltIn().log_to_console(f"DEBUG: Retrieved user_id: {user_id}")
        
        try:
            BuiltIn().log_to_console("DEBUG: Attempting to input email...")
            self.webutils.wait_and_input_text(ZinniaLive_web_locators.zl_user_input, user_id)
            BuiltIn().log_to_console("DEBUG: Email input successful")
            
            BuiltIn().log_to_console("DEBUG: Clicking submit button...")
            self.webutils.wait_and_click(ZinniaLive_web_locators.zl_user_submit_btn)
            BuiltIn().log_to_console("DEBUG: Submit button clicked")
            
            # Add extra wait time for page transition
            BuiltIn().log_to_console("DEBUG: Waiting 5 seconds for page transition...")
            self.webutils.sleep_time(5)
            
        except Exception as e:
            BuiltIn().log_to_console(f"DEBUG: Login step failed: {str(e)}")
            raise
            
        self.start_loan_process(policy_number, expected_payee_name, start_loan_amount, payment_mode_select,
                                expected_fund_allocation_type, expected_account_name, expected_account_number, plan_code)

        if self.webutils.is_element_visible(ZinniaLive_web_locators.zl_user_pass_input):
            user_pass = self.read_config.getValueByKey('zinnia_live_pass')
            self.webutils.wait_and_input_text(ZinniaLive_web_locators.zl_user_pass_input, user_pass)
            self.webutils.wait_and_click(ZinniaLive_web_locators.zl_user_pass_submit_btn)
            self.start_loan_process(policy_number, expected_payee_name, start_loan_amount, payment_mode_select,
                                    expected_fund_allocation_type, expected_account_name, expected_account_number, plan_code)

    @keyword
    def format_payment_mode(self, payment_mode_select):
        if payment_mode_select.upper() == "CHECK":
            return "Check"
        elif payment_mode_select.upper() in ["WIRE", "ACH"]:
            return payment_mode_select.upper()
        else:
            return "Invalid Payment Mode"

    @keyword
    def start_loan_process(self, policy_num, payee_name, start_loan_amt, payment_mode, fund_type, acc_name, acc_number, plan_code):
        policy_number = self.file.normalize_input_value(policy_num)
        expected_payee_name = self.file.normalize_input_value(payee_name)
        start_loan_amount = self.file.normalize_input_value(start_loan_amt)
        payment_mode_select = self.file.normalize_input_value(payment_mode)
        expected_fund_allocation_type = self.file.normalize_input_value(fund_type)
        expected_account_name = self.file.normalize_input_value(acc_name)
        expected_account_number = self.file.normalize_input_value(acc_number)
        client_plan_code = self.file.normalize_input_value(plan_code)

        # DEBUG: Check for Policies & Contracts tab
        BuiltIn().log_to_console("DEBUG: Looking for 'Policies & Contracts' tab...")
        BuiltIn().log_to_console(f"DEBUG: Locator: {ZinniaLive_web_locators.zl_policy_search_tab}")
        
        try:
            # Check if element exists first
            if self.webutils.is_element_visible(ZinniaLive_web_locators.zl_policy_search_tab):
                BuiltIn().log_to_console("DEBUG: 'Policies & Contracts' tab found!")
                self.webutils.wait_and_click(ZinniaLive_web_locators.zl_policy_search_tab)
                BuiltIn().log_to_console("DEBUG: 'Policies & Contracts' tab clicked successfully")
            else:
                BuiltIn().log_to_console("DEBUG: 'Policies & Contracts' tab NOT visible")
                # Try alternative approach - wait longer
                BuiltIn().log_to_console("DEBUG: Waiting additional 15 seconds for page to load...")
                self.webutils.sleep_time(15)
                self.webutils.wait_and_click(ZinniaLive_web_locators.zl_policy_search_tab)
                
        except Exception as e:
            BuiltIn().log_to_console(f"DEBUG: Failed to find/click 'Policies & Contracts' tab: {str(e)}")
            raise
        self.webutils.wait_and_input_text(ZinniaLive_web_locators.policy_search_input, policy_number)
        self.webutils.wait_and_click(ZinniaLive_web_locators.policy_search_btn)
        self.webutils.wait_and_click(ZinniaLive_web_locators.search_result_select)

        if self.webutils.is_element_visible(ZinniaLive_web_locators.policy_tab):
            self.webutils.wait_and_click(ZinniaLive_web_locators.policy_tab)

        elif self.webutils.is_element_visible(ZinniaLive_web_locators.contract_tab):
            self.webutils.wait_and_click(ZinniaLive_web_locators.contract_tab)

        self.webutils.wait_and_click(ZinniaLive_web_locators.loans_tab)
        self.webutils.wait_and_click(ZinniaLive_web_locators.start_loan_btn)

        self.webutils.wait_and_click(ZinniaLive_web_locators.process_without_document_txt)
        self.webutils.scroll_down(1000)
        self.webutils.wait_and_click(ZinniaLive_web_locators.continue_btn)

        self.webutils.wait_and_click(ZinniaLive_web_locators.start_loan_date_btn)

        for _ in range(3):
            self.webutils.wait_and_click(ZinniaLive_web_locators.back_date_btn)

        self.webutils.wait_and_click(ZinniaLive_web_locators.start_loan_date_select)
        enter_loan_effective_date = self.webutils.get_input_value(ZinniaLive_web_locators.start_loan_effective_date)

        self.webutils.wait_and_click(ZinniaLive_web_locators.custom_amount_radio_btn)
        self.webutils.wait_and_input_text(ZinniaLive_web_locators.custom_amount_input, start_loan_amount)
        self.webutils.scroll_down(1000)
        self.webutils.wait_and_click(ZinniaLive_web_locators.continue_btn)

        self.webutils.scroll_down(1000)
        self.webutils.wait_and_click(ZinniaLive_web_locators.payee_tab)
        self.webutils.wait_and_click(ZinniaLive_web_locators.continue_btn)

        payment_mode_locator = ZinniaLive_web_locators.payment_mode_select.format(payment_mode_select)
        self.webutils.wait_and_click(payment_mode_locator)
        self.webutils.scroll_down(1000)

        self.webutils.wait_and_click(ZinniaLive_web_locators.payee_tab)

        # if payment_mode_select in ["WIRE", "CHECK"]:
        #     self.webutils.wait_and_click(ZinniaLive_web_locators.payee_tab)

        self.webutils.wait_and_click(ZinniaLive_web_locators.payment_page_continue_btn)

        self.webutils.sleep_time(10)
        self.webutils.scroll_up(800)

        self.validate_loan_amount(start_loan_amount)

        expected_date = self.file.date_format_as_remove_zero_from_date_month(enter_loan_effective_date)
        self.validate_effective_date(expected_date)
        self.validate_fund_allocation_type(expected_fund_allocation_type)
        self.validate_payee_name(expected_payee_name)

        self.webutils.scroll_down(1000)

        format_payment_mode = self.format_payment_mode(payment_mode_select)
        self.validate_payment_method(format_payment_mode)
        self.validate_account_name_and_number(expected_account_name, expected_account_number)

        # self.webutils.wait_and_click(ZinniaLive_web_locators.loan_submit_checkbox)

        self.webutils.wait_and_click(ZinniaLive_web_locators.loan_submit_btn)

        expected_loan_status = "Go to case"
        self.validate_start_a_loan_submission(expected_loan_status)

        self.webutils.sleep_time(30)
        self.webutils.wait_and_click(ZinniaLive_web_locators.go_to_case_btn)

        self.webutils.sleep_time(5)
        lifecycle_date = self.file.convert_date_format(enter_loan_effective_date)
        self.zahara.process_lifecycle_post_loan_processing(policy_num, lifecycle_date, client_plan_code)

        complete_validate_status =  ZinniaLive_web_locators.validate_zinnia_complete_status
        nigo_validate_status = ZinniaLive_web_locators.validate_zinnia_nigo_status
        self.webutils.validate_zinniaLive_case_status(complete_validate_status, nigo_validate_status)


    @keyword
    def process_setup_autoPay_repayment(self, policy_number, expected_payee_name, loan_autopay_amt, Payment_freq, acc_name, payment_mode, acc_number, plan_code):
        BuiltIn().log("Perform Systematic Loan Repayment Setup AutoPay Process")
        BuiltIn().log_to_console("Perform Systematic Loan Repayment Setup AutoPay Process")
        BuiltIn().log("-----------------------------------------------------------")
        BuiltIn().log_to_console("-----------------------------------------------------------")

        loan_auto_pay_amount = self.file.normalize_input_value(loan_autopay_amt)
        Payment_frequency = self.file.normalize_input_value(Payment_freq)
        payment_mode_select = self.file.normalize_input_value(payment_mode)
        expected_account_name = self.file.normalize_input_value(acc_name)
        expected_account_number = self.file.normalize_input_value(acc_number)
        client_plan_code = self.file.normalize_input_value(plan_code)


        self.webutils.wait_and_click(ZinniaLive_web_locators.zl_policy_search_tab)
        self.webutils.wait_and_input_text(ZinniaLive_web_locators.policy_search_input, policy_number)
        self.webutils.wait_and_click(ZinniaLive_web_locators.policy_search_btn)
        self.webutils.wait_and_click(ZinniaLive_web_locators.search_result_select)

        if self.webutils.is_element_visible(ZinniaLive_web_locators.policy_tab):
            self.webutils.wait_and_click(ZinniaLive_web_locators.policy_tab)

        elif self.webutils.is_element_visible(ZinniaLive_web_locators.contract_tab):
            self.webutils.wait_and_click(ZinniaLive_web_locators.contract_tab)

        self.webutils.wait_and_click(ZinniaLive_web_locators.loans_tab)

        self.webutils.scroll_down(800)
        self.webutils.wait_and_click(ZinniaLive_web_locators.setup_auto_pay_btn)

        self.webutils.wait_and_click(ZinniaLive_web_locators.process_without_document_txt)
        self.webutils.wait_and_click(ZinniaLive_web_locators.continue_btn)

        self.webutils.scroll_down(1000)
        self.webutils.wait_and_input_text(ZinniaLive_web_locators.loan_auto_amount_input, loan_auto_pay_amount)
        self.webutils.wait_and_click(ZinniaLive_web_locators.payment_frequency_radio_btn.format(Payment_frequency))

        # self.webutils.wait_and_click(ZinniaLive_web_locators.start_loan_date_btn)
        # self.webutils.wait_and_click(ZinniaLive_web_locators.payment_start_date)

        expected_date = self.webutils.get_input_value(ZinniaLive_web_locators.autopay_payment_start_date)
        autopay_start_date = self.file.remove_leading_zeros_from_date(expected_date)

        self.webutils.wait_and_click(ZinniaLive_web_locators.continue_btn)

        self.webutils.wait_and_click(ZinniaLive_web_locators.continue_btn)

        self.webutils.wait_and_click(ZinniaLive_web_locators.autopay_payment_method_continue_btn)

        self.validate_loan_autopay_amount(loan_auto_pay_amount)

        self.validate_effective_date(autopay_start_date)
        self.validate_payment_frequency(Payment_frequency)

        self.webutils.sleep_time(5)
        self.webutils.scroll_down(1000)
        self.validate_payee_name(expected_payee_name)
        format_payment_mode = self.format_payment_mode(payment_mode_select)
        self.validate_payment_method(format_payment_mode)
        self.validate_account_name_and_number(expected_account_name, expected_account_number)

        self.webutils.wait_and_click(ZinniaLive_web_locators.submit_payment_btn)

        expected_loan_status = "Go to case"
        self.validate_loan_autopay_submission(expected_loan_status)

        self.webutils.sleep_time(30)
        self.webutils.wait_and_click(ZinniaLive_web_locators.go_to_case_btn)

        self.webutils.sleep_time(5)
        lifecycle_date = self.file.get_cst_date("%Y-%m-%d")
        self.zahara.process_lifecycle_post_loan_repayment_processing(policy_number, lifecycle_date, client_plan_code)

        complete_validate_status = ZinniaLive_web_locators.validate_zinnia_complete_status
        nigo_validate_status = ZinniaLive_web_locators.validate_zinnia_nigo_status
        self.webutils.validate_zinniaLive_case_status(complete_validate_status, nigo_validate_status)


    @keyword
    def login_to_zinnia_live_and_process_manage_loan_auto_pay(self, policy_number, expected_payee_name, loan_autopay_amt, Payment_freq,
                                                              loan_manage_autopay_amt, manage_payment_freq,
                                                              payment_mode, plan_code):
        BuiltIn().log("Perform Systematic Loan Repayment Setup AutoPay Process")
        BuiltIn().log_to_console("Perform Systematic Loan Repayment Setup AutoPay Process")
        BuiltIn().log("-----------------------------------------------------------")
        BuiltIn().log_to_console("-----------------------------------------------------------")

        self.webutils.open_browser_with_url(ZinniaLive.url, ZinniaLive.browser)
        user_id = self.read_config.getValueByKey('zinnia_live_user_email')
        self.webutils.wait_and_input_text(ZinniaLive_web_locators.zl_user_input, user_id)
        self.webutils.wait_and_click(ZinniaLive_web_locators.zl_user_submit_btn)
        
        # Handle password authentication if required
        if self.webutils.is_element_visible(ZinniaLive_web_locators.zl_user_pass_input):
            user_pass = self.read_config.getValueByKey('zinnia_live_pass')
            self.webutils.wait_and_input_text(ZinniaLive_web_locators.zl_user_pass_input, user_pass)
            self.webutils.wait_and_click(ZinniaLive_web_locators.zl_user_pass_submit_btn)
        
        # Process manage autopay after authentication is complete
        self.process_manage_autoPay(policy_number, expected_payee_name, loan_autopay_amt, Payment_freq, loan_manage_autopay_amt, manage_payment_freq,
                                    payment_mode, plan_code)
        
        # Close browser after process is complete
        self.webutils.close_browser()

    @keyword
    def login_to_zinnia_live_and_perform_systematic_withdrawal_process(self, policy_number, expected_payee_name, loan_autopay_amt, Payment_freq, acc_name, payment_mode, acc_number, plan_code):
        BuiltIn().log("Perform Systematic Withdrawal Process")
        BuiltIn().log_to_console("Perform Systematic Withdrawal Process")
        BuiltIn().log("-----------------------------------------------------------")
        BuiltIn().log_to_console("-----------------------------------------------------------")

        self.webutils.open_browser_with_url(ZinniaLive.url, ZinniaLive.browser)
        user_id = self.read_config.getValueByKey('zinnia_live_user_email')
        self.webutils.wait_and_input_text(ZinniaLive_web_locators.zl_user_input, user_id)
        self.webutils.wait_and_click(ZinniaLive_web_locators.zl_user_submit_btn)
        
        # Handle password authentication if required
        if self.webutils.is_element_visible(ZinniaLive_web_locators.zl_user_pass_input):
            user_pass = self.read_config.getValueByKey('zinnia_live_pass')
            self.webutils.wait_and_input_text(ZinniaLive_web_locators.zl_user_pass_input, user_pass)
            self.webutils.wait_and_click(ZinniaLive_web_locators.zl_user_pass_submit_btn)
        
        # Process systematic withdrawal after authentication is complete
        self.manage_systematic_withdrawal_process(policy_number, expected_payee_name, loan_autopay_amt, Payment_freq, acc_name, payment_mode, acc_number, plan_code)
        
        # Close browser after process is complete
        self.webutils.close_browser()

    @keyword
    def login_to_zinnia_live_and_perform_systematic_premium_setup_process(self, policy_number):
        BuiltIn().log("Perform Systematic Premium Setup Process")
        BuiltIn().log_to_console("Perform Systematic Premium Setup Process")
        BuiltIn().log("-----------------------------------------------------------")
        BuiltIn().log_to_console("-----------------------------------------------------------")

        self.webutils.open_browser_with_url(ZinniaLive.url, ZinniaLive.browser)
        user_id = self.read_config.getValueByKey('zinnia_live_user_email')
        self.webutils.wait_and_input_text(ZinniaLive_web_locators.zl_user_input, user_id)
        self.webutils.wait_and_click(ZinniaLive_web_locators.zl_user_submit_btn)
        self.systematic_premium_setup_process_flow(policy_number)

        if self.webutils.is_element_visible(ZinniaLive_web_locators.zl_user_pass_input):
            user_pass = self.read_config.getValueByKey('zinnia_live_pass')
            self.webutils.wait_and_input_text(ZinniaLive_web_locators.zl_user_pass_input, user_pass)
            self.webutils.wait_and_click(ZinniaLive_web_locators.zl_user_pass_submit_btn)
            self.systematic_premium_setup_process_flow(policy_number)

    @keyword
    def login_to_zinnia_live_and_perform_systematic_rmd_process(self, policy_number, expected_payee_name, loan_autopay_amt, Payment_freq, acc_name, payment_mode, acc_number, plan_code):
        BuiltIn().log("Perform Systematic RMD Process")
        BuiltIn().log_to_console("Perform Systematic RMD Process")
        BuiltIn().log("-----------------------------------------------------------")
        BuiltIn().log_to_console("-----------------------------------------------------------")

        self.webutils.open_browser_with_url(ZinniaLive.url, ZinniaLive.browser)
        user_id = self.read_config.getValueByKey('zinnia_live_user_email')
        self.webutils.wait_and_input_text(ZinniaLive_web_locators.zl_user_input, user_id)
        self.webutils.wait_and_click(ZinniaLive_web_locators.zl_user_submit_btn)
        self.manage_systematic_rmd_process(policy_number, expected_payee_name, loan_autopay_amt, Payment_freq, acc_name, payment_mode, acc_number, plan_code)

        if self.webutils.is_element_visible(ZinniaLive_web_locators.zl_user_pass_input):
            user_pass = self.read_config.getValueByKey('zinnia_live_pass')
            self.webutils.wait_and_input_text(ZinniaLive_web_locators.zl_user_pass_input, user_pass)
            self.webutils.wait_and_click(ZinniaLive_web_locators.zl_user_pass_submit_btn)
            self.manage_systematic_rmd_process(policy_number, expected_payee_name, loan_autopay_amt, Payment_freq, acc_name, payment_mode, acc_number, plan_code)

    @keyword
    def login_to_zinnia_live_and_perform_systematic_rmd_manage_autopay_process(self, policy_num, payee_name, loan_autopay_amt, Payment_freq, systematic_rmd_update_amount, manage_payment_freq,
                               payment_mode):

        BuiltIn().log("Perform Systematic RMD manage AutoPay Process")
        BuiltIn().log_to_console("Perform Systematic RMD manage AutoPay Process")
        BuiltIn().log("-----------------------------------------------------------")
        BuiltIn().log_to_console("-----------------------------------------------------------")

        self.webutils.open_browser_with_url(ZinniaLive.url, ZinniaLive.browser)
        user_id = self.read_config.getValueByKey('zinnia_live_user_email')
        self.webutils.wait_and_input_text(ZinniaLive_web_locators.zl_user_input, user_id)
        self.webutils.wait_and_click(ZinniaLive_web_locators.zl_user_submit_btn)
        self.manage_systematic_rmd_manage_autopay_process(policy_num, payee_name, loan_autopay_amt, Payment_freq, systematic_rmd_update_amount, manage_payment_freq,
                               payment_mode)

        if self.webutils.is_element_visible(ZinniaLive_web_locators.zl_user_pass_input):
            user_pass = self.read_config.getValueByKey('zinnia_live_pass')
            self.webutils.wait_and_input_text(ZinniaLive_web_locators.zl_user_pass_input, user_pass)
            self.webutils.wait_and_click(ZinniaLive_web_locators.zl_user_pass_submit_btn)
            self.manage_systematic_rmd_manage_autopay_process(policy_num, payee_name, loan_autopay_amt, Payment_freq, systematic_rmd_update_amount, manage_payment_freq,
                               payment_mode)


    @keyword
    def login_to_zinnia_live_and_perform_systematic_withdrawal_manage_autopay_process(self, policy_num, payee_name, loan_autopay_amt, Payment_freq, systematic_withdrawal_update_amount, manage_payment_freq,
                               payment_mode):

        BuiltIn().log("Perform Systematic Withdrawal manage AutoPay Process")
        BuiltIn().log_to_console("Perform Systematic Withdrawal manage AutoPay Process")
        BuiltIn().log("-----------------------------------------------------------")
        BuiltIn().log_to_console("-----------------------------------------------------------")

        self.webutils.open_browser_with_url(ZinniaLive.url, ZinniaLive.browser)
        user_id = self.read_config.getValueByKey('zinnia_live_user_email')
        self.webutils.wait_and_input_text(ZinniaLive_web_locators.zl_user_input, user_id)
        self.webutils.wait_and_click(ZinniaLive_web_locators.zl_user_submit_btn)
        self.manage_systematic_withdrawal_manage_autopay_process(policy_num, payee_name, loan_autopay_amt, Payment_freq, systematic_withdrawal_update_amount, manage_payment_freq,
                               payment_mode)

        if self.webutils.is_element_visible(ZinniaLive_web_locators.zl_user_pass_input):
            user_pass = self.read_config.getValueByKey('zinnia_live_pass')
            self.webutils.wait_and_input_text(ZinniaLive_web_locators.zl_user_pass_input, user_pass)
            self.webutils.wait_and_click(ZinniaLive_web_locators.zl_user_pass_submit_btn)
            self.manage_systematic_withdrawal_manage_autopay_process(policy_num, payee_name, loan_autopay_amt, Payment_freq, systematic_withdrawal_update_amount, manage_payment_freq,
                               payment_mode)

    @keyword
    def login_to_zinnia_live_and_perform_systematic_premium_manage_autopay_process(self, policy_num, payee_name, loan_autopay_amt, Payment_freq, systematic_premium_update_amount, manage_payment_freq,
                               payment_mode):

        BuiltIn().log("Perform Systematic Premium Update Process")
        BuiltIn().log_to_console("Perform Systematic Premium Update Process")
        BuiltIn().log("-----------------------------------------------------------")
        BuiltIn().log_to_console("-----------------------------------------------------------")

        self.webutils.open_browser_with_url(ZinniaLive.url, ZinniaLive.browser)
        user_id = self.read_config.getValueByKey('zinnia_live_user_email')
        self.webutils.wait_and_input_text(ZinniaLive_web_locators.zl_user_input, user_id)
        self.webutils.wait_and_click(ZinniaLive_web_locators.zl_user_submit_btn)
        self.manage_systematic_premium_manage_autopay_process(policy_num, payee_name, loan_autopay_amt, Payment_freq, systematic_premium_update_amount, manage_payment_freq,
                               payment_mode)

        if self.webutils.is_element_visible(ZinniaLive_web_locators.zl_user_pass_input):
            user_pass = self.read_config.getValueByKey('zinnia_live_pass')
            self.webutils.wait_and_input_text(ZinniaLive_web_locators.zl_user_pass_input, user_pass)
            self.webutils.wait_and_click(ZinniaLive_web_locators.zl_user_pass_submit_btn)
            self.manage_systematic_premium_manage_autopay_process(policy_num, payee_name, loan_autopay_amt, Payment_freq, systematic_premium_update_amount, manage_payment_freq,
                               payment_mode)



    @keyword
    def process_manage_autoPay(self, policy_num, payee_name, loan_autopay_amt, Payment_freq, loan_manage_autopay_amt, manage_payment_freq,
                               payment_mode, plan_code):

        policy_number = self.file.normalize_input_value(policy_num)
        expected_payee_name = self.file.normalize_input_value(payee_name)
        loan_manage_auto_pay_amount = self.file.normalize_input_value(loan_manage_autopay_amt)
        manage_payment_frequency = self.file.normalize_input_value(manage_payment_freq)
        loan_auto_pay_amount = self.file.normalize_input_value(loan_autopay_amt)
        Payment_frequency = self.file.normalize_input_value(Payment_freq)
        payment_mode_select = self.file.normalize_input_value(payment_mode)

        self.webutils.wait_and_click(ZinniaLive_web_locators.zl_policy_search_tab)
        self.webutils.wait_and_input_text(ZinniaLive_web_locators.policy_search_input, policy_number)
        self.webutils.wait_and_click(ZinniaLive_web_locators.policy_search_btn)
        self.webutils.wait_and_click(ZinniaLive_web_locators.search_result_select)

        if self.webutils.is_element_visible(ZinniaLive_web_locators.policy_tab):
            self.webutils.wait_and_click(ZinniaLive_web_locators.policy_tab)

        elif self.webutils.is_element_visible(ZinniaLive_web_locators.contract_tab):
            self.webutils.wait_and_click(ZinniaLive_web_locators.contract_tab)

        self.webutils.wait_and_click(ZinniaLive_web_locators.loans_tab)

        self.webutils.scroll_down(800)
        self.webutils.wait_and_click(ZinniaLive_web_locators.manage_autopay_btn)

        self.webutils.wait_and_click(ZinniaLive_web_locators.process_without_document_txt)
        self.webutils.wait_and_click(ZinniaLive_web_locators.continue_btn)

        self.webutils.scroll_down(500)

        self.webutils.sleep_time(2)
        # self.webutils.wait_and_clear_text_by_press_key(ZinniaLive_web_locators.loan_auto_pay_amount_input)
        # self.webutils.wait_and_input_text(ZinniaLive_web_locators.loan_auto_pay_amount_input, loan_manage_autopay_amt)


        self.webutils.wait_and_click(
            ZinniaLive_web_locators.payment_frequency_radio_btn.format(manage_payment_frequency))
        next_payment_date = self.webutils.get_input_value(ZinniaLive_web_locators.manage_payment_next_payment_date)

        self.webutils.wait_and_click(ZinniaLive_web_locators.continue_btn)

        self.webutils.wait_and_click(ZinniaLive_web_locators.continue_btn)

        self.webutils.wait_and_click(ZinniaLive_web_locators.autopay_payment_method_continue_btn)

        self.webutils.sleep_time(5)
        self.webutils.scroll_down(1000)
        # self.validate_new_loan_autopay_details(loan_auto_pay_amount, loan_manage_auto_pay_amount)
        self.validate_manage_next_payment_date(next_payment_date)
        self.validate_old_new_payment_frequency(Payment_frequency, manage_payment_frequency)
        self.validate_payee_name(expected_payee_name)
        format_payment_mode = self.format_payment_mode(payment_mode_select)
        self.validate_payment_method(format_payment_mode)

        BuiltIn().log("Systematic Loan Repayment Update Request Submitted.")
        BuiltIn().log_to_console("Systematic Loan Repayment Update Request Submitted.")

        complete_validate_status = ZinniaLive_web_locators.validate_zinnia_complete_status
        nigo_validate_status = ZinniaLive_web_locators.validate_zinnia_nigo_status
        self.webutils.validate_zinniaLive_case_status_1(complete_validate_status, nigo_validate_status)

        # self.webutils.wait_and_click(ZinniaLive_web_locators.update_loan_loan_autoPay_submit_btn)
        #
        # expected_loan_status = "Go to case"
        # self.validate_update_loan_autopay_submission(expected_loan_status)
        #
        # self.webutils.sleep_time(30)
        # self.webutils.wait_and_click(ZinniaLive_web_locators.go_to_case_btn)
        #
        # self.webutils.sleep_time(10)
        # lifecycle_date = self.file.get_cst_date("%Y-%m-%d")
        # self.zahara.process_lifecycle_post_loan_repayment_processing(policy_number, lifecycle_date, plan_code)
        #
        # complete_validate_status = ZinniaLive_web_locators.validate_zinnia_complete_status
        # nigo_validate_status = ZinniaLive_web_locators.validate_zinnia_nigo_status
        # self.webutils.validate_zinniaLive_case_status(complete_validate_status, nigo_validate_status)


    @keyword
    def manage_systematic_withdrawal_process(self, policy_num, expected_payee_name, loan_autopay_amt, Payment_freq, acc_name, payment_mode, acc_number, plan_code):

        policy_number = self.file.normalize_input_value(policy_num)
        loan_auto_pay_amount = self.file.normalize_input_value(loan_autopay_amt)
        Payment_frequency = self.file.normalize_input_value(Payment_freq)
        payment_mode_select = self.file.normalize_input_value(payment_mode)
        expected_account_name = self.file.normalize_input_value(acc_name)
        expected_account_number = self.file.normalize_input_value(acc_number)
        client_plan_code = self.file.normalize_input_value(plan_code)

        self.webutils.wait_and_click(ZinniaLive_web_locators.zl_policy_search_tab)
        self.webutils.wait_and_input_text(ZinniaLive_web_locators.policy_search_input, policy_number)
        self.webutils.wait_and_click(ZinniaLive_web_locators.policy_search_btn)
        self.webutils.wait_and_click(ZinniaLive_web_locators.search_result_select)

        if self.webutils.is_element_visible(ZinniaLive_web_locators.policy_tab):
            self.webutils.wait_and_click(ZinniaLive_web_locators.policy_tab)

        elif self.webutils.is_element_visible(ZinniaLive_web_locators.contract_tab):
            self.webutils.wait_and_click(ZinniaLive_web_locators.contract_tab)

        self.webutils.wait_and_click(ZinniaLive_web_locators.withdrawal_tab)

        self.webutils.scroll_down(600)
        self.webutils.wait_and_click(ZinniaLive_web_locators.setup_auto_pay_btn)

        self.webutils.wait_and_click(ZinniaLive_web_locators.process_without_document_txt)
        self.webutils.wait_and_click(ZinniaLive_web_locators.continue_btn)

        self.webutils.wait_and_click(ZinniaLive_web_locators.withdrawal_type_btn)
        self.webutils.scroll_down(300)
        self.webutils.sleep_time(2)
        self.webutils.wait_and_input_text(ZinniaLive_web_locators.systematic_loan_auto_pay_input, loan_auto_pay_amount)
        self.webutils.wait_and_click(ZinniaLive_web_locators.payment_frequency_radio_btn.format(Payment_frequency))

        self.webutils.wait_and_click(ZinniaLive_web_locators.start_loan_date_btn)
        self.webutils.wait_and_click(ZinniaLive_web_locators.month_select)
        self.webutils.wait_and_click(ZinniaLive_web_locators.feb_month_select)
        self.webutils.wait_and_click(ZinniaLive_web_locators.systematic_withdrawal_effective_start_date)

        expected_date = self.webutils.get_input_value(ZinniaLive_web_locators.autopay_payment_start_date)
        autopay_start_date = self.file.remove_leading_zeros_from_date(expected_date)
        self.webutils.scroll_down(900)
        self.webutils.wait_and_click(ZinniaLive_web_locators.continue_btn)

        self.webutils.wait_and_click(ZinniaLive_web_locators.continue_btn)

        payment_mode_locator = ZinniaLive_web_locators.payment_mode_select.format(payment_mode_select)
        self.webutils.wait_and_click(payment_mode_locator)
        self.webutils.wait_and_click(ZinniaLive_web_locators.payee_tab)
        self.webutils.wait_and_click(ZinniaLive_web_locators.payment_page_continue_btn)

        self.validate_loan_autopay_amount(loan_auto_pay_amount)
        self.validate_effective_date(autopay_start_date)
        self.validate_payment_frequency(Payment_frequency)
        self.validate_payee_name(expected_payee_name)
        format_payment_mode = self.format_payment_mode(payment_mode_select)
        self.validate_payment_method(format_payment_mode)
        self.validate_account_name_and_number(expected_account_name, expected_account_number)
        self.webutils.wait_and_click(ZinniaLive_web_locators.submit_payment_btn)

        expected_loan_status = "Go to case"
        self.validate_systematic_setup_submission(expected_loan_status)

        self.webutils.sleep_time(30)
        self.webutils.wait_and_click(ZinniaLive_web_locators.go_to_case_btn)

        self.webutils.sleep_time(5)
        lifecycle_date = "2025-08-22"
        self.zahara.process_lifecycle_for_systematic_withdrawal_processing(policy_number, lifecycle_date, client_plan_code)

        complete_validate_status = ZinniaLive_web_locators.validate_zinnia_complete_status
        nigo_validate_status = ZinniaLive_web_locators.validate_zinnia_nigo_status
        self.webutils.validate_zinniaLive_case_status(complete_validate_status, nigo_validate_status)



    @keyword
    def systematic_premium_setup_process_flow(self, policy_number):
        self.webutils.wait_and_click(ZinniaLive_web_locators.zl_policy_search_tab)
        self.webutils.wait_and_input_text(ZinniaLive_web_locators.policy_search_input, policy_number)
        self.webutils.wait_and_click(ZinniaLive_web_locators.policy_search_btn)
        self.webutils.wait_and_click(ZinniaLive_web_locators.search_result_select)

        if self.webutils.is_element_visible(ZinniaLive_web_locators.policy_tab):
            self.webutils.wait_and_click(ZinniaLive_web_locators.policy_tab)

        elif self.webutils.is_element_visible(ZinniaLive_web_locators.contract_tab):
            self.webutils.wait_and_click(ZinniaLive_web_locators.contract_tab)

        self.webutils.wait_and_click(ZinniaLive_web_locators.premium_tab)

        self.webutils.wait_until_element_visible(ZinniaLive_web_locators.validate_premium_setup)

        premium_setup_amount = "$300.00"
        self.validate_premium_setup_process_completation(premium_setup_amount)

    @keyword
    def manage_systematic_rmd_process(self, policy_num, expected_payee_name, loan_autopay_amt, Payment_freq, acc_name, payment_mode, acc_number, plan_code):

        policy_number = self.file.normalize_input_value(policy_num)
        loan_auto_pay_amount = self.file.normalize_input_value(loan_autopay_amt)
        Payment_frequency = self.file.normalize_input_value(Payment_freq)
        payment_mode_select = self.file.normalize_input_value(payment_mode)
        expected_account_name = self.file.normalize_input_value(acc_name)
        expected_account_number = self.file.normalize_input_value(acc_number)
        client_plan_code = self.file.normalize_input_value(plan_code)

        self.webutils.wait_and_click(ZinniaLive_web_locators.zl_policy_search_tab)
        self.webutils.wait_and_input_text(ZinniaLive_web_locators.policy_search_input, policy_number)
        self.webutils.wait_and_click(ZinniaLive_web_locators.policy_search_btn)
        self.webutils.wait_and_click(ZinniaLive_web_locators.search_result_select)

        if self.webutils.is_element_visible(ZinniaLive_web_locators.policy_tab):
            self.webutils.wait_and_click(ZinniaLive_web_locators.policy_tab)

        elif self.webutils.is_element_visible(ZinniaLive_web_locators.contract_tab):
            self.webutils.wait_and_click(ZinniaLive_web_locators.contract_tab)

        self.webutils.wait_and_click(ZinniaLive_web_locators.withdrawal_tab)

        self.webutils.scroll_down(900)
        self.webutils.wait_and_click(ZinniaLive_web_locators.setup_auto_rmd_pay_btn)

        self.webutils.wait_and_click(ZinniaLive_web_locators.process_without_document_txt)
        self.webutils.wait_and_click(ZinniaLive_web_locators.continue_btn)

        self.webutils.wait_and_click(ZinniaLive_web_locators.rmd_type_btn)
        self.webutils.scroll_down(300)
        self.webutils.sleep_time(2)
        self.webutils.wait_and_input_text(ZinniaLive_web_locators.systematic_loan_auto_pay_input, loan_auto_pay_amount)
        self.webutils.wait_and_click(ZinniaLive_web_locators.payment_frequency_radio_btn.format(Payment_frequency))

        self.webutils.wait_and_click(ZinniaLive_web_locators.start_loan_date_btn)
        self.webutils.wait_and_click(ZinniaLive_web_locators.month_select)
        self.webutils.wait_and_click(ZinniaLive_web_locators.feb_month_select)
        self.webutils.wait_and_click(ZinniaLive_web_locators.systematic_withdrawal_effective_start_date)

        expected_date = self.webutils.get_input_value(ZinniaLive_web_locators.autopay_payment_start_date)
        autopay_start_date = self.file.remove_leading_zeros_from_date(expected_date)
        self.webutils.scroll_down(900)
        self.webutils.wait_and_click(ZinniaLive_web_locators.continue_btn)

        self.webutils.wait_and_click(ZinniaLive_web_locators.continue_btn)

        payment_mode_locator = ZinniaLive_web_locators.payment_mode_select.format(payment_mode_select)
        self.webutils.wait_and_click(payment_mode_locator)
        self.webutils.wait_and_click(ZinniaLive_web_locators.payee_tab)
        self.webutils.wait_and_click(ZinniaLive_web_locators.payment_page_continue_btn)

        self.validate_loan_autopay_amount(loan_auto_pay_amount)
        self.validate_effective_date(autopay_start_date)
        self.validate_payment_frequency(Payment_frequency)
        self.validate_payee_name(expected_payee_name)
        format_payment_mode = self.format_payment_mode(payment_mode_select)
        self.validate_payment_method(format_payment_mode)
        self.validate_account_name_and_number(expected_account_name, expected_account_number)
        self.webutils.wait_and_click(ZinniaLive_web_locators.submit_payment_btn)

        expected_loan_status = "Go to case"
        self.validate_systematic_RMD_setup_submission(expected_loan_status)

        self.webutils.sleep_time(30)
        self.webutils.wait_and_click(ZinniaLive_web_locators.go_to_case_btn)

        self.webutils.sleep_time(5)
        lifecycle_date = "2025-08-22"
        self.zahara.process_lifecycle_for_systematic_RMD_processing(policy_number, lifecycle_date, client_plan_code)

        complete_validate_status = ZinniaLive_web_locators.validate_zinnia_complete_status
        nigo_validate_status = ZinniaLive_web_locators.validate_zinnia_nigo_status
        self.webutils.validate_zinniaLive_case_status(complete_validate_status, nigo_validate_status)


    @keyword
    def manage_systematic_rmd_manage_autopay_process(self,  policy_num, payee_name, loan_autopay_amt, Payment_freq, systematic_rmd_update_amount, manage_payment_freq,
                               payment_mode):

        policy_number = self.file.normalize_input_value(policy_num)
        expected_payee_name = self.file.normalize_input_value(payee_name)
        loan_manage_auto_pay_amount = self.file.normalize_input_value(systematic_rmd_update_amount)
        manage_payment_frequency = self.file.normalize_input_value(manage_payment_freq)
        loan_auto_pay_amount = self.file.normalize_input_value(loan_autopay_amt)
        Payment_frequency = self.file.normalize_input_value(Payment_freq)
        payment_mode_select = self.file.normalize_input_value(payment_mode)

        self.webutils.wait_and_click(ZinniaLive_web_locators.zl_policy_search_tab)
        self.webutils.wait_and_input_text(ZinniaLive_web_locators.policy_search_input, policy_number)
        self.webutils.wait_and_click(ZinniaLive_web_locators.policy_search_btn)
        self.webutils.wait_and_click(ZinniaLive_web_locators.search_result_select)

        if self.webutils.is_element_visible(ZinniaLive_web_locators.policy_tab):
            self.webutils.wait_and_click(ZinniaLive_web_locators.policy_tab)

        elif self.webutils.is_element_visible(ZinniaLive_web_locators.contract_tab):
            self.webutils.wait_and_click(ZinniaLive_web_locators.contract_tab)

        self.webutils.wait_and_click(ZinniaLive_web_locators.withdrawal_tab)

        self.webutils.scroll_down(900)
        self.webutils.wait_and_click(ZinniaLive_web_locators.systematic_manage_autopay_btn)



        self.webutils.wait_and_click(ZinniaLive_web_locators.process_without_document_txt)
        self.webutils.wait_and_click(ZinniaLive_web_locators.continue_btn)

        self.webutils.sleep_time(2)
        self.webutils.scroll_down(500)
        self.webutils.sleep_time(2)
        # self.webutils.wait_and_clear_text_by_press_key(ZinniaLive_web_locators.loan_auto_pay_amount_input)
        # self.webutils.wait_and_input_text(ZinniaLive_web_locators.loan_auto_pay_amount_input, loan_manage_autopay_amt)

        self.webutils.wait_and_click(
            ZinniaLive_web_locators.payment_frequency_radio_btn.format(manage_payment_frequency))
        next_payment_date = self.webutils.get_input_value(ZinniaLive_web_locators.manage_payment_next_payment_date)

        self.webutils.wait_and_click(ZinniaLive_web_locators.continue_btn)

        self.webutils.wait_and_click(ZinniaLive_web_locators.continue_btn)

        self.webutils.scroll_down(400)
        self.webutils.wait_and_click(ZinniaLive_web_locators.autopay_payment_method_continue_btn)

        self.webutils.sleep_time(5)

        # self.validate_new_loan_autopay_details(loan_auto_pay_amount, loan_manage_auto_pay_amount)
        self.validate_manage_next_payment_date(next_payment_date)
        self.validate_old_new_payment_frequency(Payment_frequency, manage_payment_frequency)
        self.validate_payee_name(expected_payee_name)
        format_payment_mode = self.format_payment_mode(payment_mode_select)
        self.validate_payment_method(format_payment_mode)
        self.webutils.scroll_down(300)

        BuiltIn().log("Systematic Loan RMD Update Request Submitted.")
        BuiltIn().log_to_console("Systematic Loan RMD Update Request Submitted.")

        complete_validate_status = ZinniaLive_web_locators.validate_zinnia_complete_status
        nigo_validate_status = ZinniaLive_web_locators.validate_zinnia_nigo_status
        self.webutils.validate_zinniaLive_case_status_1(complete_validate_status, nigo_validate_status)

        # self.webutils.wait_and_click(ZinniaLive_web_locators.submit_payment_btn)
        #
        # expected_loan_status = "Go to case"
        # self.validate_update_systematic_rmd_submission(expected_loan_status)
        #
        # self.webutils.sleep_time(30)
        # self.webutils.wait_and_click(ZinniaLive_web_locators.go_to_case_btn)
        #
        # self.webutils.sleep_time(10)
        # lifecycle_date = self.file.get_cst_date("%Y-%m-%d")
        # self.zahara.process_lifecycle_for_systematic_rmd_update_processing(policy_number, lifecycle_date)
        #
        # complete_validate_status = ZinniaLive_web_locators.validate_zinnia_complete_status
        # nigo_validate_status = ZinniaLive_web_locators.validate_zinnia_nigo_status
        # self.webutils.validate_zinniaLive_case_status(complete_validate_status, nigo_validate_status)



    @keyword
    def manage_systematic_withdrawal_manage_autopay_process(self,  policy_num, payee_name, loan_autopay_amt, Payment_freq, systematic_withdrawal_update_amount, manage_payment_freq,
                               payment_mode):

        policy_number = self.file.normalize_input_value(policy_num)
        expected_payee_name = self.file.normalize_input_value(payee_name)
        loan_manage_auto_pay_amount = self.file.normalize_input_value(systematic_withdrawal_update_amount)
        manage_payment_frequency = self.file.normalize_input_value(manage_payment_freq)
        loan_auto_pay_amount = self.file.normalize_input_value(loan_autopay_amt)
        Payment_frequency = self.file.normalize_input_value(Payment_freq)
        payment_mode_select = self.file.normalize_input_value(payment_mode)

        self.webutils.wait_and_click(ZinniaLive_web_locators.zl_policy_search_tab)
        self.webutils.wait_and_input_text(ZinniaLive_web_locators.policy_search_input, policy_number)
        self.webutils.wait_and_click(ZinniaLive_web_locators.policy_search_btn)
        self.webutils.wait_and_click(ZinniaLive_web_locators.search_result_select)

        if self.webutils.is_element_visible(ZinniaLive_web_locators.policy_tab):
            self.webutils.wait_and_click(ZinniaLive_web_locators.policy_tab)

        elif self.webutils.is_element_visible(ZinniaLive_web_locators.contract_tab):
            self.webutils.wait_and_click(ZinniaLive_web_locators.contract_tab)

        self.webutils.wait_and_click(ZinniaLive_web_locators.withdrawal_tab)

        self.webutils.scroll_down(600)
        self.webutils.wait_and_click(ZinniaLive_web_locators.systematic_manage_autopay_btn)

        self.webutils.wait_and_click(ZinniaLive_web_locators.process_without_document_txt)
        self.webutils.wait_and_click(ZinniaLive_web_locators.continue_btn)

        self.webutils.sleep_time(2)
        self.webutils.scroll_down(500)
        self.webutils.sleep_time(2)
        # self.webutils.wait_and_clear_text_by_press_key(ZinniaLive_web_locators.loan_auto_pay_amount_input)
        # self.webutils.wait_and_input_text(ZinniaLive_web_locators.loan_auto_pay_amount_input, loan_manage_autopay_amt)

        self.webutils.wait_and_click(
            ZinniaLive_web_locators.payment_frequency_radio_btn.format(manage_payment_frequency))
        next_payment_date = self.webutils.get_input_value(ZinniaLive_web_locators.manage_payment_next_payment_date)

        self.webutils.wait_and_click(ZinniaLive_web_locators.continue_btn)

        self.webutils.wait_and_click(ZinniaLive_web_locators.continue_btn)

        self.webutils.scroll_down(400)
        self.webutils.wait_and_click(ZinniaLive_web_locators.autopay_payment_method_continue_btn)

        self.webutils.sleep_time(5)

        # self.validate_new_loan_autopay_details(loan_auto_pay_amount, loan_manage_auto_pay_amount)
        self.validate_manage_next_payment_date(next_payment_date)
        self.validate_old_new_payment_frequency(Payment_frequency, manage_payment_frequency)
        self.validate_payee_name(expected_payee_name)
        format_payment_mode = self.format_payment_mode(payment_mode_select)
        self.validate_payment_method(format_payment_mode)
        self.webutils.scroll_down(300)

        BuiltIn().log("Systematic Withdrawal Update Request Submitted.")
        BuiltIn().log_to_console("Systematic Withdrawal Update Request Submitted.")

        complete_validate_status = ZinniaLive_web_locators.validate_zinnia_complete_status
        nigo_validate_status = ZinniaLive_web_locators.validate_zinnia_nigo_status
        self.webutils.validate_zinniaLive_case_status_1(complete_validate_status, nigo_validate_status)

        # self.webutils.wait_and_click(ZinniaLive_web_locators.submit_payment_btn)
        #
        # expected_loan_status = "Go to case"
        # self.validate_update_systematic_withdrawal_submission(expected_loan_status)
        #
        # self.webutils.sleep_time(30)
        # self.webutils.wait_and_click(ZinniaLive_web_locators.go_to_case_btn)
        #
        # self.webutils.sleep_time(10)
        # lifecycle_date = self.file.get_cst_date("%Y-%m-%d")
        # self.zahara.process_lifecycle_for_systematic_withdrawal_update_processing(policy_number, lifecycle_date)
        #
        # complete_validate_status = ZinniaLive_web_locators.validate_zinnia_complete_status
        # nigo_validate_status = ZinniaLive_web_locators.validate_zinnia_nigo_status
        # self.webutils.validate_zinniaLive_case_status(complete_validate_status, nigo_validate_status)



    @keyword
    def manage_systematic_premium_manage_autopay_process(self,  policy_num, payee_name, loan_autopay_amt, Payment_freq, systematic_premium_update_amount, manage_payment_freq,
                               payment_mode):

        policy_number = self.file.normalize_input_value(policy_num)
        expected_payee_name = self.file.normalize_input_value(payee_name)
        loan_manage_auto_pay_amount = self.file.normalize_input_value(systematic_premium_update_amount)
        manage_payment_frequency = self.file.normalize_input_value(manage_payment_freq)
        loan_auto_pay_amount = self.file.normalize_input_value(loan_autopay_amt)
        Payment_frequency = self.file.normalize_input_value(Payment_freq)
        payment_mode_select = self.file.normalize_input_value(payment_mode)

        self.webutils.wait_and_click(ZinniaLive_web_locators.zl_policy_search_tab)
        self.webutils.wait_and_input_text(ZinniaLive_web_locators.policy_search_input, policy_number)
        self.webutils.wait_and_click(ZinniaLive_web_locators.policy_search_btn)
        self.webutils.wait_and_click(ZinniaLive_web_locators.search_result_select)

        if self.webutils.is_element_visible(ZinniaLive_web_locators.policy_tab):
            self.webutils.wait_and_click(ZinniaLive_web_locators.policy_tab)

        elif self.webutils.is_element_visible(ZinniaLive_web_locators.contract_tab):
            self.webutils.wait_and_click(ZinniaLive_web_locators.contract_tab)

        self.webutils.wait_and_click(ZinniaLive_web_locators.premium_tab)

        self.webutils.scroll_down(500)
        self.webutils.wait_and_click(ZinniaLive_web_locators.systematic_manage_autopay_btn)

        self.webutils.wait_and_click(ZinniaLive_web_locators.process_without_document_txt)
        self.webutils.wait_and_click(ZinniaLive_web_locators.continue_btn)

        self.webutils.sleep_time(2)
        self.webutils.scroll_down(500)
        self.webutils.sleep_time(2)
        # self.webutils.wait_and_clear_text_by_press_key(ZinniaLive_web_locators.loan_auto_pay_amount_input)
        # self.webutils.wait_and_input_text(ZinniaLive_web_locators.loan_auto_pay_amount_input, loan_manage_autopay_amt)

        self.webutils.wait_and_click(
            ZinniaLive_web_locators.payment_frequency_radio_btn.format(manage_payment_frequency))
        next_payment_date = self.webutils.get_input_value(ZinniaLive_web_locators.manage_payment_next_payment_date)

        self.webutils.wait_and_click(ZinniaLive_web_locators.continue_btn)

        self.webutils.wait_and_click(ZinniaLive_web_locators.continue_btn)

        self.webutils.scroll_down(200)
        self.webutils.wait_and_click(ZinniaLive_web_locators.autopay_payment_method_continue_btn)

        self.webutils.sleep_time(5)

        # self.validate_new_loan_autopay_details(loan_auto_pay_amount, loan_manage_auto_pay_amount)
        self.validate_manage_next_payment_date(next_payment_date)
        self.validate_old_new_payment_frequency(Payment_frequency, manage_payment_frequency)
        self.validate_payee_name(expected_payee_name)
        format_payment_mode = self.format_payment_mode(payment_mode_select)
        self.validate_payment_method(format_payment_mode)
        self.webutils.scroll_down(300)

        BuiltIn().log("Systematic Premium Update Request Submitted.")
        BuiltIn().log_to_console("Systematic Premium Update Request Submitted.")

        complete_validate_status = ZinniaLive_web_locators.validate_zinnia_complete_status
        nigo_validate_status = ZinniaLive_web_locators.validate_zinnia_nigo_status
        self.webutils.validate_zinniaLive_case_status_1(complete_validate_status, nigo_validate_status)

        # self.webutils.wait_and_click(ZinniaLive_web_locators.update_premium_autopay_btn)
        #
        # expected_loan_status = "Go to case"
        # self.validate_update_systematic_premium_submission(expected_loan_status)
        #
        # self.webutils.sleep_time(30)
        # self.webutils.wait_and_click(ZinniaLive_web_locators.go_to_case_btn)
        #
        # self.webutils.sleep_time(10)
        # lifecycle_date = self.file.get_cst_date("%Y-%m-%d")
        # self.zahara.process_lifecycle_for_systematic_premium_update_processing(policy_number, lifecycle_date)
        #
        # complete_validate_status = ZinniaLive_web_locators.validate_zinnia_complete_status
        # nigo_validate_status = ZinniaLive_web_locators.validate_zinnia_nigo_status
        # self.webutils.validate_zinniaLive_case_status(complete_validate_status, nigo_validate_status)



    @keyword
    def process_cancel_autoPay(self, policy_num, plan_code):
        policy_number = self.file.normalize_input_value(policy_num)

        self.webutils.wait_and_click(ZinniaLive_web_locators.zl_policy_search_tab)
        self.webutils.wait_and_input_text(ZinniaLive_web_locators.policy_search_input, policy_number)
        self.webutils.wait_and_click(ZinniaLive_web_locators.policy_search_btn)
        self.webutils.wait_and_click(ZinniaLive_web_locators.search_result_select)

        if self.webutils.is_element_visible(ZinniaLive_web_locators.policy_tab):
            self.webutils.wait_and_click(ZinniaLive_web_locators.policy_tab)

        elif self.webutils.is_element_visible(ZinniaLive_web_locators.contract_tab):
            self.webutils.wait_and_click(ZinniaLive_web_locators.contract_tab)

        self.webutils.wait_and_click(ZinniaLive_web_locators.loans_tab)

        self.webutils.scroll_down(800)
        self.webutils.wait_and_click(ZinniaLive_web_locators.cancel_autopay_btn)

        self.webutils.wait_and_click(ZinniaLive_web_locators.process_without_document_txt)
        self.webutils.wait_and_click(ZinniaLive_web_locators.cancel_autopay_checkbox)

        BuiltIn().log("Systematic Loan Repayment Cancel Request Submitted.")
        BuiltIn().log_to_console("Systematic Loan Repayment Cancel Request Submitted.")

        complete_validate_status = ZinniaLive_web_locators.validate_zinnia_complete_status
        nigo_validate_status = ZinniaLive_web_locators.validate_zinnia_nigo_status
        self.webutils.validate_zinniaLive_case_status_1(complete_validate_status, nigo_validate_status)

        # self.webutils.wait_and_click(ZinniaLive_web_locators.cancel_autppay_btn)
        #
        # expected_loan_status = "Go to case"
        # self.validate_cancel_loan_autopay_submission(expected_loan_status)
        #
        # self.webutils.sleep_time(30)
        # self.webutils.wait_and_click(ZinniaLive_web_locators.go_to_case_btn)
        #
        # self.webutils.sleep_time(5)
        # lifecycle_date = self.file.get_cst_date("%Y-%m-%d")
        # self.zahara.process_lifecycle_post_loan_repayment_processing(policy_number, lifecycle_date, plan_code)
        #
        # complete_validate_status = ZinniaLive_web_locators.validate_zinnia_complete_status
        # nigo_validate_status = ZinniaLive_web_locators.validate_zinnia_nigo_status
        # self.webutils.validate_zinniaLive_case_status(complete_validate_status, nigo_validate_status)



    @keyword
    def process_cancel_systematic_rmd_autoPay(self, policy_num, plan_code):
        policy_number = self.file.normalize_input_value(policy_num)

        self.webutils.wait_and_click(ZinniaLive_web_locators.zl_policy_search_tab)
        self.webutils.wait_and_input_text(ZinniaLive_web_locators.policy_search_input, policy_number)
        self.webutils.wait_and_click(ZinniaLive_web_locators.policy_search_btn)
        self.webutils.wait_and_click(ZinniaLive_web_locators.search_result_select)

        if self.webutils.is_element_visible(ZinniaLive_web_locators.policy_tab):
            self.webutils.wait_and_click(ZinniaLive_web_locators.policy_tab)

        elif self.webutils.is_element_visible(ZinniaLive_web_locators.contract_tab):
            self.webutils.wait_and_click(ZinniaLive_web_locators.contract_tab)

        self.webutils.wait_and_click(ZinniaLive_web_locators.withdrawal_tab)

        self.webutils.scroll_down(800)
        self.webutils.wait_and_click(ZinniaLive_web_locators.cancel_autopay_btn)

        self.webutils.wait_and_click(ZinniaLive_web_locators.process_without_document_txt)
        self.webutils.wait_and_click(ZinniaLive_web_locators.cancel_autopay_checkbox)

        BuiltIn().log("Systematic Loan RMD Cancel Request Submitted.")
        BuiltIn().log_to_console("Systematic Loan RMD cancel Request Submitted.")

        complete_validate_status = ZinniaLive_web_locators.validate_zinnia_complete_status
        nigo_validate_status = ZinniaLive_web_locators.validate_zinnia_nigo_status
        self.webutils.validate_zinniaLive_case_status_1(complete_validate_status, nigo_validate_status)

        # self.webutils.wait_and_click(ZinniaLive_web_locators.cancel_autppay_btn)
        #
        # expected_loan_status = "Go to case"
        # self.validate_cancel_systematic_rmd__autopay_submission(expected_loan_status)
        #
        # self.webutils.sleep_time(30)
        # self.webutils.wait_and_click(ZinniaLive_web_locators.go_to_case_btn)
        #
        # self.webutils.sleep_time(5)
        # lifecycle_date = self.file.get_cst_date("%Y-%m-%d")
        # self.zahara.process_lifecycle_systematic_rmd_autopay_cancel_processing(policy_number, lifecycle_date, plan_code)
        #
        # complete_validate_status = ZinniaLive_web_locators.validate_zinnia_complete_status
        # nigo_validate_status = ZinniaLive_web_locators.validate_zinnia_nigo_status
        # self.webutils.validate_zinniaLive_case_status(complete_validate_status, nigo_validate_status)


    @keyword
    def process_cancel_systematic_withdrawal_autoPay(self, policy_num, plan_code):
        policy_number = self.file.normalize_input_value(policy_num)

        self.webutils.wait_and_click(ZinniaLive_web_locators.zl_policy_search_tab)
        self.webutils.wait_and_input_text(ZinniaLive_web_locators.policy_search_input, policy_number)
        self.webutils.wait_and_click(ZinniaLive_web_locators.policy_search_btn)
        self.webutils.wait_and_click(ZinniaLive_web_locators.search_result_select)

        if self.webutils.is_element_visible(ZinniaLive_web_locators.policy_tab):
            self.webutils.wait_and_click(ZinniaLive_web_locators.policy_tab)

        elif self.webutils.is_element_visible(ZinniaLive_web_locators.contract_tab):
            self.webutils.wait_and_click(ZinniaLive_web_locators.contract_tab)

        self.webutils.wait_and_click(ZinniaLive_web_locators.withdrawal_tab)

        self.webutils.scroll_down(600)
        self.webutils.wait_and_click(ZinniaLive_web_locators.cancel_autopay_btn)

        self.webutils.wait_and_click(ZinniaLive_web_locators.process_without_document_txt)
        self.webutils.wait_and_click(ZinniaLive_web_locators.cancel_autopay_checkbox)

        BuiltIn().log("Systematic Withdrawal Cancel Request Submitted.")
        BuiltIn().log_to_console("Systematic Withdrawal Cancel Request Submitted.")

        complete_validate_status = ZinniaLive_web_locators.validate_zinnia_complete_status
        nigo_validate_status = ZinniaLive_web_locators.validate_zinnia_nigo_status
        self.webutils.validate_zinniaLive_case_status_1(complete_validate_status, nigo_validate_status)

        # self.webutils.wait_and_click(ZinniaLive_web_locators.cancel_autppay_btn)
        #
        # expected_loan_status = "Go to case"
        # self.validate_cancel_systematic_withdrawal_autopay_submission(expected_loan_status)
        #
        # self.webutils.sleep_time(30)
        # self.webutils.wait_and_click(ZinniaLive_web_locators.go_to_case_btn)
        #
        # self.webutils.sleep_time(5)
        # lifecycle_date = self.file.get_cst_date("%Y-%m-%d")
        # self.zahara.process_lifecycle_systematic_withdrawal_autopay_cancel_processing(policy_number, lifecycle_date, plan_code)
        #
        # complete_validate_status = ZinniaLive_web_locators.validate_zinnia_complete_status
        # nigo_validate_status = ZinniaLive_web_locators.validate_zinnia_nigo_status
        # self.webutils.validate_zinniaLive_case_status(complete_validate_status, nigo_validate_status)



    @keyword
    def validate_fix_fund_allocation_percent(self, expected_fix_fund_allocation_percent):
        locator = ZinniaLive_web_locators.validate_fix_fund_allocation_percent.format(expected_fix_fund_allocation_percent)
        self.webutils.wait_until_element_visible(locator, timeout=60)
        actual_fix_fund_allocation_percent = self.webutils.get_text(locator)

        if expected_fix_fund_allocation_percent != actual_fix_fund_allocation_percent:
            raise AssertionError(
                f"Fix fund allocation percentage mismatch on submission page! Expected: '{expected_fix_fund_allocation_percent}', Actual: '{actual_fix_fund_allocation_percent}'")
        BuiltIn().log(
            f"Fix fund allocation percentage match on submission page! Expected: '{expected_fix_fund_allocation_percent}', Actual: '{actual_fix_fund_allocation_percent}'")
        BuiltIn().log_to_console(
            f"Fix fund allocation percentage match on submission page! Expected: '{expected_fix_fund_allocation_percent}', Actual: '{actual_fix_fund_allocation_percent}'")


    @keyword
    def validate_cap_account_allocation_percent(self, expected_cap_account_allocation_percent):
        locator = ZinniaLive_web_locators.validate_fix_fund_allocation_percent.format(expected_cap_account_allocation_percent)
        self.webutils.wait_until_element_visible(locator, timeout=60)
        actual_cap_account_allocation_percent = self.webutils.get_text(locator)

        if expected_cap_account_allocation_percent != actual_cap_account_allocation_percent:
            raise AssertionError(
                f"Cap account allocation percentage mismatch on submission page! Expected: '{expected_cap_account_allocation_percent}', Actual: '{actual_cap_account_allocation_percent}'")
        BuiltIn().log(
            f"Cap account allocation percentage match on submission page! Expected: '{expected_cap_account_allocation_percent}', Actual: '{actual_cap_account_allocation_percent}'")
        BuiltIn().log_to_console(
            f"Cap account allocation percentage match on submission page! Expected: '{expected_cap_account_allocation_percent}', Actual: '{actual_cap_account_allocation_percent}'")

    @keyword
    def validate_participation_rate_account_allocation_percent(self, expected_participation_rate_account_allocation_percent):
        locator = ZinniaLive_web_locators.validate_fix_fund_allocation_percent.format(expected_participation_rate_account_allocation_percent)
        self.webutils.wait_until_element_visible(locator, timeout=60)
        actual_participation_rate_account_allocation_percent = self.webutils.get_text(locator)

        if expected_participation_rate_account_allocation_percent != actual_participation_rate_account_allocation_percent:
            raise AssertionError(
                f"Participation rate account allocation percentage mismatch on submission page! Expected: '{expected_participation_rate_account_allocation_percent}', Actual: '{actual_participation_rate_account_allocation_percent}'")
        BuiltIn().log(
            f"Participation rate account allocation percentage match on submission page! Expected: '{expected_participation_rate_account_allocation_percent}', Actual: '{actual_participation_rate_account_allocation_percent}'")
        BuiltIn().log_to_console(
            f"Participation rate account allocation percentage match on submission page! Expected: '{expected_participation_rate_account_allocation_percent}', Actual: '{actual_participation_rate_account_allocation_percent}'")


    @keyword
    def process_fund_allocation(self, policy_num, expected_fix_fund_allocation, expected_cap_account_allocation, expected_participation_rate_account_allocation, client_plan_code):
        policy_number = self.file.normalize_input_value(policy_num)
        plan_code = self.file.normalize_input_value(client_plan_code)
        expected_fix_fund_allocation_percent = self.file.normalize_input_value(expected_fix_fund_allocation)
        expected_cap_account_allocation_percent = self.file.normalize_input_value(expected_cap_account_allocation)
        expected_participation_rate_account_allocation_percent = self.file.normalize_input_value(expected_participation_rate_account_allocation)

        self.webutils.wait_and_click(ZinniaLive_web_locators.zl_policy_search_tab)
        self.webutils.wait_and_input_text(ZinniaLive_web_locators.policy_search_input, policy_number)
        self.webutils.wait_and_click(ZinniaLive_web_locators.policy_search_btn)
        self.webutils.wait_and_click(ZinniaLive_web_locators.search_result_select)

        if self.webutils.is_element_visible(ZinniaLive_web_locators.policy_tab):
            self.webutils.wait_and_click(ZinniaLive_web_locators.policy_tab)

        elif self.webutils.is_element_visible(ZinniaLive_web_locators.contract_tab):
            self.webutils.wait_and_click(ZinniaLive_web_locators.contract_tab)

        self.webutils.wait_and_click(ZinniaLive_web_locators.fund_account_tab)
        self.webutils.sleep_time(3)
        self.webutils.scroll_down(500)
        self.webutils.sleep_time(3)

        self.webutils.wait_and_click(ZinniaLive_web_locators.edit_allocation_btn)

        self.webutils.wait_and_click(ZinniaLive_web_locators.process_without_document_txt)
        self.webutils.wait_and_clear_text_by_press_key(ZinniaLive_web_locators.fix_fund_allocation_percent)
        self.webutils.wait_and_input_text(ZinniaLive_web_locators.test, expected_fix_fund_allocation_percent)
        self.webutils.wait_and_clear_text_by_press_key(ZinniaLive_web_locators.cap_amount_allocation_percent)
        self.webutils.wait_and_input_text(ZinniaLive_web_locators.test1, expected_cap_account_allocation_percent)
        self.webutils.wait_and_clear_text_by_press_key(ZinniaLive_web_locators.participation_allocation_rate_percent)
        self.webutils.wait_and_input_text(ZinniaLive_web_locators.test2, expected_participation_rate_account_allocation_percent)
        self.webutils.wait_and_click(ZinniaLive_web_locators.update_allocation_btn)

        self.validate_fix_fund_allocation_percent(expected_fix_fund_allocation_percent)
        self.validate_cap_account_allocation_percent(expected_cap_account_allocation_percent)
        self.validate_participation_rate_account_allocation_percent(expected_participation_rate_account_allocation_percent)
        self.webutils.wait_and_click(ZinniaLive_web_locators.allocation_submit_btn)

        expected_loan_status = "Go to case"
        self.validate_fund_allocation_submission(expected_loan_status)

        self.webutils.sleep_time(30)
        self.webutils.wait_and_click(ZinniaLive_web_locators.go_to_case_btn)

        self.webutils.sleep_time(5)
        lifecycle_date = self.file.get_cst_date("%Y-%m-%d")
        self.zahara.process_lifecycle_for_fund_allocation_processing(policy_number, lifecycle_date, plan_code)

        complete_validate_status = ZinniaLive_web_locators.validate_zinnia_complete_status
        nigo_validate_status = ZinniaLive_web_locators.validate_zinnia_nigo_status
        self.webutils.validate_zinniaLive_case_status(complete_validate_status, nigo_validate_status)


    @keyword
    def process_communication_preference_change(self, policy_num, client_plan_code, preferred_communication_type):
        policy_number = self.file.normalize_input_value(policy_num)
        plan_code = self.file.normalize_input_value(client_plan_code)
        preferred_com_type = self.file.normalize_input_value(preferred_communication_type)

        self.webutils.wait_and_click(ZinniaLive_web_locators.zl_policy_search_tab)
        self.webutils.wait_and_input_text(ZinniaLive_web_locators.policy_search_input, policy_number)
        self.webutils.wait_and_click(ZinniaLive_web_locators.policy_search_btn)
        self.webutils.wait_and_click(ZinniaLive_web_locators.search_result_select)

        self.webutils.wait_and_click(ZinniaLive_web_locators.people_tab)

        self.webutils.wait_and_click(ZinniaLive_web_locators.owner_tab_select)
        self.webutils.wait_and_click(ZinniaLive_web_locators.people_owner_payee_select)
        self.webutils.wait_and_click(ZinniaLive_web_locators.communication_edit_btn)

        self.webutils.wait_and_click(ZinniaLive_web_locators.process_without_document_txt)

        if preferred_com_type in ["email"]:
            self.webutils.wait_and_click(ZinniaLive_web_locators.email_com_select)

        elif preferred_com_type in ["address"]:
            self.webutils.wait_and_click(ZinniaLive_web_locators.residence_com_select)

        BuiltIn().log("Communication change Request Submitted.")
        BuiltIn().log_to_console("Communication Change Request Submitted.")

        # complete_validate_status = ZinniaLive_web_locators.validate_zinnia_complete_status
        # nigo_validate_status = ZinniaLive_web_locators.validate_zinnia_nigo_status
        # self.webutils.validate_zinniaLive_case_status_1(complete_validate_status, nigo_validate_status)

        # self.webutils.wait_and_click(ZinniaLive_web_locators.preferred_comm_type)
        #
        # expected_loan_status = "Go to case"
        # self.validate_preferred_communication_change_submission(expected_loan_status)
        #
        # self.webutils.sleep_time(30)
        # self.webutils.wait_and_click(ZinniaLive_web_locators.go_to_case_btn)
        #
        # self.webutils.sleep_time(5)
        # lifecycle_date = self.file.get_cst_date("%Y-%m-%d")
        # self.zahara.process_lifecycle_for_fund_allocation_processing(policy_number, lifecycle_date, plan_code)
        #
        # complete_validate_status = ZinniaLive_web_locators.validate_zinnia_complete_status
        # nigo_validate_status = ZinniaLive_web_locators.validate_zinnia_nigo_status
        # self.webutils.validate_zinniaLive_case_status(complete_validate_status, nigo_validate_status)



    @keyword
    def process_bene_change_term(self, policy_num, client_plan_code):
        policy_number = self.file.normalize_input_value(policy_num)
        plan_code = self.file.normalize_input_value(client_plan_code)

        self.webutils.wait_and_click(ZinniaLive_web_locators.zl_policy_search_tab)
        self.webutils.wait_and_input_text(ZinniaLive_web_locators.policy_search_input, policy_number)
        self.webutils.wait_and_click(ZinniaLive_web_locators.policy_search_btn)
        self.webutils.wait_and_click(ZinniaLive_web_locators.search_result_select)

        self.webutils.wait_and_click(ZinniaLive_web_locators.people_tab)

        self.webutils.wait_and_click(ZinniaLive_web_locators.bene_tab_select)
        self.webutils.sleep_time(5)
        self.webutils.wait_and_click(ZinniaLive_web_locators.manage_bene_select)

        self.webutils.wait_and_click(ZinniaLive_web_locators.process_without_document_txt)
        self.webutils.scroll_down(100)
        self.webutils.wait_and_click(ZinniaLive_web_locators.continue_doc_btn)

        self.webutils.scroll_down(500)
        self.webutils.wait_and_click(ZinniaLive_web_locators.continue_btn)

        self.webutils.wait_and_click(ZinniaLive_web_locators.primary_bene_extend)
        # self.webutils.scroll_down(500)
        self.webutils.wait_and_input_text(ZinniaLive_web_locators.middle_name_bene_change_inout, "kumar")
        self.webutils.scroll_down(1000)
        self.webutils.wait_and_click(ZinniaLive_web_locators.continue_btn)

        self.webutils.wait_and_click(ZinniaLive_web_locators.designation_select)
        self.webutils.wait_and_click(ZinniaLive_web_locators.assignee_select)
        self.webutils.wait_and_click(ZinniaLive_web_locators.sign_present_select)
        self.webutils.wait_and_click(ZinniaLive_web_locators.sign_present_slct)
        self.webutils.wait_and_click(ZinniaLive_web_locators.continue_button)
        sign_current_date = self.file.get_current_date_format_windows_with_two_digit()
        self.webutils.wait_and_input_text(ZinniaLive_web_locators.sign_date_input, sign_current_date)
        self.webutils.sleep_time(5)
        self.webutils.scroll_up(500)
        self.webutils.wait_and_click(ZinniaLive_web_locators.select_signature_tab)

        self.webutils.wait_and_click(ZinniaLive_web_locators.continue_button)

        self.webutils.sleep_time(5)

        BuiltIn().log("Bene Chnage Request Submitted.")
        BuiltIn().log_to_console("Bene Change Request Submitted.")

        complete_validate_status = ZinniaLive_web_locators.validate_zinnia_complete_status
        nigo_validate_status = ZinniaLive_web_locators.validate_zinnia_nigo_status
        self.webutils.validate_zinniaLive_case_status_1(complete_validate_status, nigo_validate_status)

        # self.webutils.wait_and_click(ZinniaLive_web_locators.continue_button)
        #
        # expected_loan_status = "Go to case"
        # self.validate_bene_change_submission(expected_loan_status)
        #
        # self.webutils.sleep_time(30)
        # self.webutils.wait_and_click(ZinniaLive_web_locators.go_to_case_btn)
        #
        # self.webutils.sleep_time(5)
        # lifecycle_date = self.file.get_cst_date("%Y-%m-%d")
        # self.zahara.process_lifecycle_for_bene_change_processing(policy_number, lifecycle_date, plan_code)
        #
        # complete_validate_status = ZinniaLive_web_locators.validate_zinnia_complete_status
        # nigo_validate_status = ZinniaLive_web_locators.validate_zinnia_nigo_status
        # self.webutils.validate_zinniaLive_case_status(complete_validate_status, nigo_validate_status)


    @keyword
    def process_fund_transfer(self, policy_num, trans_amount, client_plan_code):
        policy_number = self.file.normalize_input_value(policy_num)
        transfer_amount = self.file.normalize_input_value(trans_amount)

        self.webutils.wait_and_click(ZinniaLive_web_locators.zl_policy_search_tab)

        self.webutils.wait_and_input_text(ZinniaLive_web_locators.policy_search_input, policy_number)
        self.webutils.wait_and_click(ZinniaLive_web_locators.policy_search_btn)
        self.webutils.wait_and_click(ZinniaLive_web_locators.search_result_select)

        if self.webutils.is_element_visible(ZinniaLive_web_locators.policy_tab):
            self.webutils.wait_and_click(ZinniaLive_web_locators.policy_tab)

        elif self.webutils.is_element_visible(ZinniaLive_web_locators.contract_tab):
            self.webutils.wait_and_click(ZinniaLive_web_locators.contract_tab)

        self.webutils.wait_and_click(ZinniaLive_web_locators.fund_account_tab)

        self.webutils.wait_and_click(ZinniaLive_web_locators.transfer_fund_value_btn)

        self.webutils.scroll_down(300)
        self.webutils.sleep_time(2)
        self.webutils.wait_and_click(ZinniaLive_web_locators.process_without_document_txt)
        self.webutils.wait_and_click(ZinniaLive_web_locators.continue_btn)

        enter_loan_effective_date = self.webutils.get_input_value(ZinniaLive_web_locators.start_loan_effective_date)
        self.webutils.sleep_time(2)
        self.webutils.scroll_down(300)
        self.webutils.sleep_time(2)
        self.webutils.wait_and_click(ZinniaLive_web_locators.transfer_form_fund_select)
        self.webutils.wait_and_click(ZinniaLive_web_locators.transfer_cap_account_select)
        expected_transfer_from_form = self.webutils.get_text(ZinniaLive_web_locators.transfer_cap_account_select)
        self.webutils.wait_and_input_text(ZinniaLive_web_locators.transfer_from_amount_input, transfer_amount)

        self.webutils.wait_and_click(ZinniaLive_web_locators.transfer_to_fund_select)
        self.webutils.wait_and_click(ZinniaLive_web_locators.transfer_to_rate_account_select)
        expected_transfer_to_form = self.webutils.get_text(ZinniaLive_web_locators.transfer_to_rate_account_select)

        self.webutils.wait_and_input_text(ZinniaLive_web_locators.transfer_to_amount_input, transfer_amount)
        self.webutils.wait_and_click(ZinniaLive_web_locators.continue_button)

        expected_date = self.file.date_format_as_remove_zero_from_date_month(enter_loan_effective_date)
        self.validate_effective_date(expected_date)
        self.validate_transfer_from_and_transfer_to_account(expected_transfer_from_form, expected_transfer_to_form)

        BuiltIn().log("Fund Transfer Request Submitted.")
        BuiltIn().log_to_console("Fund Transfer Request Submitted.")

        # complete_validate_status = ZinniaLive_web_locators.validate_zinnia_complete_status
        # nigo_validate_status = ZinniaLive_web_locators.validate_zinnia_nigo_status
        # self.webutils.validate_zinniaLive_case_status_1(complete_validate_status, nigo_validate_status)


        # self.webutils.wait_and_click(ZinniaLive_web_locators.continue_button)
        #
        # expected_loan_status = "Go to case"
        # self.validate_fund_transfer_submission(expected_loan_status)
        #
        # self.webutils.sleep_time(30)
        # self.webutils.wait_and_click(ZinniaLive_web_locators.go_to_case_btn)

        # self.webutils.sleep_time(10)
        # lifecycle_date = self.file.get_cst_date("%Y-%m-%d")
        # self.zahara.process_lifecycle_for_fund_transfer_processing(policy_number, lifecycle_date, client_plan_code)
        #
        # complete_validate_status = ZinniaLive_web_locators.validate_zinnia_complete_status
        # nigo_validate_status = ZinniaLive_web_locators.validate_zinnia_nigo_status
        # self.webutils.validate_zinniaLive_case_status(complete_validate_status, nigo_validate_status)


    @keyword
    def process_one_time_loan_repayment(self, policy_number, expected_payee_name, loan_repayment_amt, payment_mode,
                                        acc_name, acc_number, plan_code):
        BuiltIn().log("Perform New One-Time Loan Repayment Process")
        BuiltIn().log_to_console("Perform New One-Time Loan Repayment Process")
        BuiltIn().log("-----------------------------------------------------------")
        BuiltIn().log_to_console("-----------------------------------------------------------")
        loan_repayment_amount = self.file.normalize_input_value(loan_repayment_amt)
        expected_payment_method = self.file.normalize_input_value(payment_mode)
        expected_account_name = self.file.normalize_input_value(acc_name)
        expected_account_number = self.file.normalize_input_value(acc_number)
        client_plan_code = self.file.normalize_input_value(plan_code)

        self.webutils.wait_and_click(ZinniaLive_web_locators.zl_policy_search_tab)
        self.webutils.wait_and_input_text(ZinniaLive_web_locators.policy_search_input, policy_number)
        self.webutils.wait_and_click(ZinniaLive_web_locators.policy_search_btn)
        self.webutils.wait_and_click(ZinniaLive_web_locators.search_result_select)

        if self.webutils.is_element_visible(ZinniaLive_web_locators.policy_tab):
            self.webutils.wait_and_click(ZinniaLive_web_locators.policy_tab)

        elif self.webutils.is_element_visible(ZinniaLive_web_locators.contract_tab):
            self.webutils.wait_and_click(ZinniaLive_web_locators.contract_tab)

        self.webutils.wait_and_click(ZinniaLive_web_locators.loans_tab)

        self.webutils.scroll_down(800)
        self.webutils.wait_and_click(ZinniaLive_web_locators.one_time_loan_repayment_btn)
        self.webutils.scroll_down(1000)
        self.webutils.wait_and_click(ZinniaLive_web_locators.process_without_document_txt)
        self.webutils.wait_and_click(ZinniaLive_web_locators.continue_btn)
        self.webutils.wait_and_input_text(ZinniaLive_web_locators.one_time_loan_payment_input, loan_repayment_amount)
        self.webutils.wait_and_click(ZinniaLive_web_locators.continue_btn)

        self.webutils.wait_and_click(ZinniaLive_web_locators.continue_btn)
        self.webutils.wait_and_click(ZinniaLive_web_locators.onr_time_payment_method_continue_btn)

        self.validate_loan_amount(loan_repayment_amount)
        expected_date = self.file.get_current_date_format_windows()
        self.validate_effective_date(expected_date)

        self.validate_payee_name(expected_payee_name)
        self.webutils.scroll_down(1000)

        format_payment_mode = self.format_payment_mode(expected_payment_method)
        self.validate_payment_method(format_payment_mode)
        self.validate_account_name_and_number(expected_account_name, expected_account_number)
        self.webutils.wait_and_click(ZinniaLive_web_locators.one_time_submit_payment_btn)

        expected_loan_status = "Go to case"
        self.validate_one_type_loan__repayment_submission(expected_loan_status)

        self.webutils.sleep_time(30)
        self.webutils.wait_and_click(ZinniaLive_web_locators.go_to_case_btn)

        self.webutils.sleep_time(5)
        lifecycle_date = self.file.get_cst_date("%Y-%m-%d")
        self.zahara.process_lifecycle_post_loan_repayment_processing(policy_number, lifecycle_date, client_plan_code)

        complete_validate_status = ZinniaLive_web_locators.validate_zinnia_complete_status
        nigo_validate_status = ZinniaLive_web_locators.validate_zinnia_nigo_status
        self.webutils.validate_zinniaLive_case_status(complete_validate_status, nigo_validate_status)


    @keyword
    def process_one_time_loan_repayment_complete_flow(self, old_xml_name, expect_poly_status, start_loan_amount,
                                                      loan_repayment_amount, payment_mode_select,
                                                      expected_fund_allocation_type, expected_account_name,
                                                      expected_account_number, client, client_plan_code):
        policy_number, expected_payee_name = self.zahara.create_policy(old_xml_name, expect_poly_status, client, client_plan_code)


        self.login_to_zinnia_live_and_start_a_loan(policy_number, expected_payee_name, start_loan_amount, payment_mode_select,
                                                   expected_fund_allocation_type, expected_account_name,
                                                   expected_account_number, client_plan_code)

        self.process_one_time_loan_repayment(policy_number, expected_payee_name, loan_repayment_amount, payment_mode_select,
                                                                      expected_account_name, expected_account_number, client_plan_code)

    @keyword
    def process_loan_autoPay_complete_flow(self, old_xml_name, expect_poly_status, start_loan_amount, loan_autopay_amt,
                                           Payment_freq, payment_mode_select, expected_fund_allocation_type,
                                           expected_account_name, expected_account_number, client, plan_code):
        policy_number, expected_payee_name = self.zahara.create_policy(old_xml_name, expect_poly_status, client, plan_code)

        self.login_to_zinnia_live_and_start_a_loan(policy_number, expected_payee_name, start_loan_amount, payment_mode_select,
                                                   expected_fund_allocation_type, expected_account_name,
                                                   expected_account_number, plan_code)
        self.process_setup_autoPay_repayment(policy_number, expected_payee_name, loan_autopay_amt, Payment_freq, expected_account_name, payment_mode_select,
                                             expected_account_number, plan_code)


    @keyword
    def login_to_zinnia_live_and_process_cancel_loan_auto_pay(self, policy_number, plan_code):
        BuiltIn().log("Perform Systematic Loan Repayment Cancel AutoPay Process")
        BuiltIn().log_to_console("Perform Systematic Loan Repayment Cancel AutoPay Process")
        BuiltIn().log("-----------------------------------------------------------")
        BuiltIn().log_to_console("-----------------------------------------------------------")

        self.webutils.open_browser_with_url(ZinniaLive.url, ZinniaLive.browser)
        user_id = self.read_config.getValueByKey('zinnia_live_user_email')
        self.webutils.wait_and_input_text(ZinniaLive_web_locators.zl_user_input, user_id)
        self.webutils.wait_and_click(ZinniaLive_web_locators.zl_user_submit_btn)
        self.process_cancel_autoPay(policy_number, plan_code)

        if self.webutils.is_element_visible(ZinniaLive_web_locators.zl_user_pass_input):
            user_pass = self.read_config.getValueByKey('zinnia_live_pass')
            self.webutils.wait_and_input_text(ZinniaLive_web_locators.zl_user_pass_input, user_pass)
            self.webutils.wait_and_click(ZinniaLive_web_locators.zl_user_pass_submit_btn)
            self.process_cancel_autoPay(policy_number, plan_code)

    @keyword
    def login_to_zinnia_live_and_process_systematic_rmd_cancel_loan_auto_pay(self, policy_number, plan_code):
        BuiltIn().log("Perform Systematic RMD Cancel AutoPay Process")
        BuiltIn().log_to_console("Perform Systematic RMD Cancel AutoPay Process")
        BuiltIn().log("-----------------------------------------------------------")
        BuiltIn().log_to_console("-----------------------------------------------------------")

        self.webutils.open_browser_with_url(ZinniaLive.url, ZinniaLive.browser)
        user_id = self.read_config.getValueByKey('zinnia_live_user_email')
        self.webutils.wait_and_input_text(ZinniaLive_web_locators.zl_user_input, user_id)
        self.webutils.wait_and_click(ZinniaLive_web_locators.zl_user_submit_btn)
        self.process_cancel_systematic_rmd_autoPay(policy_number, plan_code)

        if self.webutils.is_element_visible(ZinniaLive_web_locators.zl_user_pass_input):
            user_pass = self.read_config.getValueByKey('zinnia_live_pass')
            self.webutils.wait_and_input_text(ZinniaLive_web_locators.zl_user_pass_input, user_pass)
            self.webutils.wait_and_click(ZinniaLive_web_locators.zl_user_pass_submit_btn)
            self.process_cancel_systematic_rmd_autoPay(policy_number, plan_code)

    @keyword
    def login_to_zinnia_live_and_process_systematic_withdrawal_cancel_loan_auto_pay(self, policy_number, plan_code):
        BuiltIn().log("Perform Systematic Withdrawal Cancel AutoPay Process")
        BuiltIn().log_to_console("Perform Systematic Withdrawal Cancel AutoPay Process")
        BuiltIn().log("-----------------------------------------------------------")
        BuiltIn().log_to_console("-----------------------------------------------------------")

        self.webutils.open_browser_with_url(ZinniaLive.url, ZinniaLive.browser)
        user_id = self.read_config.getValueByKey('zinnia_live_user_email')
        self.webutils.wait_and_input_text(ZinniaLive_web_locators.zl_user_input, user_id)
        self.webutils.wait_and_click(ZinniaLive_web_locators.zl_user_submit_btn)
        self.process_cancel_systematic_withdrawal_autoPay(policy_number, plan_code)

        if self.webutils.is_element_visible(ZinniaLive_web_locators.zl_user_pass_input):
            user_pass = self.read_config.getValueByKey('zinnia_live_pass')
            self.webutils.wait_and_input_text(ZinniaLive_web_locators.zl_user_pass_input, user_pass)
            self.webutils.wait_and_click(ZinniaLive_web_locators.zl_user_pass_submit_btn)
            self.process_cancel_systematic_withdrawal_autoPay(policy_number, plan_code)

    @keyword
    def login_to_zinnia_live_and_process_fund_allocation_flow(self, policy_number, expected_fix_fund_allocation_percent, expected_cap_account_allocation_percent, expected_participation_rate_account_allocation_percent, client_plan_code):
        BuiltIn().log("Perform Fund Allocation Process")
        BuiltIn().log_to_console("Perform Fund Allocation Process")
        BuiltIn().log("-----------------------------------------------------------")
        BuiltIn().log_to_console("-----------------------------------------------------------")

        self.webutils.open_browser_with_url(ZinniaLive.url, ZinniaLive.browser)
        user_id = self.read_config.getValueByKey('zinnia_live_user_email')
        self.webutils.wait_and_input_text(ZinniaLive_web_locators.zl_user_input, user_id)
        self.webutils.wait_and_click(ZinniaLive_web_locators.zl_user_submit_btn)
        
        # Handle password authentication if required
        if self.webutils.is_element_visible(ZinniaLive_web_locators.zl_user_pass_input):
            user_pass = self.read_config.getValueByKey('zinnia_live_pass')
            self.webutils.wait_and_input_text(ZinniaLive_web_locators.zl_user_pass_input, user_pass)
            self.webutils.wait_and_click(ZinniaLive_web_locators.zl_user_pass_submit_btn)
        
        # Process fund allocation after authentication is complete
        self.process_fund_allocation(policy_number, expected_fix_fund_allocation_percent, expected_cap_account_allocation_percent, expected_participation_rate_account_allocation_percent, client_plan_code)
        
        # Close browser after process is complete


    @keyword
    def login_to_zinnia_live_and_process_communication_preference_change_flow(self, policy_number, client_plan_code, preferred_communication_type):
        BuiltIn().log("Perform Communication Preference change Process")
        BuiltIn().log_to_console("Perform Communication Preference change Process")
        BuiltIn().log("-----------------------------------------------------------")
        BuiltIn().log_to_console("-----------------------------------------------------------")

        self.webutils.open_browser_with_url(ZinniaLive.url, ZinniaLive.browser)
        user_id = self.read_config.getValueByKey('zinnia_live_user_email')
        self.webutils.wait_and_input_text(ZinniaLive_web_locators.zl_user_input, user_id)
        self.webutils.wait_and_click(ZinniaLive_web_locators.zl_user_submit_btn)
        self.process_communication_preference_change(policy_number, client_plan_code, preferred_communication_type)

        if self.webutils.is_element_visible(ZinniaLive_web_locators.zl_user_pass_input):
            user_pass = self.read_config.getValueByKey('zinnia_live_pass')
            self.webutils.wait_and_input_text(ZinniaLive_web_locators.zl_user_pass_input, user_pass)
            self.webutils.wait_and_click(ZinniaLive_web_locators.zl_user_pass_submit_btn)
            self.process_communication_preference_change(policy_number, client_plan_code, preferred_communication_type)


    @keyword
    def process_multi_phone_change_flow(self, old_xml_name, expect_poly_status, client, client_plan_code):
        BuiltIn().log("Perform Multi Phone change Process")
        BuiltIn().log_to_console("Perform Multi Phone change Process")
        BuiltIn().log("-----------------------------------------------------------")
        BuiltIn().log_to_console("-----------------------------------------------------------")

        policy_number, expected_payee_name = self.zahara.create_policy_with_effective_date(old_xml_name,
                                                                                           expect_poly_status, client,
                                                                                           client_plan_code)


        token = self.zahara_api.get_access_token()
        client_code = self.file.normalize_input_value(client_plan_code)
        self.zahara_api.update_party_phones(client_code, policy_number, token)

        self.zahara.login_to_zahara_and_perform_transaction_process(policy_number, client_code, expect_poly_status)

    @keyword
    def process_multi_email_change_flow(self, old_xml_name, expect_poly_status, client, client_plan_code):
        BuiltIn().log("Perform Multi Email change Process")
        BuiltIn().log_to_console("Perform Multi Email change Process")
        BuiltIn().log("-----------------------------------------------------------")
        BuiltIn().log_to_console("-----------------------------------------------------------")

        policy_number, expected_payee_name = self.zahara.create_policy_with_effective_date(old_xml_name, expect_poly_status, client, client_plan_code)

        token = self.zahara_api.get_access_token()
        client_code = self.file.normalize_input_value(client_plan_code)
        self.zahara_api.update_party_emails(client_code, policy_number, token)

        self.zahara.login_to_zahara_and_perform_multi_email_change_transaction_process(policy_number, client_code, expect_poly_status)

    @keyword
    def login_to_zinnia_live_and_process_bene_change_term_flow(self, policy_number, client_plan_code):
        BuiltIn().log("Perform Beneficiary Change Term Change Term Process")
        BuiltIn().log_to_console("Perform Beneficiary Change Term Change Term Process")
        BuiltIn().log("-----------------------------------------------------------")
        BuiltIn().log_to_console("-----------------------------------------------------------")

        self.webutils.open_browser_with_url(ZinniaLive.url, ZinniaLive.browser)
        user_id = self.read_config.getValueByKey('zinnia_live_user_email')
        self.webutils.wait_and_input_text(ZinniaLive_web_locators.zl_user_input, user_id)
        self.webutils.wait_and_click(ZinniaLive_web_locators.zl_user_submit_btn)
        self.process_bene_change_term(policy_number, client_plan_code)

        if self.webutils.is_element_visible(ZinniaLive_web_locators.zl_user_pass_input):
            user_pass = self.read_config.getValueByKey('zinnia_live_pass')
            self.webutils.wait_and_input_text(ZinniaLive_web_locators.zl_user_pass_input, user_pass)
            self.webutils.wait_and_click(ZinniaLive_web_locators.zl_user_pass_submit_btn)
            self.process_bene_change_term(policy_number, client_plan_code)


    @keyword
    def login_to_zinnia_live_and_process_fund_transfer_flow(self, policy_number, transfer_amount, client_plan_code):
        BuiltIn().log("Perform Fund Transfer Process")
        BuiltIn().log_to_console("Perform Fund Transfer Process")
        BuiltIn().log("-----------------------------------------------------------")
        BuiltIn().log_to_console("-----------------------------------------------------------")

        self.webutils.open_browser_with_url(ZinniaLive.url, ZinniaLive.browser)
        user_id = self.read_config.getValueByKey('zinnia_live_user_email')
        self.webutils.wait_and_input_text(ZinniaLive_web_locators.zl_user_input, user_id)
        self.webutils.wait_and_click(ZinniaLive_web_locators.zl_user_submit_btn)
        self.process_fund_transfer(policy_number, transfer_amount, client_plan_code)

        if self.webutils.is_element_visible(ZinniaLive_web_locators.zl_user_pass_input):
            user_pass = self.read_config.getValueByKey('zinnia_live_pass')
            self.webutils.wait_and_input_text(ZinniaLive_web_locators.zl_user_pass_input, user_pass)
            self.webutils.wait_and_click(ZinniaLive_web_locators.zl_user_pass_submit_btn)
            self.process_fund_transfer(policy_number, transfer_amount, client_plan_code)


    @keyword
    def process_systematic_withdrawal_flow(self, old_xml_name, expect_poly_status, client, loan_autopay_amt, Payment_freq, acc_name, payment_mode, acc_number, plan_code):
        policy_number, expected_payee_name = self.zahara.create_policy_with_effective_date(old_xml_name, expect_poly_status, client, plan_code)

        self.login_to_zinnia_live_and_perform_systematic_withdrawal_process(policy_number, expected_payee_name, loan_autopay_amt, Payment_freq, acc_name, payment_mode, acc_number, plan_code)

    @keyword
    def process_systematic_premium_setup_flow(self, old_xml_name, expect_poly_status, client, plan_code):
        client_tran_initiate_date = ""
        client_life_cycle_date = "2025-03-25"
        validate_client_effe_date = "03/25/2025"

        policy_number, expected_payee_name = self.zahara.create_policy_for_specific_client(old_xml_name, expect_poly_status, client,
                                                                       plan_code, client_tran_initiate_date, client_life_cycle_date, validate_client_effe_date)

        self.login_to_zinnia_live_and_perform_systematic_premium_setup_process(policy_number)

    @keyword
    def process_rmd_withdrawal_flow(self, old_xml_name, expect_poly_status, client, loan_autopay_amt, Payment_freq, acc_name, payment_mode, acc_number, plan_code):
        policy_number, expected_payee_name = self.zahara.create_policy_with_effective_date(old_xml_name, expect_poly_status, client, plan_code)

        self.login_to_zinnia_live_and_perform_systematic_rmd_process(policy_number, expected_payee_name, loan_autopay_amt, Payment_freq, acc_name, payment_mode, acc_number, plan_code)

    @keyword
    def process_systematic_rmd_manage_autopay_flow(self,policy_number, expected_payee_name, loan_autopay_amt, Payment_freq, systematic_rmd_update_amount, manage_payment_freq,
                               payment_mode):

        self.login_to_zinnia_live_and_perform_systematic_rmd_manage_autopay_process(policy_number, expected_payee_name, loan_autopay_amt, Payment_freq, systematic_rmd_update_amount, manage_payment_freq,
                               payment_mode)

    @keyword
    def process_systematic_withdrawal_manage_autopay_flow(self,policy_number, expected_payee_name, loan_autopay_amt, Payment_freq, systematic_withdrawal_update_amount, manage_payment_freq,
                               payment_mode):

        self.login_to_zinnia_live_and_perform_systematic_withdrawal_manage_autopay_process(policy_number, expected_payee_name, loan_autopay_amt, Payment_freq, systematic_withdrawal_update_amount, manage_payment_freq,
                               payment_mode)

    @keyword
    def process_systematic_premium_manage_autopay_flow(self,policy_number, expected_payee_name, loan_autopay_amt, Payment_freq, systematic_premium_update_amount, manage_payment_freq,
                               payment_mode):

        self.login_to_zinnia_live_and_perform_systematic_premium_manage_autopay_process(policy_number, expected_payee_name, loan_autopay_amt, Payment_freq, systematic_premium_update_amount, manage_payment_freq,
                               payment_mode)


    @keyword
    def process_manage_autpPay_complete_flow(self, policy_number, expected_payee_name, loan_autopay_amt, Payment_freq, loan_manage_autopay_amt,
                                             manage_payment_freq, payment_mode, plan_code):
        self.login_to_zinnia_live_and_process_manage_loan_auto_pay(policy_number, expected_payee_name, loan_autopay_amt, Payment_freq,
                                                                   loan_manage_autopay_amt, manage_payment_freq,
                                                                   payment_mode, plan_code)

    @keyword
    def process_autoPay_cancel_complete_flow(self, policy_number, plan_code):
        self.login_to_zinnia_live_and_process_cancel_loan_auto_pay(policy_number, plan_code)

    @keyword
    def process_systematic_rmd_autoPay_cancel_complete_flow(self, policy_number, plan_code):
        self.login_to_zinnia_live_and_process_systematic_rmd_cancel_loan_auto_pay(policy_number, plan_code)

    @keyword
    def process_systematic_withdrawal_autoPay_cancel_complete_flow(self, policy_number, plan_code):
        self.login_to_zinnia_live_and_process_systematic_withdrawal_cancel_loan_auto_pay(policy_number, plan_code)

    @keyword
    def process_fund_allocation_flow(self, policy_number, expected_fix_fund_allocation_percent, expected_cap_account_allocation_percent, expected_participation_rate_account_allocation_percent, client_plan_code):

        # policy_number, expected_payee_name = self.zahara.create_policy(old_xml_name, expect_poly_status, client, client_plan_code)



        self.login_to_zinnia_live_and_process_fund_allocation_flow(policy_number, expected_fix_fund_allocation_percent, expected_cap_account_allocation_percent, expected_participation_rate_account_allocation_percent, client_plan_code)

    @keyword
    def communication_preference_change_flow(self, policy_number, client_plan_code, preferred_communication_type):

        # policy_number, expected_payee_name = self.zahara.create_policy(old_xml_name, expect_poly_status, client, client_plan_code)

        self.login_to_zinnia_live_and_process_communication_preference_change_flow(policy_number, client_plan_code, preferred_communication_type)

    @keyword
    def multi_phone_change_flow(self, old_xml_name, expect_poly_status, client, client_plan_code):
        self.process_multi_phone_change_flow(old_xml_name, expect_poly_status, client, client_plan_code)

    @keyword
    def multi_email_change_flow(self, old_xml_name, expect_poly_status, client, client_plan_code):
        self.process_multi_email_change_flow(old_xml_name, expect_poly_status, client, client_plan_code)

    @keyword
    def bene_change_term_flow(self, old_xml_name, expect_poly_status, client, client_plan_code):
        policy_number, expected_payee_name = self.zahara.create_policy_with_effective_date(old_xml_name,
                                                                                           expect_poly_status, client,
                                                                                           client_plan_code)

        # self.login_to_zinnia_live_and_process_bene_change_term_flow(policy_number, client_plan_code)

    @keyword
    def process_fund_transfer_flow(self, policy_number, transfer_amount, client_plan_code):

        # policy_number, expected_payee_name = self.zahara.create_policy(old_xml_name, expect_poly_status, client, client_plan_code)


        self.login_to_zinnia_live_and_process_fund_transfer_flow(policy_number, transfer_amount, client_plan_code)

    @keyword
    def systematic_withdrawal_process(self, old_xml_name, expect_poly_status, client, loan_autopay_amt, Payment_freq, acc_name, payment_mode, acc_number, plan_code):
        self.process_systematic_withdrawal_flow(old_xml_name, expect_poly_status, client, loan_autopay_amt, Payment_freq, acc_name, payment_mode, acc_number, plan_code)

    @keyword
    def systematic_premium_setup_process(self, old_xml_name, expect_poly_status, client, plan_code):
        self.process_systematic_premium_setup_flow(old_xml_name, expect_poly_status, client, plan_code)

    @keyword
    def systematic_rmd_process(self, old_xml_name, expect_poly_status, client, loan_autopay_amt, Payment_freq, acc_name, payment_mode, acc_number, plan_code):
        self.process_rmd_withdrawal_flow(old_xml_name, expect_poly_status, client, loan_autopay_amt, Payment_freq, acc_name, payment_mode, acc_number, plan_code)

    @keyword
    def systematic_rmd_manage_autopay_process(self, policy_number, expected_payee_name, loan_autopay_amt, Payment_freq, systematic_rmd_update_amount, manage_payment_freq,
                               payment_mode):
        self.process_systematic_rmd_manage_autopay_flow(policy_number, expected_payee_name, loan_autopay_amt, Payment_freq, systematic_rmd_update_amount, manage_payment_freq,
                               payment_mode)

    @keyword
    def systematic_withdrawal_manage_autopay_process(self, policy_number, expected_payee_name, loan_autopay_amt, Payment_freq, systematic_withdrawal_update_amount, manage_payment_freq,
                               payment_mode):
        self.process_systematic_withdrawal_manage_autopay_flow(policy_number, expected_payee_name, loan_autopay_amt, Payment_freq, systematic_withdrawal_update_amount, manage_payment_freq,
                               payment_mode)

    @keyword
    def systematic_premium_manage_autopay_process(self, policy_number, expected_payee_name, loan_autopay_amt, Payment_freq, systematic_premium_update_amount, manage_payment_freq,
                               payment_mode):
        self.process_systematic_premium_manage_autopay_flow(policy_number, expected_payee_name, loan_autopay_amt, Payment_freq, systematic_premium_update_amount, manage_payment_freq,
                               payment_mode)


    @keyword
    def transaction_onboarding_automation_flow(self, automate_flow, old_xml_name, policy_number, expected_payee_name, expect_poly_status,
                                               start_loan_amount, loan_autopay_amt, Payment_freq, loan_repayment_amount,
                                               payment_mode_select, expected_fund_allocation_type,
                                               expected_account_name, expected_account_number, loan_manage_autopay_amt,
                                               manage_payment_freq, expected_fix_fund_allocation_percent, expected_cap_account_allocation_percent, expected_participation_rate_account_allocation_percent, client, client_plan_code, transfer_amount, systematic_withd_rmd_amount, systematic_premium_update_amount, systematic_withdrawal_update_amount, systematic_rmd_update_amount, preferred_communication_type):

        automation_flow = self.file.normalize_input_value(automate_flow)

        if automation_flow == "New One Time Loan Repayment":
            self.process_one_time_loan_repayment_complete_flow(old_xml_name, expect_poly_status, start_loan_amount,
                                                               loan_repayment_amount, payment_mode_select,
                                                               expected_fund_allocation_type, expected_account_name,
                                                               expected_account_number, client, client_plan_code)
        elif automation_flow == "Systematic Loan Repayment Setup":
            self.process_loan_autoPay_complete_flow(old_xml_name, expect_poly_status, start_loan_amount,
                                                    loan_autopay_amt, Payment_freq, payment_mode_select,
                                                    expected_fund_allocation_type, expected_account_name,
                                                    expected_account_number, client, client_plan_code)
        elif automation_flow == "Systematic Loan Repayment Update":
            self.process_manage_autpPay_complete_flow(policy_number, expected_payee_name, loan_autopay_amt, Payment_freq, loan_manage_autopay_amt,
                                                      manage_payment_freq, payment_mode_select, client_plan_code)
        elif automation_flow == "Systematic Loan Repayment Cancel":
            self.process_autoPay_cancel_complete_flow(policy_number, client_plan_code)

        elif automation_flow == "Fund Allocation":
            self.process_fund_allocation_flow(policy_number, expected_fix_fund_allocation_percent, expected_cap_account_allocation_percent, expected_participation_rate_account_allocation_percent, client_plan_code)

        elif automation_flow == "Systematic Withdrawal Setup":
            self.systematic_withdrawal_process(old_xml_name, expect_poly_status, client, systematic_withd_rmd_amount, Payment_freq, expected_account_name, payment_mode_select, expected_account_number, client_plan_code)

        elif automation_flow == "Systematic Withdrawal Update":
            self.systematic_withdrawal_manage_autopay_process(policy_number, expected_payee_name, loan_autopay_amt, Payment_freq, systematic_withdrawal_update_amount, manage_payment_freq,
                               payment_mode_select)

        elif automation_flow == "Systematic Withdrawal Cancel":
            self.process_systematic_withdrawal_autoPay_cancel_complete_flow(policy_number, client_plan_code)

        elif automation_flow == "Systematic RMD Setup":
            self.systematic_rmd_process(old_xml_name, expect_poly_status, client, systematic_withd_rmd_amount, Payment_freq, expected_account_name, payment_mode_select, expected_account_number, client_plan_code)

        elif automation_flow == "Systematic RMD Update":
            self.systematic_rmd_manage_autopay_process(policy_number, expected_payee_name, loan_autopay_amt, Payment_freq, systematic_rmd_update_amount, manage_payment_freq,
                               payment_mode_select)

        elif automation_flow == "Systematic RMD Cancel":
            self.process_systematic_rmd_autoPay_cancel_complete_flow(policy_number, client_plan_code)

        elif automation_flow == "Fund Transfer":
            self.process_fund_transfer_flow(policy_number, transfer_amount, client_plan_code)

        elif automation_flow == "Communication Preference change":
            self.communication_preference_change_flow(policy_number, client_plan_code, preferred_communication_type)

        elif automation_flow == "Systematic Premium Setup":
            self.systematic_premium_setup_process(old_xml_name, expect_poly_status, client, client_plan_code)

        elif automation_flow == "Systematic Premium Update":
            self.systematic_premium_manage_autopay_process(policy_number, expected_payee_name, loan_autopay_amt, Payment_freq, systematic_premium_update_amount, manage_payment_freq,
                               payment_mode_select)

        elif automation_flow == "Beneficiary Change":
            self.bene_change_term_flow(old_xml_name, expect_poly_status, client, client_plan_code)

        elif automation_flow == "Beneficiary Change Term":
            self.bene_change_term_flow(old_xml_name, expect_poly_status, client, client_plan_code)

        elif automation_flow == "Beneficiary Change ROP":
            self.bene_change_term_flow(old_xml_name, expect_poly_status, client, client_plan_code)

        elif automation_flow == "Beneficiary Change IUL":
            self.bene_change_term_flow(old_xml_name, expect_poly_status, client, client_plan_code)

        elif automation_flow == "Multi Phone Change":
            self.multi_phone_change_flow(old_xml_name, expect_poly_status, client, client_plan_code)

        elif automation_flow == "Multi Email Change":
            self.multi_email_change_flow(old_xml_name, expect_poly_status, client, client_plan_code)


        else:
            raise ValueError(f"Unknown automation flow: {automation_flow}")

    @keyword
    def transaction_onboarding_automation_flow_until_lifecycle_completion(self, automate_flow, old_xml_name, policy_number, expected_payee_name, expect_poly_status,
                                               start_loan_amount, loan_autopay_amt, Payment_freq, loan_repayment_amount,
                                               payment_mode_select, expected_fund_allocation_type,
                                               expected_account_name, expected_account_number, loan_manage_autopay_amt,
                                               manage_payment_freq, expected_fix_fund_allocation_percent, expected_cap_account_allocation_percent, expected_participation_rate_account_allocation_percent, client, client_plan_code, transfer_amount, systematic_withd_rmd_amount, systematic_premium_update_amount, systematic_withdrawal_update_amount, systematic_rmd_update_amount, preferred_communication_type):

        automation_flow = self.file.normalize_input_value(automate_flow)
        BuiltIn().log(f"Executing {automation_flow} until lifecycle completion only")
        BuiltIn().log_to_console(f"Executing {automation_flow} until lifecycle completion only")

        if automation_flow == "New One Time Loan Repayment":
            policy_number, expected_payee_name = self.zahara.create_policy(old_xml_name, expect_poly_status, client, client_plan_code)
            self.login_to_zinnia_live_and_start_a_loan(policy_number, expected_payee_name, start_loan_amount, payment_mode_select,
                                                       expected_fund_allocation_type, expected_account_name,
                                                       expected_account_number, client_plan_code)
            # Stop here - lifecycle processing is complete after loan creation

        elif automation_flow == "Systematic Premium Setup":
            policy_number, expected_payee_name = self.zahara.create_policy_with_effective_date(old_xml_name, expect_poly_status, client, client_plan_code)
            # Stop here - lifecycle processing is complete after policy creation

        elif automation_flow == "Fund Allocation":
            self.login_to_zinnia_live_and_process_fund_allocation_flow_until_lifecycle(policy_number, expected_fix_fund_allocation_percent, expected_cap_account_allocation_percent, expected_participation_rate_account_allocation_percent, client_plan_code)

        else:
            BuiltIn().log(f"Lifecycle-only version not implemented for: {automation_flow}")
            BuiltIn().log_to_console(f"Lifecycle-only version not implemented for: {automation_flow}")
            # Fall back to original method for unsupported flows
            self.transaction_onboarding_automation_flow(automate_flow, old_xml_name, policy_number, expected_payee_name, expect_poly_status,
                                               start_loan_amount, loan_autopay_amt, Payment_freq, loan_repayment_amount,
                                               payment_mode_select, expected_fund_allocation_type,
                                               expected_account_name, expected_account_number, loan_manage_autopay_amt,
                                               manage_payment_freq, expected_fix_fund_allocation_percent, expected_cap_account_allocation_percent, expected_participation_rate_account_allocation_percent, client, client_plan_code, transfer_amount, systematic_withd_rmd_amount, systematic_premium_update_amount, systematic_withdrawal_update_amount, systematic_rmd_update_amount, preferred_communication_type)

    @keyword
    def login_to_zinnia_live_and_process_fund_allocation_flow_until_lifecycle(self, policy_number, expected_fix_fund_allocation_percent, expected_cap_account_allocation_percent, expected_participation_rate_account_allocation_percent, client_plan_code):
        BuiltIn().log("Perform Fund Allocation Process Until Lifecycle Completion")
        BuiltIn().log_to_console("Perform Fund Allocation Process Until Lifecycle Completion")
        BuiltIn().log("-----------------------------------------------------------")
        BuiltIn().log_to_console("-----------------------------------------------------------")

        self.webutils.open_browser_with_url(ZinniaLive.url, ZinniaLive.browser)
        user_id = self.read_config.getValueByKey('zinnia_live_user_email')
        self.webutils.wait_and_input_text(ZinniaLive_web_locators.zl_user_input, user_id)
        self.webutils.wait_and_click(ZinniaLive_web_locators.zl_user_submit_btn)
        
        # Handle password authentication if required
        if self.webutils.is_element_visible(ZinniaLive_web_locators.zl_user_pass_input):
            user_pass = self.read_config.getValueByKey('zinnia_live_pass')
            self.webutils.wait_and_input_text(ZinniaLive_web_locators.zl_user_pass_input, user_pass)
            self.webutils.wait_and_click(ZinniaLive_web_locators.zl_user_pass_submit_btn)
        
        # Process fund allocation until lifecycle completion only
        self.process_fund_allocation_until_lifecycle(policy_number, expected_fix_fund_allocation_percent, expected_cap_account_allocation_percent, expected_participation_rate_account_allocation_percent, client_plan_code)
        
        BuiltIn().log("Fund allocation lifecycle processing completed. Stopping here as requested.")
        BuiltIn().log_to_console("Fund allocation lifecycle processing completed. Stopping here as requested.")

    @keyword
    def process_fund_allocation_until_lifecycle(self, policy_num, expected_fix_fund_allocation_percent, expected_cap_account_allocation_percent, expected_participation_rate_account_allocation_percent, plan_code):
        policy_number = self.file.normalize_input_value(policy_num)
        client_plan_code = self.file.normalize_input_value(plan_code)

        self.webutils.wait_and_click(ZinniaLive_web_locators.zl_policy_search_tab)
        self.webutils.wait_and_input_text(ZinniaLive_web_locators.policy_search_input, policy_number)
        self.webutils.wait_and_click(ZinniaLive_web_locators.policy_search_btn)
        self.webutils.wait_and_click(ZinniaLive_web_locators.search_result_select)

        self.webutils.wait_and_click(ZinniaLive_web_locators.fund_allocation_tab)

        self.validate_fix_fund_allocation_percent(expected_fix_fund_allocation_percent)
        self.validate_cap_account_allocation_percent(expected_cap_account_allocation_percent)
        self.validate_participation_rate_account_allocation_percent(expected_participation_rate_account_allocation_percent)
        self.webutils.wait_and_click(ZinniaLive_web_locators.allocation_submit_btn)

        expected_loan_status = "Go to case"
        self.validate_fund_allocation_submission(expected_loan_status)

        self.webutils.sleep_time(30)
        self.webutils.wait_and_click(ZinniaLive_web_locators.go_to_case_btn)

        self.webutils.sleep_time(5)
        lifecycle_date = self.file.get_cst_date("%Y-%m-%d")
        self.zahara.process_lifecycle_for_fund_allocation_processing(policy_number, lifecycle_date, client_plan_code)

        # *** LIFECYCLE PROCESSING COMPLETED - STOPPING HERE ***
        # The following validation steps are commented out as requested:
        # complete_validate_status = ZinniaLive_web_locators.validate_zinnia_complete_status
        # nigo_validate_status = ZinniaLive_web_locators.validate_zinnia_nigo_status
        # self.webutils.validate_zinniaLive_case_status(complete_validate_status, nigo_validate_status)

        BuiltIn().log("Lifecycle processing completed. Validation steps after lifecycle are commented out.")
        BuiltIn().log_to_console("Lifecycle processing completed. Validation steps after lifecycle are commented out.")
