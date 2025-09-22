*** Settings ***
Library    OperatingSystem
Library    String
Library    DateTime
Library    Collections
Library    Process

*** Variables ***
${CONSOLE_LOG_FILE}    ${OUTPUT_DIR}/console_output.log
${ALLURE_RESULTS_DIR}    ${OUTPUT_DIR}/allure-results

*** Keywords ***
Setup Allure Reporting
    [Documentation]    Enhanced Allure reporting setup with console integration
    Log To Console    Setting up enhanced Allure reporting with console integration
    
    # Create console log file
    ${output_dir}=    Set Variable    ${OUTPUT_DIR}
    Create Directory    ${output_dir}
    Create File    ${CONSOLE_LOG_FILE}
    
    # Set up Allure environment info
    ${current_time}=    Get Current Date    result_format=%Y-%m-%d %H:%M:%S
    
    # Log environment information
    Log    Test execution started at: ${current_time}

Setup Test With Console Logging
    [Documentation]    Setup individual test with enhanced console logging
    [Arguments]    ${test_name}=${TEST_NAME}
    
    ${current_time}=    Get Current Date    result_format=%Y-%m-%d %H:%M:%S
    Log To Console    Starting test: ${test_name}
    Append To Console Log    ========================================
    Append To Console Log    Test: ${test_name}
    Append To Console Log    Started: ${current_time}
    Append To Console Log    ========================================
    
    # Add test metadata to Allure using built-in keywords
    Log    Enhanced test with console logging integration
    
Teardown Test With Console Logging
    [Documentation]    Teardown test and attach console logs to Allure
    
    ${current_time}=    Get Current Date    result_format=%Y-%m-%d %H:%M:%S
    Append To Console Log    Test completed at: ${current_time}
    Append To Console Log    ========================================
    
    # Attach console log to Allure report
    Attach Console Log To Allure
    
    Log To Console    Test completed with console logs attached to Allure

Log Step To Console And Allure
    [Documentation]    Log a step to both console and Allure report
    [Arguments]    ${step_description}    ${details}=${EMPTY}
    
    Log To Console    STEP: ${step_description}
    Append To Console Log    STEP: ${step_description}
    
    Run Keyword If    "${details}" != "${EMPTY}"    
    ...    Append To Console Log    DETAILS: ${details}
    
    # Log step information for Allure integration
    Log    STEP: ${step_description}    INFO
    Run Keyword If    "${details}" != "${EMPTY}"    
    ...    Log    STEP DETAILS: ${details}    INFO

Log Process To Console And Allure
    [Documentation]    Log a process/operation to both console and Allure
    [Arguments]    ${process_name}    ${process_details}=${EMPTY}
    
    ${timestamp}=    Get Current Date    result_format=%H:%M:%S
    Log To Console    [${timestamp}] PROCESS: ${process_name}
    Append To Console Log    [${timestamp}] PROCESS: ${process_name}
    
    Run Keyword If    "${process_details}" != "${EMPTY}"    
    ...    Append To Console Log    PROCESS DETAILS: ${process_details}
    
    # Log process information for Allure integration
    Log    PROCESS: ${process_name}    INFO
    Run Keyword If    "${process_details}" != "${EMPTY}"    
    ...    Log    PROCESS DETAILS: ${process_details}    INFO

Log Failure To Console And Allure
    [Documentation]    Log failure details to both console and Allure
    [Arguments]    ${failure_message}    ${error_details}=${EMPTY}
    
    ${timestamp}=    Get Current Date    result_format=%H:%M:%S
    Log To Console    [${timestamp}] FAILURE: ${failure_message}
    Append To Console Log    [${timestamp}] FAILURE: ${failure_message}
    
    Run Keyword If    "${error_details}" != "${EMPTY}"    
    ...    Append To Console Log    ERROR DETAILS: ${error_details}
    
    # Log failure information for Allure integration
    Log    FAILURE: ${failure_message}    WARN
    Run Keyword If    "${error_details}" != "${EMPTY}"    
    ...    Log    ERROR DETAILS: ${error_details}    ERROR

Append To Console Log
    [Documentation]    Append message to console log file
    [Arguments]    ${message}
    
    ${timestamp}=    Get Current Date    result_format=%Y-%m-%d %H:%M:%S
    ${log_entry}=    Set Variable    [${timestamp}] ${message}
    Append To File    ${CONSOLE_LOG_FILE}    ${log_entry}\n

Attach Console Log To Allure
    [Documentation]    Attach the console log file to Allure report
    
    ${log_exists}=    Run Keyword And Return Status    File Should Exist    ${CONSOLE_LOG_FILE}
    Run Keyword If    ${log_exists}    
    ...    Log    Console log file available: ${CONSOLE_LOG_FILE}
    Run Keyword If    ${log_exists}    
    ...    Log To Console    Console log attached: ${CONSOLE_LOG_FILE}

