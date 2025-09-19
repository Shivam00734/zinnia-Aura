from robot.api.deco import keyword, library
from robot.libraries.BuiltIn import BuiltIn
from resources.locators import ETPLocators
import time
from resources.vo.FilePropertiesVo import FilePropertiesVo
from selenium.webdriver.chrome.options import Options


@library
class EappValidation:
    fileProperties = FilePropertiesVo()

    def __init__(self):
        self.selLib = BuiltIn().get_library_instance("SeleniumLibrary")

    @keyword
    def open_browser_with_ETP_Dashboard_url(self, url, browser):
        if browser.lower() == "chrome" or browser.lower() == "headlesschrome":
            options = self._get_chrome_options(browser.lower() == "headlesschrome")
            self.selLib.open_browser(url=url, browser=browser, options=options)
        else:
            self.selLib.open_browser(url=url, browser=browser)
        self.selLib.maximize_browser_window()

    def _get_chrome_options(self, headless=False):
        """Configure Chrome options to suppress GCM errors and other unwanted messages"""
        options = Options()
        
        if headless:
            options.add_argument("--headless")
        
        # Suppress GCM (Google Cloud Messaging) errors
        options.add_argument("--disable-background-networking")
        options.add_argument("--disable-background-timer-throttling")
        options.add_argument("--disable-backgrounding-occluded-windows")
        options.add_argument("--disable-features=TranslateUI")
        options.add_argument("--disable-ipc-flooding-protection")
        options.add_argument("--no-default-browser-check")
        options.add_argument("--no-first-run")
        options.add_argument("--disable-default-apps")
        
        # Disable various background services and sync
        options.add_argument("--disable-sync")
        options.add_argument("--disable-background-mode")
        options.add_argument("--disable-component-update")
        
        # Disable logging and reporting
        options.add_argument("--disable-logging")
        options.add_argument("--log-level=3")  # Only fatal errors
        options.add_argument("--silent")
        
        # Additional stability options
        options.add_argument("--disable-dev-shm-usage")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-gpu-sandbox")
        options.add_argument("--disable-software-rasterizer")
        
        # Suppress info bars and notifications
        options.add_argument("--disable-infobars")
        options.add_argument("--disable-notifications")
        
        # Experimental options to suppress more Chrome internal errors
        options.add_experimental_option("excludeSwitches", ["enable-automation", "enable-logging"])
        options.add_experimental_option('useAutomationExtension', False)
        
        return options

    @keyword
    def enter_the_contract_create_date(self, contract_created_date):
        self.selLib.click_element(ETPLocators.from_date_locator)
        dtcc_file_created_date = contract_created_date
        if dtcc_file_created_date is None:
            raise AssertionError("DTCC File Created Date Not Found")
        self.selLib.input_text(ETPLocators.from_date_locator, dtcc_file_created_date)
        self.selLib.double_click_element(ETPLocators.from_date_locator)
        time.sleep(2)
        self.selLib.double_click_element(ETPLocators.to_date_locator)
        self.selLib.input_text(ETPLocators.to_date_locator, dtcc_file_created_date)
        self.selLib.double_click_element(ETPLocators.to_date_locator)

    @keyword
    def select_no_of_records_from_dropdown(self):
        self.selLib.select_from_list_by_label(ETPLocators.no_of_records_locator, '500')

    @keyword
    def click_on_refresh_button(self):
        self.selLib.click_element(ETPLocators.refreshButton)

    @keyword
    def choose_company_name(self, company_name):
        self.selLib.select_from_list_by_label(ETPLocators.select_companies_locator, company_name)
        time.sleep(2)

    @keyword
    def get_row_number_for_give_application_control_number(self, app_control_number):
        if app_control_number is None:
            raise AssertionError("Application Control number is not found ")
        trans_ref_guids = self.selLib.get_webelements(ETPLocators.trans_refGUID_column_locator)
        trans_ref_guids_list = []
        for trans_ref_guid in trans_ref_guids:
            trans_ref_guids_list.append(trans_ref_guid.text)

        for ele in trans_ref_guids_list:
            if ele != app_control_number:
                pass
            else:
                row_match_index = trans_ref_guids_list.index(ele) + 1
                if row_match_index is None:
                    raise AssertionError("Trans Ref GUID not found in the WebTable")
                return row_match_index

    @keyword
    def get_actual_ETP_info(self, app_control_number, test_id):
        row_count = self.get_row_number_for_give_application_control_number(app_control_number)
        print(f"row_count : {row_count}")
        status_code_xpath = ETPLocators.table_body_xpath_locator + f"/tr[{row_count}]/td[9]"
        print(f"status : {status_code_xpath}")
        contract_number_xpath = ETPLocators.table_body_xpath_locator + f"/tr[{row_count}]/td[1]"
        print(f"contract : {contract_number_xpath}")

        status_code = self.selLib.get_text(status_code_xpath)
        contract_number = self.selLib.get_text(contract_number_xpath)

        return {
            "status_code": status_code,
            "contract_number": contract_number,
        }
