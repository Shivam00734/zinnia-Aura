import os
from robot import run_cli
from resources.utilities.FileUtils import FileUtils
from resources.utilities.ReadConfig import ReadConfig

read_config = ReadConfig()
file = FileUtils()

if __name__ == '__main__':
    project_dir = file.get_project_directory()
    current_date_time = file.get_current_date_with_timezone_format()
    test_id = f"{file.get_current_date('%d%m%Y')}/TC_{current_date_time}"
    base_report_path = os.path.join(read_config.getValueByKey('transaction_onboarding_report_path'), test_id)

    file.create_directory(base_report_path)

    transaction_onboarding_validation = os.path.join(project_dir,
                                      'testsuite/transaction_onboarding_test_suite/ui/transaction_onboarding_regression_suite.robot')

    args = [
        '--outputdir', base_report_path,
        '--name', 'Transaction Onboarding Regression Suite',

        transaction_onboarding_validation,
    ]
    run_cli(args)

