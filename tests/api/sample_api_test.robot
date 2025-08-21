*** Settings ***
Library    RequestsLibrary
Library    Collections
Resource    ../../resources/ReportingSetup.resource
Resource    ../../resources/AllureLabels.resource
Suite Setup    Setup Allure Reporting

*** Test Cases ***
getUserInformation
    [Documentation]    This test case is to get user information
    [Tags]    smoke    feature:Login
    Mark As Critical Priority
    Create Session    mysession    ${baseUrl}
    ${actualResponce}=     GET On Session    mysession     ${path}
    ${response_body}=    Set Variable    ${actualResponce.json()}
    Log To Console    ${response_body}

getStatusCode
    [Documentation]    This test fetches user info and validates response structure.
    [Tags]    smoke    feature:API    @allure.label.priority:P1    @allure.label.layer:API
    Create Session    mysession    ${baseUrl}
    ${actualResponce}=     GET On Session    mysession     ${path}
    ${actual_status_code}=    Set Variable    ${actualResponce.status_code}
    Log To Console    ${actual_status_code}
    Should Be Equal As Integers    ${actual_status_code}    ${expected_status_code}

getUserName
    [Documentation]    This test fetches user info and validates response structure.
    [Tags]    smoke    feature:User    @allure.label.priority:P0    @allure.label.layer:API
    Create Session    mysession    ${baseUrl}
    ${actualResponce}=     GET On Session    mysession     ${path}
    ${response_body}=    Set Variable    ${actualResponce.json()}
    ${user_name}=    Set Variable    ${response_body}[users][${expected_user_id}][firstName]
    Log To Console    ${user_name}
    Should Be Equal As Strings    ${user_name}    ${expected_user_name}

getUserPhoneNumber
    [Documentation]    This test validates user phone number
    [Tags]    smoke    feature:User
    Mark As Medium Priority
    Create Session    mysession    ${baseUrl}
    ${actualResponce}=     GET On Session    mysession     ${path}
    ${response_body}=    Set Variable    ${actualResponce.json()}
    ${user_phone_number}=    Set Variable    ${response_body}[users][${expected_user_id}][phone]
    Log To Console    ${user_phone_number}
    Should Be Equal As Strings    ${user_phone_number}    ${expected_user_phone_number}

getUserEmail
    
    [Documentation]    This test validates user email
    [Tags]    smoke    feature:User    story:Contact Details    severity:minor
    Pass Execution If    True    SKIP    Skipping this test case intentionally
    Create Session    mysession    ${baseUrl}
    ${actualResponce}=     GET On Session    mysession     ${path}
    ${response_body}=    Set Variable    ${actualResponce.json()}
    ${user_email}=    Set Variable    ${response_body}[users][${expected_user_id}][email]
    Log To Console    ${user_email}
    Should Be Equal As Strings    ${user_email}    ${expected_user_email}

