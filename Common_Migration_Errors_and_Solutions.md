# Common Migration Errors and Solutions for Transaction Onboarding Test Suite

## 1. DATA-RELATED ERRORS

### Error: Excel File Not Found
**Symptoms**: 
```
FileNotFoundError: [Errno 2] No such file or directory: 'data/test_data/transaction_onboarding.xlsx'
```

**Causes**:
- Incorrect file path in new framework
- File not copied to correct location
- Different working directory

**Solutions**:
```python
import os
from pathlib import Path

# Solution 1: Use absolute paths
def get_data_file_path():
    project_root = Path(__file__).parent.parent
    return project_root / "data" / "test_data" / "transaction_onboarding.xlsx"

# Solution 2: Environment-based path
DATA_DIR = os.environ.get('TEST_DATA_DIR', 'data/test_data')
excel_file = os.path.join(DATA_DIR, 'transaction_onboarding.xlsx')

# Solution 3: Validation before use
def validate_data_file(file_path):
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"Required data file not found: {file_path}")
    return file_path
```

### Error: Excel Sheet Reading Issues
**Symptoms**:
```
ValueError: Worksheet named 'output' not found
KeyError: '${execution_flag}'
```

**Solutions**:
```python
import pandas as pd

def safe_excel_reader(file_path, sheet_name='output'):
    try:
        # Check if file exists
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"Excel file not found: {file_path}")
        
        # Load workbook to check sheets
        xl_file = pd.ExcelFile(file_path)
        if sheet_name not in xl_file.sheet_names:
            print(f"Available sheets: {xl_file.sheet_names}")
            raise ValueError(f"Sheet '{sheet_name}' not found")
        
        # Read with error handling
        df = pd.read_excel(file_path, sheet_name=sheet_name)
        
        # Validate required columns
        required_columns = ['${TestId}', '${automation_flow}', '${execution_flag}']
        missing_columns = [col for col in required_columns if col not in df.columns]
        if missing_columns:
            raise ValueError(f"Missing required columns: {missing_columns}")
        
        return df
    except Exception as e:
        print(f"Error reading Excel file: {e}")
        raise
```

## 2. CONFIGURATION ERRORS

### Error: Configuration File Loading Failed
**Symptoms**:
```
configparser.NoSectionError: No section: 'DEFAULT'
KeyError: 'zinnia_live_user_email'
```

**Solutions**:
```python
import configparser
import os

class ConfigManager:
    def __init__(self, config_file='config/config.properties'):
        self.config = configparser.ConfigParser()
        self.config_file = config_file
        self.load_config()
    
    def load_config(self):
        if not os.path.exists(self.config_file):
            raise FileNotFoundError(f"Config file not found: {self.config_file}")
        
        try:
            # Handle Java-style properties files
            with open(self.config_file, 'r') as f:
                content = f.read()
            
            # Add [DEFAULT] section if missing
            if '[DEFAULT]' not in content:
                content = '[DEFAULT]\n' + content
            
            self.config.read_string(content)
        except Exception as e:
            raise Exception(f"Error loading config: {e}")
    
    def get_value(self, key, default=None):
        try:
            return self.config.get('DEFAULT', key)
        except (configparser.NoOptionError, configparser.NoSectionError):
            if default is not None:
                return default
            raise KeyError(f"Configuration key '{key}' not found")
```

### Error: Encrypted Password Handling
**Symptoms**:
```
AttributeError: 'ConfigManager' object has no attribute 'get_encrypt_value_by_key'
```

**Solutions**:
```python
import base64
from cryptography.fernet import Fernet

class SecureConfigManager(ConfigManager):
    def __init__(self, config_file, encryption_key=None):
        super().__init__(config_file)
        self.encryption_key = encryption_key or self._get_default_key()
        self.cipher = Fernet(self.encryption_key)
    
    def _get_default_key(self):
        # Generate or load encryption key
        return Fernet.generate_key()
    
    def get_encrypt_value_by_key(self, key):
        encrypted_value = self.get_value(key)
        try:
            # Decode base64 and decrypt
            encrypted_bytes = base64.b64decode(encrypted_value)
            decrypted_bytes = self.cipher.decrypt(encrypted_bytes)
            return decrypted_bytes.decode('utf-8')
        except Exception:
            # If decryption fails, return as-is (might be plain text)
            return encrypted_value
```

