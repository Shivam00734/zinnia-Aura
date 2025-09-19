import configparser
from robot.libraries.BuiltIn import BuiltIn
from robot.api.deco import library, keyword
from resources.utilities.FileUtils import FileUtils


@library
class ReadProperties:
    file = FileUtils()

    @keyword
    def read_properties(self, fineName):
        project_dir = self.file.get_project_directory()
        filepath = project_dir + "/Resources/" + fineName
        config = configparser.ConfigParser()
        with open(filepath) as f:
            file_content = '[DEFAULT]\n' + f.read()
        config.read_string(file_content)
        properties = {key: value for key, value in config.items('DEFAULT')}
        return properties

    @keyword
    def set_robot_variables(self, properties):
        for key, value in properties.items():
            BuiltIn().set_global_variable(f'${{{key.upper()}}}', value)