*** Settings ***
Library    RequestsLibrary
Library    Collections
Library    allure_robotframework
Library    Process
Resource    ../../resources/Reporting/ReportingSetup.resource
Suite Setup    Setup Enhanced Allure Environment    QA    API
Suite Teardown    Create Test Execution Summary    2    1    1
Test Setup    Setup Test With Console Logging
Test Teardown    Teardown Test With Console Logging

Library    FakerLibrary





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
    [Documentation]    Enhanced API test with console logging integration
    [Tags]
    ...  allure.label.epic:Web interface
    ...  allure.label.feature:Essential features
    ...  allure.label.story:Authentication
    ...  allure.severity:critical
    
    Log Step To Console And Allure    Starting user information retrieval test
    Log Process To Console And Allure    Creating HTTP session    Connecting to ${baseUrl}
    
    Create Session    mysession    ${baseUrl}
    
    Log Step To Console And Allure    Sending GET request to users endpoint    Endpoint: ${path}
    ${actualResponce}=     GET On Session    mysession     ${path}
    ${response_body}=    Set Variable    ${actualResponce.json()}
    
    Log Step To Console And Allure    Processing API response    Response received with ${actualResponce.status_code} status
    Log To Console    Response Body: ${response_body}
    
    # Validate response structure
    Should Not Be Empty    ${response_body}
    Should Contain    ${response_body}    users
    
    Log Step To Console And Allure    User information test completed successfully

getStatusCode
    [Documentation]    Enhanced status code validation test with detailed logging
    [Tags]    smoke    feature:API    story:Status Check    priority:medium
    
    Log Step To Console And Allure    Starting status code validation test
    Log Process To Console And Allure    Establishing API connection    Target URL: ${baseUrl}${path}
    
    Create Session    mysession    ${baseUrl}
    
    Log Step To Console And Allure    Executing API call for status validation
    ${actualResponce}=     GET On Session    mysession     ${path}
    ${actual_status_code}=    Set Variable    ${actualResponce.status_code}
    
    Log Step To Console And Allure    Validating status code    Expected: ${expected_status_code}, Actual: ${actual_status_code}
    Log To Console    Status Code Validation: Expected=${expected_status_code}, Actual=${actual_status_code}
    
    Run Keyword If    ${actual_status_code} != ${expected_status_code}
    ...    Log Failure To Console And Allure    Status code mismatch    Expected ${expected_status_code} but got ${actual_status_code}
    
    Should Be Equal As Integers    ${actual_status_code}    ${expected_status_code}
<<<<<<< HEAD
    
    Log Step To Console And Allure    Status code validation completed successfully

Enhanced API Test With Error Handling
    [Documentation]    Demonstrates error handling and failure logging
    [Tags]    allure.severity:normal    feature:Error_Handling
    
    Log Step To Console And Allure    Starting enhanced API test with error scenarios
    
    TRY
        Log Process To Console And Allure    Testing invalid endpoint    Endpoint: /invalid-endpoint
        Create Session    testsession    ${baseUrl}
        GET On Session    testsession    /invalid-endpoint
        Log Step To Console And Allure    Invalid endpoint test - unexpected success
    EXCEPT    AS    ${error}
        Log Step To Console And Allure    Expected error caught    Error: ${error}
        Log To Console    Error handling demonstration: ${error}
    END
    
    Log Step To Console And Allure    Error handling test completed
    
=======
    #demo
>>>>>>> 0cf56ad3845949a99f952ca7a33721626a7eec62
