Library    ../../Faker/FakerDataLib.py



*** Test Cases ***
Generate Fake User Data
    ${user}=    Get Fake User
    Log To Console    Name: ${user['name']}
    Log To Console    Email: ${user['email']}
    Log To Console    Address: ${user['address']}
    Log To Console    Phone: ${user['phone']}
