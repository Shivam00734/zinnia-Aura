*** Settings ***
Library    ../../Libraries/ExcelLibrary.py
Library    Collections
#Library    DataDriver    ${CURDIR}/../../resources/TestD.xlsx    sheet_name=Sheet1

*** Test Cases ***
Verify User Logins from Excel Data
    ${test_data}=    Get Excel Data As List    ${CURDIR}/../../resources/xml/TestD.xlsx    sheet_name=Sheet1
    
    FOR    ${row}    IN    @{test_data}
        Log To Console    Testing with username: ${row.username} and password: ${row.password}
        
        # Example Test Steps:
        # Input Text    username_field    ${row.username}
        # Input Text    password_field    ${row.password}
        # Click Button    login_button
        # Page Should Contain    ${row.expected_message}
    END