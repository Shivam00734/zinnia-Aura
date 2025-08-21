# Automation Framework

This is a test automation framework built with Python. The framework is designed to run automated tests and generate detailed reports.

## Setup

1. Create a virtual environment:
```bash
python -m venv .venv
source .venv/bin/activate  # On Windows use: .venv\Scripts\activate
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

## Running Tests

To run the tests, use:
```bash
python run_tests.py
```

## Project Structure

- `tests/` - Test cases
- `keywords/` - Custom keywords and test steps
- `utils/` - Utility functions and helpers
- `configs/` - Configuration files
- `resources/` - Test resources and data files

## Reports

Test reports are generated in multiple formats:
- HTML reports
- Allure reports
- XML reports
