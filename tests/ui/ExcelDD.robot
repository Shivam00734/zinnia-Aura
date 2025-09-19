# *** Settings ***
# Library    SeleniumLibrary
# Resource    ../../resources/Loginresources.robot
# Library    DataDriver    ${CURDIR}/../../resources/TestD.xlsx    sheet_name=Sheet1

# Suite Setup    Open my Browser
# Suite Teardown    Close Browser
# Test Template    Invalid Login

# *** Test Cases ***

# LoginTestwithExcelData using ${username}  and  ${password}



# *** Keywords ***
# Invalid Login

#     [Arguments]    ${username}    ${password}
#     Input username    ${username}
#     Input password    ${password}
#     Click login button
#     Error message should be visible


*** Settings ***

Library           SeleniumLibrary
Resource          ../../resources/Loginresources.robot
Library           DataDriver    ${CURDIR}/../../resources/TestD.xlsx    sheet_name=Sheet1

Suite Setup       Open my Browser
Suite Teardown    Close Browser
Test Template     Invalid Login



*** Test Cases ***
LoginTestwithExcel using ${username}     ${password}




*** Keywords ***
Invalid Login
    [Arguments]    ${username}    ${password}
    Input username    ${username}
    Input password    ${password}
    Click login button
    Error message should be visible
