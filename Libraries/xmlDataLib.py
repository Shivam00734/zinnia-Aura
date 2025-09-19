import xml.etree.ElementTree as ET

class XmlDataLib:
    def get_users(self, filepath):
        tree = ET.parse(filepath)
        root = tree.getroot()
        users = []

        for user_elem in root.findall('User'):
            user = {
                'name': user_elem.find('Name').text,
                'email': user_elem.find('Email').text,
                'phone': user_elem.find('Phone').text
            }
            users.append(user)

        return users
