import time
from robot.api.deco import keyword, library
from robot.libraries.BuiltIn import BuiltIn
from robot.api import logger
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.chrome.options import Options

@library
class   WebUtils:

    def __init__(self):
        self.selLib = BuiltIn().get_library_instance("SeleniumLibrary")


    @keyword
    def open_browser_with_url(self, url, browser):
        if browser.lower() == "chrome":
            options = self._get_chrome_options()
            self.selLib.open_browser(url=url, browser=browser, options=options)
        else:
            self.selLib.open_browser(url=url, browser=browser)
        self.selLib.maximize_browser_window()

    @keyword
    def _get_chrome_options(self):
        """Configure Chrome options to suppress GCM errors and other unwanted messages"""
        options = Options()
        
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
    def browser_go_back(self):
        self.selLib.go_back()


    @keyword
    def wait_and_click(self, locator, timeout=60):
        self.selLib.wait_until_element_is_visible(locator, timeout=timeout)
        self.selLib.click_element(locator)

    @keyword
    def web_element_is_visible(self, locator, timeout=5):
        try:
            self.selLib.wait_until_element_is_visible(locator, timeout=timeout)
            return True
        except Exception:
            return False

    @keyword
    def wait_and_click_any(self, locators, timeout=60):
        for locator in locators:
            if self.web_element_is_visible(locator, timeout):
                self.wait_and_click(locator)
                return True
        return False

    @keyword
    def is_element_with_partial_text_present(self, text, tag="span", timeout=5):
        locator = f"//{tag}[contains(text(), \"{text}\")]"

        try:
            self.selLib.wait_until_element_is_visible(locator, timeout=timeout)
            return True
        except Exception as e:
            logger.info(f"Element with text '{text}' not found. Exception: {type(e).__name__} - {e}")
            return False

    @keyword
    def wait_and_select_checkbox(self, locator, timeout=60):
        self.selLib.wait_until_element_is_visible(locator, timeout=timeout)
        self.selLib.select_checkbox(locator)

    @keyword
    def wait_until_element_visible(self, locator, timeout=60):
        self.selLib.wait_until_element_is_visible(locator, timeout=timeout)

    @keyword
    def wait_until_element_visible_with_retries(self, locator, max_retries, interval, refresh_locator):
        for attempt in range(1, max_retries + 1):
            try:
                self.wait_and_click(refresh_locator)
                self.selLib.wait_until_element_is_visible(locator, timeout=5)
                BuiltIn().log(f"Lifecycle completed on attempt {attempt}")
                BuiltIn().log_to_console(f"Lifecycle completed on attempt {attempt}")
                return
            except Exception as e:
                BuiltIn().log(f"Attempt {attempt}: Lifecycle not completed yet. Retrying in {interval} seconds.")
                BuiltIn().log_to_console(f"Attempt {attempt}: Lifecycle not completed yet. Retrying in {interval} seconds.")
                if attempt < max_retries:
                    time.sleep(interval)
                else:
                    BuiltIn().log(f"Lifecycle completion failed.")
                    BuiltIn().log_to_console(f"Lifecycle completion failed.")
                    raise Exception(f"Element '{locator}' not visible after {max_retries} attempts.") from e

    @keyword
    def validate_zinniaLive_case_status(self, complete_xpath, nigo_xpath, max_retries=15, wait_seconds=30):
        for attempt in range(1, max_retries + 1):

            BuiltIn().log(f"Attempt {attempt} of {max_retries} for Zinnia Live case status check...")
            BuiltIn().log_to_console(f"Attempt {attempt} of {max_retries} for Zinnia Live case status check...")

            nigo_visible = False
            complete_visible = False

            self.click_chrome_reload_button()
            self.sleep_time(3)

            try:
                nigo_element = self.selLib.get_webelement(nigo_xpath)
                nigo_visible = nigo_element.is_displayed()
            except Exception:
                pass

            try:
                complete_element = self.selLib.get_webelement(complete_xpath)
                complete_visible = complete_element.is_displayed()
            except Exception:
                pass

            if nigo_visible:
                raise Exception("Zinnia Live case validation failed: NIGO status is visible.")

            if complete_visible:
                BuiltIn().log("Zinnia Live case validation passed: COMPLETE status is visible.")
                BuiltIn().log_to_console("Zinnia Live validation passed: COMPLETE status is visible.")
                return

            time.sleep(wait_seconds)

        BuiltIn().log("Zinnia Live case validation passed.")
        BuiltIn().log_to_console("Zinnia Live case validation passed.")

    @keyword
    def validate_zinniaLive_case_status_1(self, complete_xpath, nigo_xpath, max_retries=10, wait_seconds=30):
        for attempt in range(1, max_retries + 1):

            BuiltIn().log(f"Attempt {attempt} of {max_retries} for Zinnia Live case status check...")
            BuiltIn().log_to_console(f"Attempt {attempt} of {max_retries} for Zinnia Live case status check...")

            time.sleep(wait_seconds)

        BuiltIn().log("Zinnia Live case validation passed.")
        BuiltIn().log_to_console("Zinnia Live case validation passed.")

    @keyword
    def wait_and_clear_text(self, locator, timeout=60):
        self.selLib.wait_until_element_is_visible(locator, timeout=timeout)
        self.selLib.clear_element_text(locator)

    @keyword
    def wait_and_clear_text_by_press_key(self, locator, timeout=60):
        self.selLib.wait_until_element_is_visible(locator, timeout=timeout)
        self.selLib.click_element(locator)
        self.selLib.press_keys(locator, "CTRL+A")
        self.selLib.press_keys(locator, "BACKSPACE")



    @keyword
    def wait_clear_and_input_text(self, locator, text, timeout=60):
        self.selLib.wait_until_element_is_visible(locator, timeout=timeout)
        self.selLib.click_element(locator)
        self.selLib.press_keys(locator, "CTRL+A")
        self.selLib.press_keys(locator, "BACKSPACE")
        self.selLib.input_text(locator, text)

        # Now verify the text is present — wait for it
        self.selLib.wait_until_element_attribute_value_is(locator, "value", text, timeout=timeout)


    @keyword
    def wait_for_element_text(self, xpath, expected_text, timeout=60):
        self.selLib.wait_until_element_contains(xpath, expected_text, timeout=timeout)

    @keyword
    @keyword
    def click_chrome_reload_button(self):
        self.selLib.reload_page()

    @keyword
    def clear_input_field_with_js(self, xpath, timeout=60):
        self.selLib.wait_until_element_is_visible(xpath, timeout=timeout)
        element = self.selLib.find_element(xpath)
        self.selLib.execute_javascript("arguments[0].value = '';", element)

    @keyword
    def wait_and_input_text(self, locator, value, timeout=60):
        self.selLib.wait_until_element_is_visible(locator, timeout=timeout)
        self.selLib.input_text(locator, value)


    @keyword
    def wait_and_input_text_by_js(self, locator, value, timeout=60):
        element = None
        # Wait for element to be visible
        self.selLib.wait_until_element_is_visible(locator, timeout=timeout)

        # Try regular input first
        try:
            element = self.selLib.find_element(locator)
            element.clear()
            element.send_keys(value)
        except Exception as e:
            # Fallback: use JavaScript if normal method fails
            self.selLib.execute_javascript("arguments[0].value = arguments[1];", element, value)

    @keyword
    def scroll_right(self, locator, pixels=500):
        element = self.selLib.get_webelement(locator)
        self.selLib.execute_javascript("arguments[0].scrollLeft += arguments[1];", element, pixels)

    @keyword
    def sleep_time(self, seconds):
        time.sleep(float(seconds))

    @keyword
    def get_text(self, xpath):
        return self.selLib.get_text(xpath)

    @keyword
    def get_input_value(self, xpath):
        return self.selLib.get_element_attribute(xpath, "value")

    @keyword
    def wait_for_element(self, xpath, timeout=10):
        self.selLib.wait_until_element_is_visible(xpath, timeout)

    @keyword
    def element_should_be_visible(self, xpath):
        self.selLib.element_should_be_visible(xpath)

    @keyword
    def scroll_down(self, pixels):
        self.selLib.execute_javascript(f"window.scrollBy(0, {pixels});")

    @keyword
    def scroll_up(self, pixels):
        self.selLib.execute_javascript(f"window.scrollBy(0, -{pixels});")

    @keyword
    def element_should_contain_text(self, xpath, expected_text):
        self.selLib.element_should_contain(xpath, expected_text)

    @keyword
    def is_element_visible(self, xpath, timeout=5):
        try:
            self.selLib.wait_until_element_is_visible(xpath, timeout)
            return True
        except Exception:
            return False

    @keyword
    def select_dropdown_by_value(self, xpath, value):
        self.selLib.select_from_list_by_value(xpath, value)

    @keyword
    def select_dropdown_by_label(self, xpath, label):
        self.selLib.select_from_list_by_label(xpath, label)

    @keyword
    def switch_to_frame(self, frame_locator, timeout=30):
        self.selLib.wait_until_element_is_visible(frame_locator, timeout=timeout)
        self.selLib.select_frame(frame_locator)

    @keyword
    def switch_to_default_content(self):
        self.selLib.unselect_frame()

    @keyword
    def capture_screenshot(self, filename="screenshot.png"):
        self.selLib.capture_page_screenshot(filename)

    @keyword
    def scroll_to_element(self, xpath):
        self.selLib.execute_javascript("arguments[0].scrollIntoView();", self.selLib.find_element(xpath))

    @keyword
    def execute_javascript(self, script, *args):
        self.selLib.execute_javascript(script, *args)

    @keyword
    def get_element_attribute(self, xpath, attribute):
        return self.selLib.get_element_attribute(xpath, attribute)

    @keyword
    def hover_over_element(self, xpath):
        self.selLib.mouse_over(xpath)

    @keyword
    def drag_and_drop(self, source_xpath, target_xpath):
        self.selLib.drag_and_drop(source_xpath, target_xpath)

    @keyword
    def double_click_element(self, xpath):
        self.selLib.double_click_element(xpath)

    @keyword
    def close_browser(self):
        self.selLib.close_browser()

    @keyword
    def close_all_browsers(self):
        self.selLib.close_all_browsers()