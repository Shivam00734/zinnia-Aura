*** Settings ***
Library    OperatingSystem
Library    BuiltIn
Library    DateTime
Library    Collections


*** Variables ***
${ALLURE_RESULTS_DIR}=    allure-results
${ALLURE_REPORT_DIR}=    allure-results
${HISTORY_DIR}=    ${ALLURE_RESULTS_DIR}/history
${TARGET_HISTORY_DIR}=    ${ALLURE_RESULTS_DIR}/history


*** Keywords ***
Setup Allure Reporting
    Log To Console    Setting up Allure Reporting...
    
    # # Check if allure-report exists and has history
    # ${report_exists}=    Run Keyword And Return Status    Directory Should Exist    allure-report/history
    # Run Keyword If    ${report_exists}    Run Keywords
    # ...    Create Directory    ${ALLURE_RESULTS_DIR}/history    AND
    # ...    Copy File    allure-report/history/history-trend.json    ${ALLURE_RESULTS_DIR}/history/history-trend.json    AND
    # ...    Copy File    allure-report/history/duration-trend.json    ${ALLURE_RESULTS_DIR}/history/duration-trend.json    AND
    # ...    Copy File    allure-report/history/retry-trend.json    ${ALLURE_RESULTS_DIR}/history/retry-trend.json    AND
    # ...    Copy File    allure-report/history/categories-trend.json    ${ALLURE_RESULTS_DIR}/history/categories-trend.json    AND
    # ...    Copy File    allure-report/history/history.json    ${ALLURE_RESULTS_DIR}/history/history.json    AND
    # ...    Log To Console    Copied history from previous report

    # # Now backup current results history if it exists
    # ${history_exists}=    Run Keyword And Return Status    Directory Should Exist    ${ALLURE_RESULTS_DIR}/history
    # Run Keyword If    ${history_exists}    Run Keywords
    # ...    Create Directory    history_backup    AND
    # ...    Run Keyword And Ignore Error    Copy File    ${ALLURE_RESULTS_DIR}/history/history-trend.json    history_backup/history-trend.json    AND
    # ...    Run Keyword And Ignore Error    Copy File    ${ALLURE_RESULTS_DIR}/history/duration-trend.json    history_backup/duration-trend.json    AND
    # ...    Run Keyword And Ignore Error    Copy File    ${ALLURE_RESULTS_DIR}/history/retry-trend.json    history_backup/retry-trend.json    AND
    # ...    Run Keyword And Ignore Error    Copy File    ${ALLURE_RESULTS_DIR}/history/categories-trend.json    history_backup/categories-trend.json    AND
    # ...    Run Keyword And Ignore Error    Copy File    ${ALLURE_RESULTS_DIR}/history/history.json    history_backup/history.json

    # # Clean and create results directory
    # Remove Directory    ${ALLURE_RESULTS_DIR}    recursive=True
    # Create Directory    ${ALLURE_RESULTS_DIR}
    # Create Directory    ${ALLURE_RESULTS_DIR}/history

    # # Restore history from backup if it exists
    # ${backup_exists}=    Run Keyword And Return Status    Directory Should Exist    history_backup
    # Run Keyword If    ${backup_exists}    Run Keywords
    # ...    Run Keyword And Ignore Error    Copy File    history_backup/history-trend.json    ${ALLURE_RESULTS_DIR}/history/history-trend.json    AND
    # ...    Run Keyword And Ignore Error    Copy File    history_backup/duration-trend.json    ${ALLURE_RESULTS_DIR}/history/duration-trend.json    AND
    # ...    Run Keyword And Ignore Error    Copy File    history_backup/retry-trend.json    ${ALLURE_RESULTS_DIR}/history/retry-trend.json    AND
    # ...    Run Keyword And Ignore Error    Copy File    history_backup/categories-trend.json    ${ALLURE_RESULTS_DIR}/history/categories-trend.json    AND
    # ...    Run Keyword And Ignore Error    Copy File    history_backup/history.json    ${ALLURE_RESULTS_DIR}/history/history.json    AND
    # ...    Remove Directory    history_backup    recursive=True    AND
    # ...    Log To Console    Restored history from backup


    ${current_date}=    Get Current Date    result_format=%Y-%m-%d
    ${current_time}=    Get Current Date    result_format=%H:%M:%S
    
    Create Environment Properties
    Create Executor JSON
    Create Categories JSON
    Log To Console    Allure setup complete.


Create Environment Properties
    ${current_date}=    Get Current Date    result_format=%Y-%m-%d
    &{env}=    Create Dictionary
    ...    Project=Allure Demo Project
    ...    Environment=Test
    ...    Date=${current_date}
    ...    ExecutedBy= Shivam Sharma

    Create File    ${ALLURE_RESULTS_DIR}/environment.properties    ${EMPTY}
    FOR    ${key}    IN    @{env}
        ${line}=    Set Variable    ${key}=${env}[${key}]\n
        Append To File    ${ALLURE_RESULTS_DIR}/environment.properties    ${line}    encoding=UTF-8
    END


Create Executor JSON
    ${current_date}=    Get Current Date    result_format=%Y-%m-%d
    ${current_time}=    Get Current Date    result_format=%H:%M:%S
    ${json}=    Catenate
    ...    {
    ...      "name": "Shivam Sharma",
    ...      "type": "jenkins",
    ...      "reportName": "My Report",
    ...      "startTime": "${current_date}T${current_time}"
    ...    }
    Create File    ${ALLURE_RESULTS_DIR}/executor.json    ${json}


Create Categories JSON
    ${categories}=    Catenate
    ...    [
    ...      {
    ...        "name": "Failed Tests",
    ...        "matchedStatuses": ["failed"]
    ...      },
    ...      {
    ...        "name": "Broken Tests",
    ...        "matchedStatuses": ["broken"]
    ...      },
    ...      {
    ...        "name": "Skipped Tests",
    ...        "matchedStatuses": ["skipped"]
    ...      },
    ...      {
    ...        "name": "Passed Tests",
    ...        "matchedStatuses": ["passed"]
    ...      }
    ...    ]


    Create File    ${ALLURE_RESULTS_DIR}/categories.json    ${categories}    encoding=UTF-8