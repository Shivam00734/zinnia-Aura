from robot.api.deco import keyword, library
import os
import xml.etree.ElementTree as ET
from resources.utilities.FileUtils import FileUtils
from resources.utilities.ReadConfig import ReadConfig
from resources.vo.FilePropertiesVo import FilePropertiesVo
from io import BytesIO
import requests
from robot.libraries.BuiltIn import BuiltIn


@library
class AccordeXmlUpdate:
    file = FileUtils()
    read_config = ReadConfig()
    fileProperties = FilePropertiesVo()
    @keyword
    def generate_new_policy_xml_everly_client(self, old_pol_number):
        new_policy_number = None
        payee_name = None
        xml_path = rf"{self.read_config.getValueByKey('policy_accorde_input_xml_file_path')}{old_pol_number}.xml"
        output_dir = self.read_config.getValueByKey('policy_accorde_output_xml_file_path')

        tree = ET.parse(xml_path)
        root = tree.getroot()

        namespaces = {'ns': 'http://ACORD.org/Standards/Life/2'}
        ET.register_namespace('', namespaces['ns'])

        for pol_number in root.findall(".//ns:PolNumber", namespaces):
            six_digit = "{:06d}".format(self.file.random_number_create(999999))

            new_policy_number = old_pol_number[:-6] + six_digit
            pol_number.text = new_policy_number

        party_pi = root.find(".//ns:Party[@id='Party_PI_1']", namespaces)
        if party_pi is not None:
            # Update GovtID
            govt_id_elem = party_pi.find("ns:GovtID", namespaces)
            if govt_id_elem is not None:
                govt_id_elem.text = self.file.generate_unique_digits(9)

            person_elem = party_pi.find("ns:Person", namespaces)
            if person_elem is not None:
                first_name = person_elem.find("ns:FirstName", namespaces)
                last_name = person_elem.find("ns:LastName", namespaces)
                if last_name is not None:
                    new_last_name = self.file.generate_unique_upper_string()
                    last_name.text = new_last_name

                    full_name_elem = party_pi.find("ns:FullName", namespaces)
                    if full_name_elem is not None and first_name is not None:
                        full_name_elem.text = f"{first_name.text} {new_last_name}"
                        payee_nam = full_name_elem.text
                        payee_name = self.file.format_second_word(payee_nam)

        party_pb = root.find(".//ns:Party[@id='Party_PB_Primary_Bene_1']", namespaces)
        if party_pb is not None:
            person_elem = party_pb.find("ns:Person", namespaces)
            if person_elem is not None:
                last_name = person_elem.find("ns:LastName", namespaces)
                if last_name is not None:
                    last_name.text = self.file.generate_unique_upper_string()

        party_pa = root.find(".//ns:Party[@id='Party_PA_Agent_1']", namespaces)
        if party_pa is not None:
            person_elem = party_pa.find("ns:Person", namespaces)
            if person_elem is not None:
                last_name = person_elem.find("ns:LastName", namespaces)
                if last_name is not None:
                    last_name.text = self.file.generate_unique_upper_string()

        os.makedirs(output_dir, exist_ok=True)

        output_file_path = os.path.join(output_dir, f"{new_policy_number}.xml")

        tree.write(output_file_path, encoding='utf-8', xml_declaration=True)

        xml_bytes = BytesIO()
        tree.write(xml_bytes, encoding='utf-8', xml_declaration=True)
        updated_xml_content = xml_bytes.getvalue().decode('utf-8')

        return new_policy_number, payee_name, updated_xml_content

    @keyword
    def generate_new_policy_xml_welb_client(self, old_pol_number):
        new_policy_number = None
        payee_name = None
        xml_path = rf"{self.read_config.getValueByKey('policy_accorde_input_xml_file_path')}{old_pol_number}.xml"
        output_dir = self.read_config.getValueByKey('policy_accorde_output_xml_file_path')

        tree = ET.parse(xml_path)
        root = tree.getroot()

        namespaces = {'ns': 'http://ACORD.org/Standards/Life/2'}
        ET.register_namespace('', namespaces['ns'])

        for pol_number in root.findall(".//ns:PolNumber", namespaces):
            six_digit = "{:06d}".format(self.file.random_number_create(999999))

            new_policy_number = old_pol_number[:-6] + six_digit
            pol_number.text = new_policy_number

        party_pi = root.find(".//ns:Party[@id='Party_Annuitant_1']", namespaces)
        if party_pi is not None:
            # Update GovtID
            govt_id_elem = party_pi.find("ns:GovtID", namespaces)
            if govt_id_elem is not None:
                govt_id_elem.text = self.file.generate_unique_digits(9)

            person_elem = party_pi.find("ns:Person", namespaces)
            if person_elem is not None:
                first_name = person_elem.find("ns:FirstName", namespaces)
                last_name = person_elem.find("ns:LastName", namespaces)
                if last_name is not None:
                    new_last_name = self.file.generate_unique_upper_string()
                    last_name.text = new_last_name

                    full_name_elem = party_pi.find("ns:FullName", namespaces)
                    if full_name_elem is not None and first_name is not None:
                        full_name_elem.text = f"{first_name.text} {new_last_name}"
                        payee_nam = full_name_elem.text
                        payee_name = self.file.format_second_word(payee_nam)

        party_pb = root.find(".//ns:Party[@id='Party_PB_Primary_Bene_1']", namespaces)
        if party_pb is not None:
            person_elem = party_pb.find("ns:Person", namespaces)
            if person_elem is not None:
                last_name = person_elem.find("ns:LastName", namespaces)
                if last_name is not None:
                    last_name.text = self.file.generate_unique_upper_string()

        party_pa = root.find(".//ns:Party[@id='Party_PA_Agent_1']", namespaces)
        if party_pa is not None:
            person_elem = party_pa.find("ns:Person", namespaces)
            if person_elem is not None:
                last_name = person_elem.find("ns:LastName", namespaces)
                if last_name is not None:
                    last_name.text = self.file.generate_unique_upper_string()

        os.makedirs(output_dir, exist_ok=True)

        output_file_path = os.path.join(output_dir, f"{new_policy_number}.xml")

        tree.write(output_file_path, encoding='utf-8', xml_declaration=True)

        xml_bytes = BytesIO()
        tree.write(xml_bytes, encoding='utf-8', xml_declaration=True)
        updated_xml_content = xml_bytes.getvalue().decode('utf-8')

        return new_policy_number, payee_name, updated_xml_content

    @keyword
    def upload_policy(self, xml_payload: str):
        url = 'https://qa-zahara-api.zinnia.io/v1/issuance'
        headers = {
            'accept': 'application/json, text/plain, */*',
            'accept-language': 'en-US,en;q=0.9',
            'content-type': 'application/xml',
            'origin': 'https://qa-zahara-ui.zinnia.io',
            'priority': 'u=1, i',
            'referer': 'https://qa-zahara-ui.zinnia.io/',
            'sec-ch-ua': '"Chromium";v="136", "Google Chrome";v="136", "Not.A/Brand";v="99"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Windows"',
            'sec-fetch-dest': 'empty',
            'sec-fetch-mode': 'cors',
            'sec-fetch-site': 'same-site',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/136.0.0.0 Safari/537.36',
        }

        response = requests.post(url, headers=headers, data=xml_payload)

        if response.status_code == 201:
            BuiltIn().log(f"Policy has been uploaded successfully on Zahara")
            BuiltIn().log_to_console(f"Policy has been uploaded successfully on Zahara")
        else:
            raise AssertionError(f'Upload failed: Policy was not uploaded successfully on Zahara: {response.status_code}, Response: {response.text}')


