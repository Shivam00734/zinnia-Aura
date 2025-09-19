from faker import Faker

class FakerDataLib:
    ROBOT_LIBRARY_SCOPE = 'GLOBAL'
    
    def __init__(self):
        self.fake = Faker()
    
    def get_fake_user(self):
        return {
            "name": self.fake.name(),
            "email": self.fake.email(),
            "address": self.fake.address(),
            "phone": self.fake.phone_number()
        }