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

Execute API
    [Arguments]    ${api}
    ${name}=       Get From Dictionary    ${api}    name
    ${endpoint}=   Get From Dictionary    ${api}    endpoint
    ${method}=     Get From Dictionary    ${api}    method
    ${headers}=    Get From Dictionary    ${api}    headers    default={}
    ${payload}=    Get From Dictionary    ${api}    payload    default=None

    Log To Console    Executing API: ${name}
    Run Keyword If    '${name}' == 'Get OAuth Token'    Execute Token API    ${endpoint}    ${method}    ${headers}    ${payload}
    ...    ELSE    Execute Normal API    ${endpoint}    ${method}    ${headers}    ${payload}

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
    [Arguments]    ${endpoint}    ${method}    ${headers}    ${payload}
    # Inject Bearer token if we have it
    Run Keyword If    '${TOKEN}' != 'None'
    ...    Set To Dictionary    ${headers}    Authorization=Bearer ${TOKEN}

    # Get caseID from environment or use default
    ${caseID}=    Get Environment Variable    CASE_ID    default=12345
    ${endpoint}=    Replace String    ${endpoint}    {caseID}    ${caseID}

    # Prepare request kwargs
    ${kwargs}=    Create Dictionary    headers=${headers}
    Run Keyword If    '${payload}' != 'None'    Set To Dictionary    ${kwargs}    json=${payload}

    # Execute request using newer RequestsLibrary syntax
    ${response}=    Run Keyword If    '${method}' == 'GET'
    ...    GET On Session    api_session_case    ${endpoint}    &{kwargs}
    ...    ELSE IF    '${method}' == 'POST'
    ...    POST On Session    api_session_case    ${endpoint}    &{kwargs}
    ...    ELSE IF    '${method}' == 'PUT'
    ...    PUT On Session    api_session_case    ${endpoint}    &{kwargs}
    ...    ELSE IF    '${method}' == 'DELETE'
    ...    DELETE On Session    api_session_case    ${endpoint}    &{kwargs}
    ...    ELSE
    ...    Fail    Unsupported method: ${method}

    # Validate response
    Should Be True    ${response.status_code} >= 200 and ${response.status_code} < 300
    ...    msg=API call failed with status ${response.status_code}: ${response.text}
    
    # Log response details
    Log To Console    \nAPI: ${endpoint}
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

Run All Configured APIs
    [Arguments]    @{apis}
    FOR    ${api}    IN    @{apis}
        Execute API    ${api}
    END

*** Test Cases ***
Run Token And Case API
    [Documentation]    Execute configured APIs from the config file
    ${config_file}=    Set Variable    ${CURDIR}${/}..${/}api_config.json
    
    # Verify config file exists
    File Should Exist    ${config_file}    msg=API config file not found: ${config_file}
    
    # Load and validate config
    ${file_content}=    Get File    ${config_file}
    ${config}=    Evaluate    json.loads('''${file_content}''')    json
    Dictionary Should Contain Key    ${config}    apis    msg=Config file must contain 'apis' key
    
    # Execute APIs
    Run All Configured APIs    @{config}[apis]
