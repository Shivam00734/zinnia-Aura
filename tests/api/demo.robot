*** Settings ***
Library    RequestsLibrary
Library    Collections
Library    allure_robotframework

Resource    ../resources/ReportingSetup.resource
Suite Setup    Setup Allure Reporting



** Variables ***
${baseUrl}    https://dummyjson.com/
${path}       users
${expected_status_code}    200
${expected_user_name}    Emily
${expected_user_id}     0
${expected_user_phone_number}    +1 234 567 890
${expected_user_email}    emily@example

*** Test Cases ***
getUserInformation
    
    # Set Suite Property    suite_name    API Test Suite
   # Set Allure Severity    critical

  # Set Allure Report Title    My Custom API Test Report 
   # [Tags]    smoke    feature:Login    story:Valid Login

    [Tags]
    ...  allure.label.epic:Web interface
    ...  allure.label.feature:Essential features
    ...  allure.label.story:Authentication
    
    Create Session    mysession    ${baseUrl}
    ${actualResponce}=     GET On Session    mysession     ${path}
    ${response_body}=    Set Variable    ${actualResponce.json()}
    Log To Console    ${response_body}

getStatusCode
 
    [Tags]    smoke    feature:API    story:Status Check    priority:medium
    Create Session    mysession    ${baseUrl}
    ${actualResponce}=     GET On Session    mysession     ${path}
    ${actual_status_code}=    Set Variable    ${actualResponce.status_code}
    Log To Console    ${actual_status_code}
    Should Be Equal As Integers    ${actual_status_code}    ${expected_status_code}
    