## 3. WEB AUTOMATION ERRORS

### Error: WebDriver Not Found
**Symptoms**:
```
selenium.common.exceptions.WebDriverException: 'chromedriver' executable needs to be in PATH
```

**Solutions**:
```python
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options

class WebDriverManager:
    @staticmethod
    def get_driver(browser='chrome', headless=False):
        if browser.lower() == 'chrome':
            options = Options()
            if headless:
                options.add_argument('--headless')
            options.add_argument('--no-sandbox')
            options.add_argument('--disable-dev-shm-usage')
            
            # Auto-download driver
            service = Service(ChromeDriverManager().install())
            return webdriver.Chrome(service=service, options=options)
        
        elif browser.lower() == 'firefox':
            from webdriver_manager.firefox import GeckoDriverManager
            service = Service(GeckoDriverManager().install())
            return webdriver.Firefox(service=service)
        
        else:
            raise ValueError(f"Unsupported browser: {browser}")
```

### Error: Element Not Found
**Symptoms**:
```
selenium.common.exceptions.NoSuchElementException: Unable to locate element
selenium.common.exceptions.TimeoutException: Message
```

**Solutions**:
```python
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

class RobustWebUtils:
    def __init__(self, driver, default_timeout=30):
        self.driver = driver
        self.wait = WebDriverWait(driver, default_timeout)
    
    def safe_find_element(self, locator, timeout=None):
        try:
            if timeout:
                wait = WebDriverWait(self.driver, timeout)
            else:
                wait = self.wait
            return wait.until(EC.presence_of_element_located(locator))
        except TimeoutException:
            print(f"Element not found within {timeout or 30} seconds: {locator}")
            raise
    
    def wait_and_click_with_retry(self, locator, max_retries=3, timeout=30):
        for attempt in range(max_retries):
            try:
                element = self.wait.until(EC.element_to_be_clickable(locator))
                element.click()
                return True
            except Exception as e:
                print(f"Click attempt {attempt + 1} failed: {e}")
                if attempt == max_retries - 1:
                    raise
                time.sleep(2)
        return False
    
    def smart_wait_for_element(self, locator, expected_condition='visible'):
        conditions = {
            'visible': EC.visibility_of_element_located,
            'clickable': EC.element_to_be_clickable,
            'present': EC.presence_of_element_located
        }
        
        condition = conditions.get(expected_condition, EC.visibility_of_element_located)
        return self.wait.until(condition(locator))
```

### Error: Locator Format Issues
**Symptoms**:
```
selenium.common.exceptions.InvalidSelectorException: invalid selector
```

**Solutions**:
```python
from selenium.webdriver.common.by import By

class LocatorConverter:
    @staticmethod
    def convert_robot_locator(robot_locator):
        """Convert Robot Framework locator strings to Selenium locators"""
        if robot_locator.startswith('//') or robot_locator.startswith('./'):
            return (By.XPATH, robot_locator)
        elif robot_locator.startswith('css='):
            return (By.CSS_SELECTOR, robot_locator[4:])
        elif robot_locator.startswith('id='):
            return (By.ID, robot_locator[3:])
        elif robot_locator.startswith('name='):
            return (By.NAME, robot_locator[5:])
        else:
            # Default to XPath
            return (By.XPATH, robot_locator)
    
    @staticmethod
    def format_locator(locator_template, **kwargs):
        """Handle dynamic locators with parameters"""
        try:
            formatted_locator = locator_template.format(**kwargs)
            return formatted_locator
        except KeyError as e:
            raise ValueError(f"Missing parameter for locator: {e}")

# Example usage
class ZinniaLiveLocators:
    USER_INPUT = (By.XPATH, "//input[@type='email']")
    VALIDATE_LOAN_AMT = (By.XPATH, "//span[contains(text(),'{}')]")  # Template locator
    
    @classmethod
    def get_loan_amount_locator(cls, amount):
        xpath = cls.VALIDATE_LOAN_AMT[1].format(amount)
        return (By.XPATH, xpath)
```

## 4. API INTEGRATION ERRORS

### Error: Authentication Failed
**Symptoms**:
```
requests.exceptions.HTTPError: 401 Client Error: Unauthorized
```

