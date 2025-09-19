*** Settings ***
Library    SeleniumLibrary


*** Variables ***
${Browser}    Chrome
${url}      https://admin-demo.nopcommerce.com/login?ReturnUrl=%2Fadmin%2F


*** Keywords ***

Open my Browser
    Open Browser    ${url}    ${Browser}
    Maximize Browser Window


Close my Browser
    Close All Browsers

Input username
    [Arguments]    ${username}
    Input Text    id:Email    ${username}

Input password
    [Arguments]    ${password}
    Input Text    id:Password    ${password}

Click login button
    Click Button    xpath://*[@class="button-1 login-button"]

click logout link
    click link     Logout

Error message should be visible
    page should contain    Login was unsuccessful

Dashboard page should be visible
    page should contain    Dashboard