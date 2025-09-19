import os
import random
from datetime import datetime
import pytz
import string
import uuid

class FileUtils:

    def random_number_create(self, value):
        return random.randint(0, value)

    def generate_unique_digits(self, length):
        return ''.join(random.choices(string.digits, k=length))

    def generate_unique_upper_string(self, length=6):
        return ''.join(random.choices(string.ascii_uppercase, k=length))

    def get_current_date(self, date_pattern):

        return datetime.now().strftime(date_pattern)

    def create_directory(self, path):
        os.makedirs(path, exist_ok=True)

    def normalize_input_value(self, value):
        if isinstance(value, tuple) and len(value) == 2:
            return value[1]
        elif isinstance(value, str):
            return value
        else:
            raise ValueError(f"Unsupported value format: {value}")

    def get_project_directory(self):
        current_dir = os.getcwd()
        # Look for key project markers instead of hardcoded directory name
        project_markers = ['resources', 'tests', 'data']
        while True:
            # Check if all required project directories exist in current directory
            if all(os.path.exists(os.path.join(current_dir, marker)) for marker in project_markers):
                return current_dir
            parent_dir = os.path.dirname(current_dir)
            if current_dir == parent_dir:  # Reached root directory
                # Fallback to current working directory if project markers not found
                return os.getcwd()
            current_dir = parent_dir

    def get_cst_date(self,pattern):

        cst_timezone = pytz.timezone('US/Central')

        utc_time = datetime.now(pytz.utc)

        cst_time = utc_time.astimezone(cst_timezone)

        return cst_time.strftime(pattern)

    def get_current_date_with_timezone_format(self):
        current_time = datetime.now().astimezone()
        return current_time.strftime("%m%d%Y%H%M%S")

    def get_current_date_format_windows(self):
        now = datetime.now()
        return f"{now.month}/{now.day}/{now.year}"

    def get_current_date_format_windows_with_two_digit(self):
        now = datetime.now()
        return f"{now.month:02}/{now.day:02}/{now.year}"

    def remove_leading_zeros_from_date(self, date_str):
        month, day, year = date_str.split('/')
        month = str(int(month))
        day = str(int(day))
        return f"{month}/{day}/{year}"


    def format_second_word(self, text):
        parts = text.split()
        if len(parts) >= 2:
            parts[1] = parts[1].capitalize()
        return ' '.join(parts)

    def convert_date_format(self, actual_date):

        try:
            date_obj = datetime.strptime(actual_date, "%m/%d/%Y")
            expected_date = date_obj.strftime("%Y-%m-%d")
            return expected_date
        except ValueError as e:
            raise ValueError(f"Invalid date format: {actual_date}. Expected format: MM/DD/YYYY") from e

    def date_format_as_remove_zero_from_date_month(self, actual_date):
        month, day, year = actual_date.split('/')
        return f"{int(month)}/{int(day)}/{year}"

    def generate_random_uuid(self):
        return str(uuid.uuid4())