**Solutions**:
```python
import requests
import time
from functools import wraps

class ApiClient:
    def __init__(self, base_url, client_id, client_secret):
        self.base_url = base_url
        self.client_id = client_id
        self.client_secret = client_secret
        self.token = None
        self.token_expiry = None
        self.session = requests.Session()
    
    def authenticate(self):
        auth_url = f"{self.base_url}/oauth/token"
        payload = {
            'grant_type': 'client_credentials',
            'client_id': self.client_id,
            'client_secret': self.client_secret
        }
        
        response = self.session.post(auth_url, data=payload)
        response.raise_for_status()
        
        token_data = response.json()
        self.token = token_data['access_token']
        # Set expiry (assuming expires_in is in seconds)
        self.token_expiry = time.time() + token_data.get('expires_in', 3600)
    
    def ensure_authenticated(func):
        @wraps(func)
        def wrapper(self, *args, **kwargs):
            if not self.token or time.time() >= self.token_expiry:
                self.authenticate()
            return func(self, *args, **kwargs)
        return wrapper
    
    @ensure_authenticated
    def make_request(self, method, endpoint, **kwargs):
        url = f"{self.base_url}/{endpoint.lstrip('/')}"
        headers = kwargs.get('headers', {})
        headers['Authorization'] = f'Bearer {self.token}'
        kwargs['headers'] = headers
        
        response = self.session.request(method, url, **kwargs)
        response.raise_for_status()
        return response.json()
```

### Error: API Response Parsing
**Symptoms**:
```
KeyError: 'data'
TypeError: 'NoneType' object is not subscriptable
```

**Solutions**:
```python
class SafeApiResponseParser:
    @staticmethod
    def safe_get(data, *keys, default=None):
        """Safely navigate nested dictionary/list structures"""
        current = data
        for key in keys:
            if isinstance(current, dict) and key in current:
                current = current[key]
            elif isinstance(current, list) and isinstance(key, int) and len(current) > key:
                current = current[key]
            else:
                return default
        return current
    
    @staticmethod
    def get_case_id(response):
        """Extract case ID with multiple fallback strategies"""
        # Strategy 1: Direct access
        case_id = SafeApiResponseParser.safe_get(response, 'id')
        if case_id:
            return case_id
        
        # Strategy 2: Nested in data
        case_id = SafeApiResponseParser.safe_get(response, 'data', 'id')
        if case_id:
            return case_id
        
        # Strategy 3: First item in results array
        case_id = SafeApiResponseParser.safe_get(response, 'results', 0, 'id')
        if case_id:
            return case_id
        
        raise ValueError("Case ID not found in response")
```

## 5. DATABASE CONNECTION ERRORS

### Error: Database Connection Failed
**Symptoms**:
```
pyodbc.Error: ('08001', '[08001] [Microsoft][ODBC Driver 17 for SQL Server]...')
```

**Solutions**:
```python
import pyodbc
import time
from contextlib import contextmanager

class DatabaseManager:
    def __init__(self, connection_string, max_retries=3):
        self.connection_string = connection_string
        self.max_retries = max_retries
    
    def get_connection(self):
        for attempt in range(self.max_retries):
            try:
                connection = pyodbc.connect(self.connection_string)
                return connection
            except Exception as e:
                print(f"Database connection attempt {attempt + 1} failed: {e}")
                if attempt == self.max_retries - 1:
                    raise
                time.sleep(2 ** attempt)  # Exponential backoff
    
    @contextmanager
    def get_cursor(self):
        connection = None
        cursor = None
        try:
            connection = self.get_connection()
            cursor = connection.cursor()
            yield cursor
            connection.commit()
        except Exception as e:
            if connection:
                connection.rollback()
            raise
        finally:
            if cursor:
                cursor.close()
            if connection:
                connection.close()
    
    def execute_query(self, query, params=None):
        with self.get_cursor() as cursor:
            if params:
                cursor.execute(query, params)
            else:
                cursor.execute(query)
            
            if cursor.description:  # SELECT query
                columns = [desc[0] for desc in cursor.description]
                rows = cursor.fetchall()
                return [dict(zip(columns, row)) for row in rows]
            else:  # INSERT/UPDATE/DELETE
                return cursor.rowcount
```

## 6. THREADING AND TIMING ERRORS

