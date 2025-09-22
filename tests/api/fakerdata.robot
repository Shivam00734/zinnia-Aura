*** Settings ***
Library    FakerLibrary    seed=234
Library    Collections
Library    RequestsLibrary
Resource   ../../resources/Reporting/ReportingSetup.resource

Suite Setup    Setup Enhanced Allure Environment    QA    Data_Generation
Suite Teardown    Create Test Execution Summary    1    1    0
Test Setup    Setup Test With Console Logging
Test Teardown    Teardown Test With Console Logging

*** Test Cases ***
Creating Fake Data
    [Documentation]    Generate fake user data using FakerLibrary with console logging
    [Tags]    Test Type: Smoke    allure.severity:normal    feature:Data_Generation
    
    Log Step To Console And Allure    Starting fake data generation process
    
    Log Process To Console And Allure    Generating user profile data    Using FakerLibrary with seed=234
    ${first_name}=    FakerLibrary.first_name
    ${last_name}=  FakerLibrary.last_name
    ${email}=    FakerLibrary.email
    ${phonenumb}=     FakerLibrary.Phone Number
    ${address}=      FakerLibrary.address

    Log Step To Console And Allure    Logging generated data to console and Allure
    Log    Name: ${first_name}
    Log To Console    Last name: ${last_name}
    Log To Console    Email id: ${email}
    Log To Console    Phone number: ${phonenumb}
    Log To Console    Address: ${address}
    
    # Create detailed data attachment for Allure
    ${user_data}=    Set Variable    User Profile Generated:\n========================\nFirst Name: ${first_name}\nLast Name: ${last_name}\nEmail: ${email}\nPhone: ${phonenumb}\nAddress: ${address}\n========================
    ${data_file}=    Set Variable    ${OUTPUT_DIR}/generated_user_data.txt
    Create File    ${data_file}    ${user_data}
    Log    Generated user data saved to: ${data_file}    INFO
    Log To Console    User data file created: ${data_file}
    
    Log Step To Console And Allure    Validating generated data format
    Should Not Be Empty    ${first_name}
    Should Not Be Empty    ${last_name}
    Should Contain    ${email}    @
    Should Not Be Empty    ${phonenumb}
    Should Not Be Empty    ${address}
    
    Log Step To Console And Allure    Fake data generation completed successfully
    



