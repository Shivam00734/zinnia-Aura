from jproperties import Properties
from robot.api.deco import library, keyword
from resources.utilities.FileUtils import FileUtils

@library
class ReadConfig:
    def __init__(self):
        self.file = FileUtils()
        self.configs = Properties()
        self.project_dir = self.file.get_project_directory()

        properties_files = [
            r'\resources/config\api_config.properties',
            r'\resources/config\config.properties',
        ]

        for properties_file in properties_files:
            with open(self.project_dir + properties_file, 'rb') as config_file:
                self.configs.load(config_file)

    @keyword
    def encrypt(self, text, shift):
        encrypted_text = ""
        for char in text:
            if char.isalpha():
                shifted_char = chr((ord(char.lower()) - 97 + shift) % 26 + 97)
                if char.isupper():
                    shifted_char = shifted_char.upper()
                encrypted_text += shifted_char
            else:
                encrypted_text += char
        return encrypted_text

    @keyword
    def decrypt(self, text, shift):
        return self.encrypt(text, -shift)

    @keyword
    def getEncryptValueByKey(self, key):
        value = self.configs.get(key).data
        return self.encrypt(value, 3)

    @keyword
    def getValueByKey(self, key):
        return self.configs.get(key).data