### Error: Race Conditions
**Symptoms**:
```
AssertionError: Expected status 'COMPLETED', but got 'IN_PROGRESS'
```

**Solutions**:
```python
import time
from typing import Callable, Any

class WaitUtils:
    @staticmethod
    def wait_for_condition(condition_func: Callable[[], bool], 
                          timeout: int = 60, 
                          interval: int = 2,
                          error_message: str = "Condition not met within timeout"):
        """Wait for a condition to become true"""
        start_time = time.time()
        while time.time() - start_time < timeout:
            if condition_func():
                return True
            time.sleep(interval)
        raise TimeoutError(error_message)
    
    @staticmethod
    def wait_for_value(value_func: Callable[[], Any], 
                      expected_value: Any,
                      timeout: int = 60,
                      interval: int = 2):
        """Wait for a function to return expected value"""
        def condition():
            try:
                return value_func() == expected_value
            except Exception:
                return False
        
        WaitUtils.wait_for_condition(
            condition, 
            timeout, 
            interval, 
            f"Value did not become '{expected_value}' within {timeout} seconds"
        )
    
    @staticmethod
    def retry_operation(operation: Callable, max_retries: int = 3, delay: int = 1):
        """Retry an operation with exponential backoff"""
        for attempt in range(max_retries):
            try:
                return operation()
            except Exception as e:
                if attempt == max_retries - 1:
                    raise
                wait_time = delay * (2 ** attempt)
                print(f"Operation failed (attempt {attempt + 1}), retrying in {wait_time}s: {e}")
                time.sleep(wait_time)
```

## 7. DATA TYPE AND FORMATTING ERRORS

### Error: Data Type Mismatches
**Symptoms**:
```
TypeError: unsupported operand type(s) for +: 'NoneType' and 'str'
ValueError: invalid literal for int() with base 10: 'N/A'
```

**Solutions**:
```python
class DataFormatter:
    @staticmethod
    def safe_string(value, default=''):
        """Convert any value to string safely"""
        if value is None or (isinstance(value, str) and value.strip().upper() in ['', 'N/A', 'NULL']):
            return default
        return str(value).strip()
    
    @staticmethod
    def safe_int(value, default=0):
        """Convert value to int safely"""
        if value is None:
            return default
        try:
            # Handle string representations
            if isinstance(value, str):
                value = value.strip().replace(',', '')
                if value.upper() in ['', 'N/A', 'NULL']:
                    return default
            return int(float(value))  # Handle decimal strings
        except (ValueError, TypeError):
            return default
    
    @staticmethod
    def safe_float(value, default=0.0):
        """Convert value to float safely"""
        if value is None:
            return default
        try:
            if isinstance(value, str):
                value = value.strip().replace(',', '').replace('$', '')
                if value.upper() in ['', 'N/A', 'NULL']:
                    return default
            return float(value)
        except (ValueError, TypeError):
            return default
    
    @staticmethod
    def normalize_input_value(value):
        """Normalize input values (equivalent to Robot Framework keyword)"""
        if value is None:
            return None
        
        str_value = str(value).strip()
        if str_value.upper() in ['', 'NONE', 'NULL', 'N/A']:
            return None
        
        return str_value
```

## 8. ENVIRONMENT-SPECIFIC ERRORS

### Error: Path Separator Issues (Windows vs Linux)
**Symptoms**:
```
FileNotFoundError: [Errno 2] No such file or directory: 'resources\\config\\config.properties'
```

**Solutions**:
```python
import os
from pathlib import Path

class PathUtils:
    @staticmethod
    def get_resource_path(*path_parts):
        """Get platform-independent resource path"""
        base_path = Path(__file__).parent.parent  # Adjust as needed
        return base_path.joinpath(*path_parts)
    
    @staticmethod
    def ensure_directory(directory_path):
        """Create directory if it doesn't exist"""
        Path(directory_path).mkdir(parents=True, exist_ok=True)
    
    @staticmethod
    def convert_robot_path(robot_path):
        """Convert Robot Framework path to current OS format"""
        # Replace backslashes with forward slashes, then use Path
        normalized = robot_path.replace('\\', '/')
        return Path(normalized)

# Example usage
config_path = PathUtils.get_resource_path('resources', 'config', 'config.properties')
```

## 9. MEMORY AND PERFORMANCE ERRORS

