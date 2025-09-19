*** Settings ***
Library    OperatingSystem

*** Variables ***
${ALLURE_RESULTS_DIR}    allure-results
${ENVIRONMENT_PROPERTIES_FILE}    ${ALLURE_RESULTS_DIR}/environment.properties
${SEVERITY_FILE}    ${ALLURE_RESULTS_DIR}/severity.properties
${DESCRIPTION_FILE}    ${ALLURE_RESULTS_DIR}/description.properties

*** Keywords ***
Set Test Severity
    [Arguments]    ${severity}
    Create Directory    ${ALLURE_RESULTS_DIR}
    Create File    ${SEVERITY_FILE}    allure.test.severity=${severity}    encoding=UTF-8
    Log    ✔️ Test severity set to: ${severity}

Set Test Description
    [Arguments]    ${description}
    Create Directory    ${ALLURE_RESULTS_DIR}
    Create File    ${DESCRIPTION_FILE}    allure.test.description=${description}    encoding=UTF-8
    Log    ✔️ Test description set to: ${description}

Set Allure Report Title
    [Arguments]    ${report_title}
    Create Directory    ${ALLURE_RESULTS_DIR}
    Create File    ${ENVIRONMENT_PROPERTIES_FILE}    allure.report.name=${report_title}    encoding=UTF-8
    Log    ✔️ Allure report title set to: ${report_title}