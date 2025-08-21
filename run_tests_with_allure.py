import os
import subprocess
import sys

def run_tests_with_allure():
    # Create results directory if it doesn't exist
    os.makedirs('reports/allure-results', exist_ok=True)
    
    # Run tests with Allure
    pytest_cmd = [
        'pytest',
        'tests/',
        '--alluredir=reports/allure-results',
        '-v'
    ]
    
    # Run the tests
    test_result = subprocess.run(pytest_cmd)
    
    # Generate the report
    generate_cmd = [
        'allure',
        'generate',
        'reports/allure-results',
        '--clean',
        '-o',
        'allure-report'
    ]
    subprocess.run(generate_cmd)
    
    # Open the report
    open_cmd = ['allure', 'open', 'allure-report']
    subprocess.run(open_cmd)
    
    return test_result.returncode

if __name__ == '__main__':
    sys.exit(run_tests_with_allure()) 