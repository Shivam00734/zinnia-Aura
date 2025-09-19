*** Settings ***
Library    SeleniumLibrary    
Library    FakerLibrary
Library    BuiltIn




*** Variables ***
${url}    https://demo.nopcommerce.com/
${browser}    Chrome




*** Test Cases ***
Register the new customer
    
    ${first_name}=    FakerLibrary.first_name
    ${Last_name}=    FakerLibrary.last_name
    ${email}=    FakerLibrary.email

    open Browser    ${url}    ${browser}
    Maximize Browser Window
    Set selenium speed    1seconds

    click Link    xpath://a[@class="ico-register"]

    Select Radio Button    Gender    M
    Select Radio Button    Gender    F
    Input Text    id:FirstName    ${first_name}
    Input Text    id:LastName    ${Last_name}
    Input Text    id:Email    ${email}
    Input Text    id:Password    Test@123
    Input text   id:ConfirmPassword    Test@123
    click Button      id:register-button

Verify the registration is successfull    
    Page Should Contain    Your registration completed
    sleep    30s
