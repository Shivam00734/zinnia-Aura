*** Settings ***
Library           Collections
Library           RequestsLibrary
Library           BuiltIn
Library           String
Library           json
Library           Process
Library           OperatingSystem

Suite Setup       Setup Session
Documentation     API Configuration Executor for handling token and case APIs

*** Variables ***
${TOKEN}          None

*** Keywords ***
Setup Session
    # Create a session without SSL verification to avoid SSL warnings
    Create Session    api_session    https://login.qa.zinnia.com    verify=False
    # For the API call (case), base URL will be https://qa.api.zinnia.io
    Create Session    api_session_case    https://qa.api.zinnia.io    verify=False
    # For BPM case management APIs
    Create Session    api_session_bpm    https://qa-bpm.se2.com    verify=False

Execute API
    [Arguments]    ${api}
    ${name}=       Get From Dictionary    ${api}    name
    ${endpoint}=   Get From Dictionary    ${api}    endpoint
    ${method}=     Get From Dictionary    ${api}    method
    ${headers}=    Get From Dictionary    ${api}    headers    default={}
    ${payload}=    Get From Dictionary    ${api}    payload    default=None
    ${base_url}=   Get From Dictionary    ${api}    base_url    default=None

    Log To Console    Executing API: ${name}
    Run Keyword If    '${name}' == 'Get OAuth Token'    Execute Token API    ${endpoint}    ${method}    ${headers}    ${payload}
    ...    ELSE    Execute Normal API    ${api}    ${endpoint}    ${method}    ${headers}    ${payload}    ${base_url}

Execute Token API
    [Arguments]    ${endpoint}    ${method}    ${headers}    ${payload}
    # Convert payload dict to form-urlencoded string
    ${form_data}=    Convert Dict To Form Data    ${payload}
    ${response}=     POST On Session     api_session    ${endpoint}    data=${form_data}    headers=${headers}
    Should Be Equal As Integers    ${response.status_code}    200    msg=Failed to get token!
    ${json}=        Set Variable    ${response.json()}
    ${token}=       Get From Dictionary    ${json}    access_token
    Set Suite Variable    ${TOKEN}    ${token}
    Log To Console    Token received: ${token}

Execute Normal API
    [Arguments]    ${api}    ${endpoint}    ${method}    ${headers}    ${payload}    ${base_url}=None
    [Documentation]    Execute API calls with automatic bearer token injection and dynamic session routing
    # Inject Bearer token if we have it
    Run Keyword If    '${TOKEN}' != 'None'
    ...    Set To Dictionary    ${headers}    Authorization=Bearer ${TOKEN}

    # Get caseID from environment, API config, or use global default
    ${default_case_id}=    Get From Dictionary    ${api}    default_case_id    default=CA0000370039
    ${caseID}=    Get Environment Variable    CASE_ID    default=${default_case_id}
    ${endpoint}=    Replace String    ${endpoint}    {caseID}    ${caseID}

    # Determine which session to use based on base_url
    ${session_name}=    Set Variable If    
    ...    '${base_url}' == 'https://qa-bpm.se2.com'    api_session_bpm
    ...    '${base_url}' == 'https://qa.api.zinnia.io'    api_session_case
    ...    api_session_case

    Log To Console    Using session: ${session_name} for base URL: ${base_url}

    # Prepare request kwargs
    ${kwargs}=    Create Dictionary    headers=${headers}
    ${payload_exists}=    Evaluate    $payload is not None
    Run Keyword If    ${payload_exists}    Set To Dictionary    ${kwargs}    json=${payload}

    # Execute request using newer RequestsLibrary syntax
    ${response}=    Run Keyword If    '${method}' == 'GET'
    ...    GET On Session    ${session_name}    ${endpoint}    &{kwargs}
    ...    ELSE IF    '${method}' == 'POST'
    ...    POST On Session    ${session_name}    ${endpoint}    &{kwargs}
    ...    ELSE IF    '${method}' == 'PUT'
    ...    PUT On Session    ${session_name}    ${endpoint}    &{kwargs}
    ...    ELSE IF    '${method}' == 'DELETE'
    ...    DELETE On Session    ${session_name}    ${endpoint}    &{kwargs}
    ...    ELSE
    ...    Fail    Unsupported method: ${method}

    # Validate response
    Should Be True    ${response.status_code} >= 200 and ${response.status_code} < 300
    ...    msg=API call failed with status ${response.status_code}: ${response.text}
    
    # Log response details
    Log To Console    \nAPI: ${endpoint}
    Log To Console    Session: ${session_name}
    Log To Console    Status: ${response.status_code}
    Log To Console    Response: ${response.text}

