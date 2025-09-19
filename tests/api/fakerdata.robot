*** Settings ***

Library    FakerLibrary    seed=234
Library    allure_robotframework
Library    Collections
Library    RequestsLibrary


*** Test Cases ***
Creating Fake Data
    [Tags]    Test Type: Smoke 
    ${first_name}=    FakerLibrary.first_name
    ${last_name}=  FakerLibrary.last_name
    ${email}=    FakerLibrary.email
    ${phonenumb}=     FakerLibrary.Phone Number
    ${address}=      FakerLibrary.address

    
    log to console    Name: ${first_name}
    log to console    Last name: ${last_name}
    log to console    email id : ${email}
    log to console    phone number: ${phonenumb}
    log to console    address: ${address}
    



