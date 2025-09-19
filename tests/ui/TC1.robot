*** Settings ***
Library    SeleniumLibrary


*** Test Cases ***
Launching Web brower
    Open Browser    https://demo.nopcommerce.com/    Chrome
    Maximize Browser Window
    Click Link    xpath://a[@class="ico-login"]
    Input text  id:Email    sksharma@gmail.com
    Input Text  id:Password    Test@123
    click button    xpath://*[text()='Log in']
    Sleep    10s