Convert Dict To Form Data
    [Arguments]    ${dict_payload}
    ${list}=    Create List
    FOR    ${key}    ${value}    IN    &{dict_payload}
        ${item}=    Catenate    SEPARATOR==    ${key}    ${value}
        Append To List    ${list}    ${item}
    END
    ${form_data}=    Catenate    SEPARATOR=&    @{list}
    RETURN    ${form_data}

Filter Selected APIs
    [Arguments]    ${selected_apis_str}    @{all_apis}
    [Documentation]    Filter APIs based on selection from dashboard
    
    # If no specific selection or "ALL", return all APIs
    ${use_all_apis}=    Evaluate    "${selected_apis_str}" == "ALL" or "${selected_apis_str}" == ""
    Return From Keyword If    ${use_all_apis}    @{all_apis}
    
    # Split selected API names
    ${selected_api_names}=    Split String    ${selected_apis_str}    ,
    
    # Filter APIs by selected names
    ${filtered_apis}=    Create List
    FOR    ${api}    IN    @{all_apis}
        ${api_name}=    Get From Dictionary    ${api}    name
        ${is_selected}=    Evaluate    "${api_name}" in [name.strip() for name in ${selected_api_names}]
        Run Keyword If    ${is_selected}    Append To List    ${filtered_apis}    ${api}
    END
    
    # Always include OAuth token API if any other API is selected
    ${filtered_count}=    Get Length    ${filtered_apis}
    ${needs_token}=    Evaluate    ${filtered_count} > 0
    ${has_token_api}=    Set Variable    False
    FOR    ${api}    IN    @{filtered_apis}
        ${api_name}=    Get From Dictionary    ${api}    name
        ${has_token_api}=    Set Variable If    "${api_name}" == "Get OAuth Token"    True    ${has_token_api}
    END
    
    # Add OAuth token API if needed and not already included
    Run Keyword If    ${needs_token} and not ${has_token_api}    Add OAuth Token API    ${filtered_apis}    @{all_apis}
    
    ${api_count}=    Get Length    ${filtered_apis}
    Log To Console    Total APIs to execute: ${api_count}
    RETURN    @{filtered_apis}

Add OAuth Token API
    [Arguments]    ${filtered_apis}    @{all_apis}
    [Documentation]    Add OAuth token API to filtered list if not already present
    FOR    ${api}    IN    @{all_apis}
        ${api_name}=    Get From Dictionary    ${api}    name
        Run Keyword If    "${api_name}" == "Get OAuth Token"    Insert Into List    ${filtered_apis}    0    ${api}
        Exit For Loop If    "${api_name}" == "Get OAuth Token"
    END

Run All Configured APIs
    [Arguments]    @{apis}
    FOR    ${api}    IN    @{apis}
        Execute API    ${api}
    END

Load And Filter API Configuration
    [Documentation]    Load config file and filter APIs based on dashboard selection
    ${config_file}=    Set Variable    ${CURDIR}${/}..${/}api_config.json
    
    # Verify config file exists
    File Should Exist    ${config_file}    msg=API config file not found: ${config_file}
    
    # Load and validate config
    ${file_content}=    Get File    ${config_file}
    ${config}=    Evaluate    json.loads('''${file_content}''')    json
    Dictionary Should Contain Key    ${config}    apis    msg=Config file must contain 'apis' key
    Set Global Variable    ${GLOBAL_CONFIG}    ${config}
    
    # Get selected APIs from environment variable (set by dashboard)
    ${selected_apis_str}=    Get Environment Variable    SELECTED_APIS    default=ALL
    
    # Filter APIs based on selection
    ${filtered_apis}=    Filter Selected APIs    ${selected_apis_str}    @{config}[apis]
    Set Global Variable    @{FILTERED_APIS}    @{filtered_apis}
    
    ${api_count}=    Get Length    ${filtered_apis}
    Log To Console    \n🚀 Loaded ${api_count} selected APIs for execution