Capture Command Output To Allure
    [Documentation]    Run command, capture output, and attach to Allure
    [Arguments]    ${command}    ${attachment_name}=Command Output
    
    Log To Console    Executing command: ${command}
    Append To Console Log    COMMAND: ${command}
    
    ${result}=    Run Process    ${command}    shell=True
    
    Log To Console    Command exit code: ${result.rc}
    Append To Console Log    EXIT CODE: ${result.rc}
    
    Run Keyword If    "${result.stdout}" != "${EMPTY}"    
    ...    Append To Console Log    STDOUT: ${result.stdout}
    
    Run Keyword If    "${result.stderr}" != "${EMPTY}"    
    ...    Append To Console Log    STDERR: ${result.stderr}
    
    # Create temporary file with command output
    ${sanitized_name}=    Replace String    ${attachment_name}    ${SPACE}    _
    ${sanitized_name}=    Convert To Lower Case    ${sanitized_name}
    ${output_file}=    Set Variable    ${OUTPUT_DIR}/command_output_${sanitized_name}.txt
    Create File    ${output_file}    Command: ${command}\nExit Code: ${result.rc}\n\nSTDOUT:\n${result.stdout}\n\nSTDERR:\n${result.stderr}
    
    # Log attachment information for Allure integration
    Log    Command output saved to: ${output_file}    INFO
    Log To Console    Attachment created: ${attachment_name} at ${output_file}
    
    RETURN    ${result}

# Setup Enhanced Allure Environment
#     [Documentation]    Setup enhanced Allure environment with detailed system info
#     [Arguments]    ${environment}=QA    ${test_type}=API
    
#     # System information
#     ${os_info}=    Evaluate    platform.system() + " " + platform.release()    platform
#     ${python_version}=    Evaluate    sys.version.split()[0]    sys
#     ${hostname}=    Evaluate    socket.gethostname()    socket


Setup Enhanced Allure Environment
    [Documentation]    Setup enhanced Allure environment with detailed system info (hard-coded values)

    # 🔒 Hard-coded environment info
    ${environment}=    Set Variable    QA
    ${test_type}=      Set Variable    API

    # System information (dynamic but machine-dependent)
    ${os_info}=    Evaluate    platform.system() + " " + platform.release()    platform
    ${python_version}=    Evaluate    sys.version.split()[0]    sys
    ${hostname}=    Evaluate    socket.gethostname()    socket



    # Log environment information for Allure integration
    Log    Environment: ${environment}    INFO
    Log    Test Type: ${test_type}    INFO
    Log    Operating System: ${os_info}    INFO
    Log    Python Version: ${python_version}    INFO
    Log    Hostname: ${hostname}    INFO
    Log    Console Logging: Enabled    INFO
    
    # Create environment properties file for Allure
    ${allure_results_dir}=    Set Variable    ${OUTPUT_DIR}/allure-results
    Create Directory    ${allure_results_dir}
    ${env_file}=    Set Variable    ${allure_results_dir}/environment.properties
    ${env_content}=    Catenate    SEPARATOR=\n
    ...    Environment=${environment}
    ...    Test_Type=${test_type}
    ...    Operating_System=${os_info}
    ...    Python_Version=${python_version}
    ...    Hostname=${hostname}
    ...    Console_Logging=Enabled
    Create File    ${env_file}    ${env_content}
    
    Log To Console    Allure environment setup completed
    Log To Console    Environment: ${environment} | Type: ${test_type}
    Log To Console    OS: ${os_info} | Python: ${python_version}

Create Test Execution Summary
    [Documentation]    Create a comprehensive test execution summary for Allure
    [Arguments]    ${total_tests}=1    ${passed_tests}=0    ${failed_tests}=0
    
    ${execution_time}=    Get Current Date    result_format=%Y-%m-%d %H:%M:%S
    ${summary}=    Set Variable    Test Execution Summary\n========================\nExecution Time: ${execution_time}\nTotal Tests: ${total_tests}\nPassed: ${passed_tests}\nFailed: ${failed_tests}\n
    
    # Create summary file
    ${summary_file}=    Set Variable    ${OUTPUT_DIR}/test_execution_summary.txt
    Create File    ${summary_file}    ${summary}
    
    # Log summary information for Allure integration
    Log    Test execution summary saved to: ${summary_file}    INFO
    Log To Console    Test execution summary created: ${summary_file}
    
    Log To Console    Test execution summary created and attached to Allure

Create Allure Attachment
    [Documentation]    Create a file attachment that Allure can process
    [Arguments]    ${file_path}    ${attachment_name}    ${content}
    
    # Create the attachment file
    Create File    ${file_path}    ${content}
    
    # Log the attachment with specific format that allure_robotframework listener can process
    Log    📎 ATTACHMENT: ${attachment_name} | Path: ${file_path}    INFO
    Log To Console    📎 Attachment created: ${attachment_name} -> ${file_path}


