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
    base_report_path = os.path.join(read_config.getValueByKey('zinnia_live_report_path'), test_id)

    file.create_directory(base_report_path)

    contract_creation = os.path.join(project_dir,
                                     'testsuite/zinnia_live_test_suite/api/Step_1_Generate_DTCC_and_Upload.robot')
    zl_case_validation = os.path.join(project_dir,
                                      'testsuite/zinnia_live_test_suite/api/Step_2_Perform_Zinnia_Live_Case_Validation.robot')

    args = [
        '--outputdir', base_report_path,
        '--name', 'Zinnia Live Case Validation',
        # contract_creation,
        zl_case_validation,
    ]
    run_cli(args)