Execute Single API
    [Arguments]    ${api}
    [Documentation]    Execute a single API with proper session setup
    ${name}=       Get From Dictionary    ${api}    name
    ${endpoint}=   Get From Dictionary    ${api}    endpoint
    ${method}=     Get From Dictionary    ${api}    method
    ${headers}=    Get From Dictionary    ${api}    headers    default={}
    ${payload}=    Get From Dictionary    ${api}    payload    default=None
    ${base_url}=   Get From Dictionary    ${api}    base_url    default=None

    Run Keyword If    '${name}' == 'Get OAuth Token'    Execute Token API    ${endpoint}    ${method}    ${headers}    ${payload}
    ...    ELSE    Execute Normal API    ${api}    ${endpoint}    ${method}    ${headers}    ${payload}    ${base_url}

Check API Selection And Load Config
    [Arguments]    ${api_name}
    [Documentation]    Load configuration and check if API is selected, exit test if not selected
    
    # Load configuration only once (check if already loaded)
    ${config_loaded}=    Evaluate    len($FILTERED_APIS) > 0
    Run Keyword If    not ${config_loaded}    Load And Filter API Configuration
    
    # Check if this specific API is selected
    ${api_selected}=    Is API Selected    ${api_name}
    Pass Execution If    not ${api_selected}    API '${api_name}' not selected for execution

Is API Selected
    [Arguments]    ${api_name}
    [Documentation]    Check if API is in the filtered list
    FOR    ${api}    IN    @{FILTERED_APIS}
        ${filtered_api_name}=    Get From Dictionary    ${api}    name
        Return From Keyword If    '${filtered_api_name}' == '${api_name}'    ${True}
    END
    Return From Keyword    ${False}

Get API If Selected
    [Arguments]    ${api_name}
    [Documentation]    Get API configuration if it's selected, return None if not selected
    FOR    ${api}    IN    @{FILTERED_APIS}
        ${filtered_api_name}=    Get From Dictionary    ${api}    name
        Return From Keyword If    '${filtered_api_name}' == '${api_name}'    ${api}
    END
    Return From Keyword    None

Execute API Test
    [Arguments]    ${api}
    [Documentation]    Execute API test with proper logging
    ${api_name}=    Get From Dictionary    ${api}    name
    Log To Console    \n=== Executing: ${api_name} ===
    Execute Single API    ${api}
    Log To Console    === Completed: ${api_name} ===

*** Variables ***
${GLOBAL_CONFIG}       ${EMPTY}
@{FILTERED_APIS}       

*** Test Cases ***
Execute Get OAuth Token API
    [Documentation]    Execute OAuth Token API for authentication
    [Setup]    Check API Selection And Load Config    Get OAuth Token
    ${api}=    Get API If Selected    Get OAuth Token
    Run Keyword If    $api is not None    Execute API Test    ${api}

Execute Get Case Details API
    [Documentation]    Execute Get Case Details API
    [Setup]    Check API Selection And Load Config    Get Case Details
    ${api}=    Get API If Selected    Get Case Details
    Run Keyword If    $api is not None    Execute API Test    ${api}

Execute Search Cases by Policy Number API
    [Documentation]    Execute Search Cases by Policy Number API
    [Setup]    Check API Selection And Load Config    Search Cases by Policy Number
    ${api}=    Get API If Selected    Search Cases by Policy Number
    Run Keyword If    $api is not None    Execute API Test    ${api}

Execute Search Cases by Agent Name API
    [Documentation]    Execute Search Cases by Agent Name API
    [Setup]    Check API Selection And Load Config    Search Cases by Agent Name
    ${api}=    Get API If Selected    Search Cases by Agent Name
    Run Keyword If    $api is not None    Execute API Test    ${api}

Execute Get Task Assignee Summary API
    [Documentation]    Execute Get Task Assignee Summary API
    [Setup]    Check API Selection And Load Config    Get Task Assignee Summary
    ${api}=    Get API If Selected    Get Task Assignee Summary
    Run Keyword If    $api is not None    Execute API Test    ${api}
