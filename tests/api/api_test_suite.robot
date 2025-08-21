*** Settings ***
Resource    ../../resources/ReportingSetup.resource
Resource    ../../resources/AllureLabels.resource

Suite Setup    Run Keywords
...    Setup Allure Reporting    AND
...    Set Test Priority    ${PRIORITY_P1}    # Default priority for all tests in suite

Force Tags    @allure.label.layer:API    # This will be applied to all tests

*** Variables ***
${baseUrl}    https://dummyjson.com/
${path}       users
${expected_status_code}    200
${expected_user_name}    Emily
${expected_user_id}     0
${expected_user_phone_number}    +1 234 567 890
${expected_user_email}    emily@example.com 