### Error: Memory Issues with Large Excel Files
**Symptoms**:
```
MemoryError: Unable to allocate array
pandas.errors.OutOfMemoryError
```

**Solutions**:
```python
import pandas as pd
from typing import Iterator, Dict, Any

class EfficientExcelReader:
    def __init__(self, file_path: str):
        self.file_path = file_path
    
    def read_in_chunks(self, sheet_name: str = 'output', chunk_size: int = 1000) -> Iterator[pd.DataFrame]:
        """Read Excel file in chunks to manage memory"""
        try:
            # Read total rows first
            df_info = pd.read_excel(self.file_path, sheet_name=sheet_name, nrows=0)
            total_rows = len(pd.read_excel(self.file_path, sheet_name=sheet_name))
            
            for start_row in range(0, total_rows, chunk_size):
                chunk = pd.read_excel(
                    self.file_path, 
                    sheet_name=sheet_name,
                    skiprows=start_row,
                    nrows=chunk_size
                )
                yield chunk
        except Exception as e:
            print(f"Error reading Excel in chunks: {e}")
            raise
    
    def get_filtered_data(self, execution_flag_column: str = '${execution_flag}') -> Iterator[Dict[str, Any]]:
        """Get filtered data row by row"""
        for chunk in self.read_in_chunks():
            if execution_flag_column in chunk.columns:
                filtered_chunk = chunk[chunk[execution_flag_column] == 'YES']
                for _, row in filtered_chunk.iterrows():
                    yield row.to_dict()
```

## 10. DEBUGGING AND TROUBLESHOOTING TIPS

### Enhanced Logging Setup
```python
import logging
import sys
from datetime import datetime

def setup_comprehensive_logging():
    # Create logger
    logger = logging.getLogger('test_migration')
    logger.setLevel(logging.DEBUG)
    
    # Create formatters
    detailed_formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(filename)s:%(lineno)d - %(message)s'
    )
    simple_formatter = logging.Formatter('%(levelname)s: %(message)s')
    
    # File handler
    file_handler = logging.FileHandler(f'migration_debug_{datetime.now().strftime("%Y%m%d_%H%M%S")}.log')
    file_handler.setLevel(logging.DEBUG)
    file_handler.setFormatter(detailed_formatter)
    
    # Console handler
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(logging.INFO)
    console_handler.setFormatter(simple_formatter)
    
    # Add handlers
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)
    
    return logger

# Usage
logger = setup_comprehensive_logging()
logger.info("Starting test migration process")
```

### Debug Helper Functions
```python
class DebugUtils:
    @staticmethod
    def log_object_structure(obj, name="Object", max_depth=3, current_depth=0):
        """Log the structure of any object for debugging"""
        indent = "  " * current_depth
        logger.info(f"{indent}{name}: {type(obj).__name__}")
        
        if current_depth >= max_depth:
            return
        
        if isinstance(obj, dict):
            for key, value in obj.items():
                DebugUtils.log_object_structure(value, f"{name}.{key}", max_depth, current_depth + 1)
        elif isinstance(obj, (list, tuple)):
            for i, item in enumerate(obj[:3]):  # Only show first 3 items
                DebugUtils.log_object_structure(item, f"{name}[{i}]", max_depth, current_depth + 1)
    
    @staticmethod
    def save_response_to_file(response, filename):
        """Save API response to file for analysis"""
        import json
        with open(f"debug_{filename}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json", 'w') as f:
            json.dump(response, f, indent=2, default=str)
    
    @staticmethod
    def compare_expected_actual(expected, actual, context=""):
        """Detailed comparison for debugging failures"""
        logger.info(f"Comparison for {context}:")
        logger.info(f"Expected ({type(expected).__name__}): {expected}")
        logger.info(f"Actual ({type(actual).__name__}): {actual}")
        logger.info(f"Equal: {expected == actual}")
        
        if isinstance(expected, (dict, list)) and isinstance(actual, (dict, list)):
            import json
            logger.info("Expected JSON:")
            logger.info(json.dumps(expected, indent=2, default=str))
            logger.info("Actual JSON:")
            logger.info(json.dumps(actual, indent=2, default=str))
```

These comprehensive error solutions and debugging approaches should help you successfully migrate your Robot Framework test suite while avoiding the most common pitfalls.
