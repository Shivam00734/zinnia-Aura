import os
import shutil
import time
from datetime import datetime, timedelta
import random
import pandas as pd
from robot.api.deco import library, keyword
from robot.libraries.BuiltIn import BuiltIn
from resources.utilities.ExcelUtilities import ExcelUtilities
from resources.utilities.FileUtils import FileUtils
from resources.utilities.ReadConfig import ReadConfig
from resources.vo.FilePropertiesVo import FilePropertiesVo


@library
class GenerateDTCC:
    fileProperties = FilePropertiesVo()
    file = FileUtils()
    global_all_dtcc_in_one = []
    all_dtcc_file_content = []
    excel_input_sheet_name = 'Input_data'
    excel_output_sheet_name = 'output_data'

    def __init__(self):
        self.excelSheet = ExcelUtilities()  # Dynamic instantiation
        self.selLib = BuiltIn().get_library_instance("SeleniumLibrary")

    @keyword
    def extract_values_from_old_dtcc_file(self, test_case_id):

        excel_file_path = self.excelSheet.getExcelSheetPath()
        old_file_name = self.excelSheet.get_value_from_excel_by_column_name(excel_file_path,
                                                                            self.excel_input_sheet_name, test_case_id,
                                                                            "old_dtcc_file_name")
        self.fileProperties.oldDtccFileName = old_file_name
        read_config = ReadConfig()
        file_path = read_config.getValueByKey('OldDTCCFilePathNetworkDrive') + old_file_name
        try:
            with open(file_path, 'r') as file:
                file_content = file.read()

                app_control_number = file_content[
                                     file_content.find("B3301") + 5:file_content.find("B3301") + 25].strip()
                self.fileProperties.app_control_no_value = app_control_number

                dis_trans_id_number = file_content[
                                      file_content.find("B3304") + 82:file_content.find("B3304") + 112].strip()
                self.fileProperties.dis_trans_id_no_value = dis_trans_id_number

                doc_control_number = file_content[
                                     file_content.find("B3344") + 25:file_content.find("B3344") + 45].strip()
                self.fileProperties.doc_control_no_value = doc_control_number

                transmission_date = file_content[
                                    file_content.find("B30") + 33:file_content.find("B30") + 41].strip()
                self.fileProperties.transmission_date = transmission_date

                return True
        except FileNotFoundError:
            raise FileNotFoundError(f"Old DTCC file not found for testcase ID: {test_case_id}")

    @keyword
    def generate_random_value(self, prefix, num_digits, suffix):
        random_number = ''.join(random.choices("0123456789", k=num_digits))
        return prefix + random_number + suffix

    @keyword
    def generate_unique_number(self):
        current_time = datetime.now().strftime("%Y%m%d%H%M%S%f")[:-3]
        if len(current_time) < 20:
            current_time = current_time.ljust(20, '0')
        elif len(current_time) > 20:
            current_time = current_time[:20]

        modified_number = current_time[:17] + "K" + current_time[18:]
        return modified_number

    @keyword
    def generate_dtccfile(self, dtccFilePath, test_case_id):
        try:

            if self.fileProperties.oldDtccFileName is None:
                raise FileNotFoundError(f"Old DTCC file not found")

            last_six_digit = "{:06d}".format(self.file.random_number_create(999999))
            new_dtccfile_name = "DTCC.APPSUB.Q.D{}.C{}{}".format(datetime.now().strftime("%y%m%d"),
                                                                 datetime.now().strftime("%Y%m%d"),
                                                                 last_six_digit)
            self.fileProperties.newDtccFileName = new_dtccfile_name

            replacement_value = '{:04d}S{:02d}'.format(self.file.random_number_create(9999),
                                                       self.file.random_number_create(99))

            now = datetime.now()
            two_days_ago = now - timedelta(days=2)
            formatted_date = two_days_ago.strftime('%Y%m%d')

            new_app_control_number = replacement_value + self.fileProperties.app_control_no_value[7:]
            new_dis_trans_id_number = replacement_value + self.fileProperties.dis_trans_id_no_value[7:]
            new_doc_control_number = replacement_value + self.fileProperties.doc_control_no_value[7:]

            if self.get_transmission_date_status(test_case_id).lower() == 'yes':
                new_transmission_date = formatted_date
            else:
                new_transmission_date = self.fileProperties.transmission_date
            read_config = ReadConfig()
            old_dtccfile_path = read_config.getValueByKey(
                'OldDTCCFilePathNetworkDrive') + self.fileProperties.oldDtccFileName
            new_dtccfile_content = []

            with open(old_dtccfile_path, 'r') as old_DtccFile:
                for line in old_DtccFile:
                    line = line.replace(self.fileProperties.app_control_no_value, new_app_control_number)
                    line = line.replace(self.fileProperties.dis_trans_id_no_value, new_dis_trans_id_number)
                    line = line.replace(self.fileProperties.doc_control_no_value, new_doc_control_number)
                    line = line.replace(self.fileProperties.transmission_date, new_transmission_date)
                    new_dtccfile_content.append(line)

            new_dtccfile_path = dtccFilePath + '/' + new_dtccfile_name

            excel_file_path = self.excelSheet.getExcelSheetPath()
            client = self.excelSheet.get_value_from_excel_by_column_name(excel_file_path, self.excel_input_sheet_name,
                                                                         test_case_id, "client_code")

            if client == 'SBGC':
                self.fileProperties.newDtccFilePathSB = new_dtccfile_path
            else:
                self.fileProperties.newDtccFilePathMM = new_dtccfile_path

            with open(new_dtccfile_path, 'w') as new_file:
                new_file.writelines(new_dtccfile_content)

            if client == 'SBGC':
                self.global_all_dtcc_in_one.append(self.fileProperties.newDtccFilePathSB)
            else:
                self.global_all_dtcc_in_one.append(self.fileProperties.newDtccFilePathMM)

            return new_dtccfile_path
        except Exception as e:
            print("An error occurred while generating DTCC file:", str(e))

    @keyword
    def get_excel_testdata_by_group_id(self, group_id, sheet_name, excel_filepath):
        try:
            df = pd.read_excel(excel_filepath, sheet_name=sheet_name, dtype=str)
        except Exception as e:
            print(f"Error reading Excel file: {e}")
            return None, None
        filtered_df = df[df['Group'] == group_id]
        column_names = filtered_df.columns.tolist()
        filtered_data = filtered_df.to_numpy()
        return column_names, filtered_data

    @keyword
    def generate_new_DTCC_file_and_store_data_to_test_data_sheet(self, test_case_id, group_id, sheet_name):

        test_id = f"{self.file.get_current_date('%d%m%Y')}"

        project_dir = self.file.get_project_directory()
        read_config = ReadConfig()
        new_file_path = os.path.join(project_dir + read_config.getValueByKey('OutputGenerateDTCCFilesReport'),
                                     test_id)

        output_dtcc_path = os.path.join(new_file_path, 'Output')
        self.file.create_directory(output_dtcc_path)

        dtccFilePath = output_dtcc_path

        excel_file_path = self.excelSheet.getExcelSheetPath()
        old_dtcc_file_name = self.excelSheet.get_value_from_excel_by_column_name(excel_file_path,
                                                                                 self.excel_input_sheet_name,
                                                                                 test_case_id,
                                                                                 "old_dtcc_file_name")

        self.fileProperties.oldDtccFileName = old_dtcc_file_name
        if self.fileProperties.oldDtccFileName is None:
            raise FileNotFoundError(f"Old DTCC file not found for testcase ID: {test_case_id}")

        new_dtcc_file_path = self.generate_dtccfile(dtccFilePath, test_case_id)

        if new_dtcc_file_path is None:
            raise FileNotFoundError(f"New DTCC file not found for testcase ID: {test_case_id}")

        try:
            with open(new_dtcc_file_path, 'r') as file:
                file_content = file.read()

                new_app_control_number = file_content[
                                         file_content.find("B3301") + 5:file_content.find("B3301") + 25].strip()
                self.fileProperties.new_app_control_number_value = new_app_control_number

                new_dis_trans_id_number = file_content[
                                          file_content.find("B3304") + 82:file_content.find("B3304") + 112].strip()
                self.fileProperties.new_dis_trans_id_number_value = new_dis_trans_id_number

                new_doc_control_number = file_content[
                                         file_content.find("B3344") + 25:file_content.find("B3344") + 45].strip()
                self.fileProperties.new_doc_control_number_value = new_doc_control_number
                new_transmission_date = file_content[
                                        file_content.find("B30") + 33:file_content.find("B30") + 41].strip()
                self.fileProperties.transmission_date = new_transmission_date

        except FileNotFoundError:
            print(f"File '{self.fileProperties.newDtccFileName}' is not present.")

        self.get_excel_testdata_by_group_id(group_id, sheet_name, excel_file_path)

        direct_fields_to_write = [
            ("${test_case_id}", test_case_id),
            ("${new_dtcc_file_name}", self.fileProperties.newDtccFileName),
            ("${app_control_number}", self.fileProperties.new_app_control_number_value),
            ("${doc_control_number}", self.fileProperties.new_doc_control_number_value),
            ("${dist_trans_id_number}", self.fileProperties.new_dis_trans_id_number_value),
            ("${dtcc_file_creation_date}", self.file.get_cst_date('%m/%d/%Y'))
        ]

        # Fields where value should be looked up from the Excel input sheet
        excel_lookup_fields = [
            ("client_code", "${client_code}"),
            ("expected_Eapp_status", "${expected_eapp_status}"),
            ("company_name", "${company_name}"),
            ("Automation flow category", "${automation_flow_category}"),
            ("company_hierarchy_id", "${company_hierarchy_id}")
        ]

        for placeholder, value in direct_fields_to_write:
            self.excelSheet.write_value_to_excel_by_column_name(
                excel_file_path,
                self.excel_output_sheet_name,
                test_case_id,
                placeholder,
                value
            )

        for column_name, placeholder in excel_lookup_fields:
            value = self.excelSheet.get_value_from_excel_by_column_name(
                excel_file_path,
                self.excel_input_sheet_name,
                test_case_id,
                column_name
            )
            self.excelSheet.write_value_to_excel_by_column_name(
                excel_file_path,
                self.excel_output_sheet_name,
                test_case_id,
                placeholder,
                value
            )

        BuiltIn().log(f"TestID: {test_case_id} New DTCC file created: {self.fileProperties.newDtccFileName}")
        BuiltIn().log_to_console(f"TestID: {test_case_id} New DTCC file created: {self.fileProperties.newDtccFileName}")

    @keyword
    def upload_new_DTCC_file_to_NSCC_folder(self):
        try:

            new_dtcc_file_path_all_dtcc = self.global_all_dtcc_in_one[0] if self.global_all_dtcc_in_one else None
            if new_dtcc_file_path_all_dtcc is None:
                raise ValueError("New DTCC file not found. Cannot proceed with uploading.")
            read_config = ReadConfig()
            destination_path = read_config.getValueByKey('NSCCFolderPath')
            if len(self.global_all_dtcc_in_one) > 0:
                shutil.copy(new_dtcc_file_path_all_dtcc, destination_path)
                file_name = os.path.basename(new_dtcc_file_path_all_dtcc)
                BuiltIn().log(f"......................................................................")
                BuiltIn().log(f"Final DTCC file successfully uploaded to the NSCC folder: {file_name}")
                BuiltIn().log_to_console(f"......................................................................")
                BuiltIn().log_to_console(
                    f"Final DTCC file successfully uploaded to the NSCC folder: {file_name}")

        except ValueError as e:
            print(f"Error: {e}")

    @keyword
    def get_transmission_date_status(self, test_case_id):
        excel_file_path = self.excelSheet.getExcelSheetPath()
        transmission_date_status = self.excelSheet.get_value_from_excel_by_column_name(excel_file_path,
                                                                                       self.excel_input_sheet_name,
                                                                                       test_case_id,
                                                                                       "transmission_date_changed")
        return transmission_date_status

    @keyword
    def append_all_dtcc_into_one_dtcc(self):
        if len(self.global_all_dtcc_in_one) == 0:
            return len(self.global_all_dtcc_in_one)
        else:
            for file in self.global_all_dtcc_in_one:
                with open(file, 'r') as f:
                    lines = f.readlines()[2:]
                    self.all_dtcc_file_content.append(lines)

            last_file_path = self.global_all_dtcc_in_one[0]
            with open(last_file_path, 'a') as last_file:
                for content in self.all_dtcc_file_content[1:]:
                    last_file.writelines(content)
            return len(self.global_all_dtcc_in_one)

    @keyword
    def check_case_status_from_excel(self, test_case_id):
        excel_file_path = self.excelSheet.getExcelSheetPath()
        case_status = self.excelSheet.get_value_from_excel_by_column_name(excel_file_path,
                                                                          self.excel_input_sheet_name,
                                                                          test_case_id,
                                                                          "NIGO/IGO")
        return case_status

    @keyword
    def generate_dtcc_file_and_upload_dtcc(self, group_id):
        self.excelSheet.clear_sheet()
        excel_file_path = self.excelSheet.getExcelSheetPath()

        all_test_case_ids = self.excelSheet.get_excel_testdata_by_groupId(
            group_id, self.excel_input_sheet_name
        )
        assert all_test_case_ids, f"[ERROR] No test case IDs found for group_id: {group_id}"

        test_cases = []

        for test_case_id in all_test_case_ids:
            dtcc_required = self.excelSheet.get_value_from_excel_by_column_name(
                excel_file_path, self.excel_input_sheet_name, test_case_id, "DTCC_Required"
            )

            if not dtcc_required:
                continue

            dtcc_required = dtcc_required.strip().upper()
            test_cases.append({
                "test_case_id": test_case_id,
                "dtcc_required": dtcc_required == "YES"
            })

        test_cases.sort(key=lambda x: x["test_case_id"])

        dtcc_yes_found = False

        dtcc_required_ids = [tc["test_case_id"] for tc in test_cases if tc["dtcc_required"]]
        last_required_test_case_id = dtcc_required_ids[-1] if dtcc_required_ids else None

        for case in test_cases:
            test_case_id = case["test_case_id"]
            is_required = case["dtcc_required"]

            # Retrieve additional details for the test case
            flow_category = self.excelSheet.get_value_from_excel_by_column_name(
                excel_file_path, self.excel_input_sheet_name, test_case_id, "Automation flow category"
            )
            company_hierarchy = self.excelSheet.get_value_from_excel_by_column_name(
                excel_file_path, self.excel_input_sheet_name, test_case_id, "company_hierarchy_id"
            )
            dtcc_required_str = "YES" if is_required else "NO"

            self.excelSheet.write_value_to_excel_by_column_name(
                excel_file_path, self.excel_output_sheet_name, test_case_id, "${test_case_id}", test_case_id
            )
            self.excelSheet.write_value_to_excel_by_column_name(
                excel_file_path, self.excel_output_sheet_name, test_case_id, "${automation_flow_category}",
                flow_category
            )
            self.excelSheet.write_value_to_excel_by_column_name(
                excel_file_path, self.excel_output_sheet_name, test_case_id, "${company_hierarchy_id}",
                company_hierarchy
            )
            self.excelSheet.write_value_to_excel_by_column_name(
                excel_file_path, self.excel_output_sheet_name, test_case_id, "${dtcc_required}", dtcc_required_str
            )

            if not is_required:
                BuiltIn().log_to_console(f"[INFO] Skipped {test_case_id} — DTCC_Required is NO")
                BuiltIn().log(f"[INFO] Skipped {test_case_id} — DTCC_Required is NO")
                continue

            dtcc_yes_found = True

            # Extract values from the old DTCC file
            status = self.extract_values_from_old_dtcc_file(test_case_id)
            assert status is not None, f"[ERROR] Extraction returned None for test_case_id: {test_case_id}"
            assert status, f"[ERROR] Extraction failed for test_case_id: {test_case_id}"

            try:
                # Generate the new DTCC file and store data to the test data sheet
                self.generate_new_DTCC_file_and_store_data_to_test_data_sheet(
                    test_case_id, group_id, self.excel_input_sheet_name
                )
            except Exception as e:
                BuiltIn().log(f"[ERROR] Exception while processing {test_case_id}: {e}")
                continue

            # Check if the current test case is the last DTCC-required test case
            if test_case_id == last_required_test_case_id:
                dtcc_files_count = self.append_all_dtcc_into_one_dtcc()
                assert dtcc_files_count > 0, f"[ERROR] No DTCC files appended for group_id: {group_id} at test_case_id: {test_case_id}"
                self.upload_new_DTCC_file_to_NSCC_folder()
                time.sleep(480)

        # Ensure that at least one DTCC-required test case was processed
        assert dtcc_yes_found, f"[ERROR] No DTCC_Required = YES test cases for group_id: {group_id}"
