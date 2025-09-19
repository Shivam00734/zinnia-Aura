import os
import xml.dom.minidom as minidom
import time
import pandas as pd
from robot.api.deco import library, keyword
from robot.libraries.BuiltIn import BuiltIn
from resources.keywords.api_keywords.OnBaseApi import OnBaseApi
from resources.utilities.ExcelUtilities import ExcelUtilities
from resources.utilities.FileUtils import FileUtils
from resources.utilities.ReadConfig import ReadConfig
from resources.vo.FilePropertiesVo import FilePropertiesVo


@library
class GenerateAttachment:
    fileProperties = FilePropertiesVo()
    file = FileUtils()
    excel_input_sheet_name = "Input_data"
    excel_output_sheet_name = "output_data"
    onbase_api = OnBaseApi()
    
    def __init__(self):
        self.excelSheet = ExcelUtilities()  # Dynamic instantiation

    @keyword
    def create_xml_file(self, testcase_id):
        project_dir = self.file.get_project_directory()
        read_config = ReadConfig()
        input_file_path = read_config.getValueByKey('ZinniaLiveTestDataND')
        old_file_name_value = self.excelSheet.get_value_from_excel_by_column_name(input_file_path,
                                                                                  self.excel_input_sheet_name,
                                                                                  testcase_id, "old_xml_file_name")

        input_path = read_config.getValueByKey('OldXMLFilePathNetworkDrive') + old_file_name_value

        doc = minidom.parse(input_path)
        six_digit = "{:06d}".format(self.file.random_number_create(999999))
        two_digit = "{:02d}".format(self.file.random_number_create(99))

        form_name_value = "ZLAttachment Form-TC" + two_digit
        self.fileProperties.form_name = form_name_value
        doc_control_no_value = self.excelSheet.get_value_from_excel_by_column_name(input_file_path,
                                                                                   self.excel_output_sheet_name,
                                                                                   testcase_id, "${doc_control_number}")

        self.fileProperties.docControlNoValue = doc_control_no_value
        trans_ref_guid_value = "DF5CACEA-4B7B-203C-BCEA-5E031" + six_digit + "ZL"
        self.fileProperties.transRefGUIDValue = trans_ref_guid_value

        for trans_ref_guid_node in doc.getElementsByTagName('TransRefGUID'):
            trans_ref_guid_node.firstChild.data = trans_ref_guid_value

        for form_name in doc.getElementsByTagName('FormName'):
            form_name.firstChild.data = form_name_value

        for doc_control_number_node in doc.getElementsByTagName('DocumentControlNumber'):
            doc_control_number_node.firstChild.data = doc_control_no_value

        form_instances = doc.getElementsByTagName('FormInstance')
        last_form_instance = form_instances[-1] if form_instances else None

        num_instances = self.excelSheet.get_value_from_excel_by_column_name(input_file_path,
                                                                            self.excel_input_sheet_name, testcase_id,
                                                                            "number_of_attachment")

        self.excelSheet.write_value_to_excel_by_column_name(input_file_path, "output_data", testcase_id,
                                                            "${number_of_attachment}",
                                                            num_instances)

        for i in range(2, num_instances + 1):

            form_instance = doc.createElement("FormInstance")
            form_instance.setAttribute("id", "FormInstance_" + str(i))
            form_instance.setAttribute("ReceiverPartyID", "Party_Recipient")
            form_instance.setAttribute("ProviderPartyID", "Party_Sender")

            form_name = doc.createElement("FormName")
            form_name.appendChild(doc.createTextNode(self.fileProperties.form_name))
            form_instance.appendChild(form_name)

            provider_form_number = doc.createElement("ProviderFormNumber")
            provider_form_number.appendChild(doc.createTextNode("DTCCAttachment"))
            form_instance.appendChild(provider_form_number)

            doc_control_number = doc.createElement("DocumentControlNumber")
            doc_control_number.appendChild(doc.createTextNode(doc_control_no_value))
            form_instance.appendChild(doc_control_number)

            doc_control_type = doc.createElement("DocumentControlType")
            doc_control_type.setAttribute("tc", "1")
            doc_control_type.appendChild(doc.createTextNode("Order Entry Control Number"))
            form_instance.appendChild(doc_control_type)

            originating_trans_type = doc.createElement("OriginatingTransType")
            originating_trans_type.setAttribute("tc", "103")
            originating_trans_type.appendChild(doc.createTextNode("New Business"))
            form_instance.appendChild(originating_trans_type)

            attachment = doc.createElement("Attachment")
            attachment.setAttribute("id", "xx40074838")

            date_created = doc.createElement("DateCreated")
            date_created.appendChild(doc.createTextNode("2023-04-24"))
            attachment.appendChild(date_created)

            attachment_basic_type = doc.createElement("AttachmentBasicType")
            attachment_basic_type.setAttribute("tc", "3")
            attachment_basic_type.appendChild(doc.createTextNode("File"))
            attachment.appendChild(attachment_basic_type)

            form_instance.appendChild(attachment)

            if last_form_instance:
                last_form_instance.parentNode.insertBefore(form_instance, last_form_instance.nextSibling)
            else:
                olife_node = doc.getElementsByTagName('OLifE')[0]
                olife_node.appendChild(form_instance)

            last_form_instance = form_instance

            doc.createTextNode('\n')

        output_file_name = "_" + trans_ref_guid_value + "_510_.XML"
        self.fileProperties.newXmlFileName = output_file_name


        current_date_time = self.file.get_current_date_with_timezone_format()

        test_id = f"{self.file.get_current_date('%d%m%Y')}/TC_{current_date_time}"
        read_config = ReadConfig()
        new_file_path = os.path.join(read_config.getValueByKey('xml_attachment_report_path'),
                                     test_id)
        self.file.create_directory(new_file_path)

        xml_output_path = os.path.join(new_file_path, output_file_name)

        with open(xml_output_path, 'w') as output_file:
            doc.writexml(output_file)

        if os.path.exists(xml_output_path):
            assert True
        else:
            assert False, f"XML file was not created at: {xml_output_path}"

        return new_file_path

    @keyword
    def store_xml_data_in_excel_sheet(self, test_case_id):
        input_file_path = self.read_config.getValueByKey('ZinniaLiveTestDataND')
        form_name = self.fileProperties.form_name

        self.excelSheet.write_value_to_excel_by_column_name(input_file_path, self.excel_output_sheet_name, test_case_id,
                                                            "${new_xml_file_name}",
                                                            self.fileProperties.newXmlFileName)

        self.excelSheet.write_value_to_excel_by_column_name(input_file_path, self.excel_output_sheet_name, test_case_id,
                                                            "${attachment_form_name}",
                                                            form_name)

    @keyword
    def create_attachment_form(self, testcase_id, output_file_path):
        input_file_path = self.read_config.getValueByKey('ZinniaLiveTestDataND')
        num_files = self.excelSheet.get_value_from_excel_by_column_name(input_file_path, self.excel_input_sheet_name,
                                                                        testcase_id, "number_of_attachment")

        for i in range(2, num_files + 2):

            old_file_name = self.excelSheet.get_value_from_excel_by_column_name(input_file_path,
                                                                                self.excel_input_sheet_name,
                                                                                testcase_id, "old_attachment_form_name")
            doc_control_number = self.excelSheet.get_value_from_excel_by_column_name(input_file_path,
                                                                                     self.excel_output_sheet_name,
                                                                                     testcase_id,
                                                                                     "${doc_control_number}")

            new_file_name = doc_control_number + f"_510_ATTACHMENT{i - 1}.pdf"

            old_file_path = self.read_config.getValueByKey('OldAttachmentFilePathNetworkDrive') + old_file_name

            output_attachment_path = os.path.join(output_file_path, new_file_name)

            with open(old_file_path, 'rb') as old_file:
                with open(output_attachment_path, 'wb') as new_file:
                    new_file.write(old_file.read())

            if os.path.exists(output_attachment_path):
                assert True
            else:
                assert False, f"Attachment file {new_file_name} was not created at path: {output_attachment_path}"

            self.fileProperties.attachment_list.append(new_file_name)

            self.excelSheet.write_value_to_excel_by_column_name(input_file_path, self.excel_output_sheet_name,
                                                                testcase_id,
                                                                "${new_attachment_file_name}",
                                                                new_file_name)

    @keyword
    def upload_file_on_network_drive(self, file_path, destination_directory):
        try:
            with open(file_path, 'rb') as file:
                file_bytes = file.read()
                file_name = os.path.basename(file_path)
                destination_path = os.path.join(destination_directory, file_name)
                with open(destination_path, 'wb') as destination_file:
                    destination_file.write(file_bytes)
        except IOError as e:
            print("Error uploading file:", e)
            raise

    @keyword
    def upload_xml_and_attachment_form(self, test_case_id, output_file_path, contract_number_dict):
        input_file_path = self.read_config.getValueByKey('ZinniaLiveTestDataND')
        new_xml_file_name = self.excelSheet.get_value_from_excel_by_column_name(input_file_path,
                                                                                self.excel_output_sheet_name,
                                                                                test_case_id, "${new_xml_file_name}")
        xml_file_path = os.path.join(output_file_path, new_xml_file_name)

        destination_directory = self.read_config.getValueByKey('IncomingFolderPath')
        self.upload_file_on_network_drive(xml_file_path, destination_directory)

        new_attachment_file_name = self.excelSheet.get_value_from_excel_by_column_name(input_file_path,
                                                                                       self.excel_output_sheet_name,
                                                                                       test_case_id,
                                                                                       "${new_attachment_file_name}")
        file_names = new_attachment_file_name.split(',')

        for array_list_value in file_names:
            attachment_file_path = os.path.join(output_file_path, array_list_value)
            self.upload_file_on_network_drive(attachment_file_path, destination_directory)
        message = (
            f"TestCase_ID: {test_case_id}, Contract_Number: {contract_number_dict.get(test_case_id)}\n"
            f"[PASS] Successfully processed and uploaded files for {test_case_id}\n"
            f"New Attachment file name: {new_attachment_file_name}\n"
            f"New XML file name: {new_xml_file_name}\n"
        )

        BuiltIn().log(f"{message}\n")
        BuiltIn().log_to_console(f"\n{message}")

    @keyword
    def check_attachment_required(self, testcase_id):
        input_file_path = self.read_config.getValueByKey('ZinniaLiveTestDataND')
        status_attachment_required = self.excelSheet.get_value_from_excel_by_column_name(input_file_path,
                                                                                         self.excel_input_sheet_name,
                                                                                         testcase_id,
                                                                                         "Attachment Required")
        self.excelSheet.write_value_to_excel_by_column_name(input_file_path, self.excel_output_sheet_name, testcase_id,
                                                            "${attachment_required}",
                                                            status_attachment_required)

        return status_attachment_required

    def wait_until_case_generated(self, test_case_id, timeout_minutes=30, retry_interval=120):
        max_attempts = int((timeout_minutes * 60) / retry_interval)
        for attempt in range(max_attempts):
            try:
                if self.onbase_api.validate_nb_application_case_status(test_case_id):
                    return True
            except Exception as e:
                print(f"[WARN] Error while checking status for {test_case_id}: {e}")
            time.sleep(retry_interval)

        assert False, f"Case not generated on OnBase for {test_case_id} within {timeout_minutes} minutes"

    @keyword
    def verify_creation_of_nb_application_case_in_onbase_and_upload_xml_file_and_attachment(self, contract_number_dict):
        file_path = self.read_config.getValueByKey('ZinniaLiveTestDataND')
        assert file_path, "[ERROR] Config value for 'ZinniaLiveTestDataND' is missing or empty."

        try:
            data = pd.read_excel(file_path, sheet_name=self.excel_output_sheet_name)
        except Exception as e:
            raise AssertionError(f"[ERROR] Failed to read Excel file at {file_path}: {e}")

        test_case_ids = data.get("${test_case_id}", []).dropna().tolist()
        assert test_case_ids, "[ERROR] No test case IDs found in the Excel sheet."

        attachment_present = False

        for test_case_id in test_case_ids:
            status_for_attachment_required = self.check_attachment_required(test_case_id)
            assert status_for_attachment_required is not None, f"[ERROR] Attachment status is None for {test_case_id}"

            status_str = str(status_for_attachment_required).strip().upper()
            assert status_str in ["YES",
                                  "NO"], f"[ERROR] Unexpected attachment requirement status for {test_case_id}: {status_for_attachment_required}"

            if status_str == 'YES':
                try:
                    output_file_path = self.create_xml_file(test_case_id)
                    assert output_file_path, f"[ERROR] XML file path not generated for {test_case_id}"

                    self.store_xml_data_in_excel_sheet(test_case_id)

                    self.create_attachment_form(test_case_id, output_file_path)

                    self.upload_xml_and_attachment_form(test_case_id, output_file_path, contract_number_dict)
                    attachment_present = True
                except Exception as e:
                    error_message = f"[ERROR] File generation or upload failed for {test_case_id}: {e}"
                    BuiltIn().log(error_message, level="ERROR")
                    raise AssertionError(f"[ASSERTION FAILED] Processing failed for {test_case_id}: {e}")

            elif status_str == 'NO':
                message = (
                    f"TestCase_ID: {test_case_id}, Contract_Number will be {contract_number_dict.get(test_case_id)}\n"
                    f"[PASS] Attachment not required for : {test_case_id}\n"
                )

                BuiltIn().log(f"{message}\n")
                BuiltIn().log_to_console(f"\n{message}")



        if attachment_present:
            time.sleep(900)
