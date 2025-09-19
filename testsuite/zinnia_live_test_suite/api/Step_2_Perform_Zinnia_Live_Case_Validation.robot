*** Settings ***
Library    SeleniumLibrary
Library    BuiltIn
Resource   resources/zinnialive.resource
#Library    DataDriver    file=C:\\Users\\nidhonk\\OneDrive - Zinnia\\New folder\\ZL_Automation\\data\\test_data\\zinnia_live_test_data4.xlsx      sheet_name=output_data
#Library    DataDriver    file=C:\\Users\\nidhonk\\Documents\\ZL_Project\\QAS-ZinniaLive-AutomationTesting\\data\\test_data\\zinnia_live_test_data5.xlsx      sheet_name=output_data

Library    DataDriver    file=../../../data/test_data/zinnia_live_test_data5.xlsx      sheet_name=output_data
Suite Setup    Validate EApp, Create Attachment, And Upload To Incoming Folder


*** Test Cases ***
Perform Zinnia Live Case Validation For Client: ${client_code}, TestID: ${test_case_id}
    [Documentation]    Validates Zinnia Live case for the given test data
    [Template]    Validate Case Overview Status, Stage Status, Steps Status, LifeCad Policy Code Status, NIGO Exception IDs, and Kafka Event ID
    # DataDriver will replace this with actual test data from Excel
    default_test_case_id    default_client_code    default_automation_flow    default_company_hierarchy


*** Keywords ***
Validate Case Overview Status, Stage Status, Steps Status, LifeCad Policy Code Status, NIGO Exception IDs, and Kafka Event ID
    [Arguments]    ${test_case_id}    ${client_code}    ${automation_flow_category}    ${company_hierarchy_id}  
    Validate All Zinnia Live Case Statuses, LifeCad Policy Code Status, NIGO Exception IDs, And Kafka Event ID    ${test_case_id}    ${client_code}    ${automation_flow_category}    ${company_hierarchy_id}





