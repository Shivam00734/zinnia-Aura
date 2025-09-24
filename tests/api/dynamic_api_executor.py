#!/usr/bin/env python3
"""
Simple Dynamic API Test Generator
Creates Robot Framework test cases only for selected APIs with console-matching Allure steps
"""

import os
import json
import sys

def create_dynamic_robot_file():
    """Create a Robot Framework file with only selected API test cases"""
    
    # Get the directory of this script
    script_dir = os.path.dirname(os.path.abspath(__file__))
    config_file = os.path.join(script_dir, "..", "api_config.json")
    
    # Load API configuration
    with open(config_file, 'r') as f:
        config = json.load(f)
    
    # Get selected APIs from environment
    selected_apis_str = os.environ.get('SELECTED_APIS', 'ALL')
    
    # Filter APIs based on selection
    oauth_explicitly_selected = False
    oauth_api = None
    
    if selected_apis_str == 'ALL' or selected_apis_str == '':
        filtered_apis = config['apis']
        oauth_explicitly_selected = True  # If ALL, OAuth is considered explicitly selected
    else:
        selected_api_names = [name.strip() for name in selected_apis_str.split(',')]
        filtered_apis = []
        oauth_explicitly_selected = 'Get OAuth Token' in selected_api_names
        
        # Find OAuth API for potential background use
        for api in config['apis']:
            if api['name'] == 'Get OAuth Token':
                oauth_api = api
                break
        
        # Add selected APIs (only the ones user actually selected)
        for api in config['apis']:
            if api['name'] in selected_api_names:
                filtered_apis.append(api)
    
    # Generate Robot Framework content
    robot_content = generate_robot_content(filtered_apis, oauth_explicitly_selected, oauth_api)
    
    # Write dynamic robot file
    dynamic_file = os.path.join(script_dir, "dynamic_api_tests.robot")
    with open(dynamic_file, 'w') as f:
        f.write(robot_content)
    
    # Calculate visible test count (only explicitly selected APIs)
    visible_test_count = len(filtered_apis)
    
    print(f"[SUCCESS] Generated dynamic test file with {visible_test_count} visible test cases")
    return dynamic_file

def generate_robot_content(apis, oauth_explicitly_selected=False, oauth_api=None):
    """Generate Robot Framework content for selected APIs"""
    
    # Determine if we need OAuth authentication in background
    needs_background_oauth = oauth_api is not None and not oauth_explicitly_selected and len(apis) > 0
    
    content = """*** Settings ***
Documentation    Dynamic API Tests - Auto-generated for selected APIs
Library    RequestsLibrary
Library    Collections
Library    OperatingSystem
Library    String
Library    BuiltIn"""

    # Add suite setup for background OAuth if needed
    if needs_background_oauth:
        content += """
Suite Setup    Background OAuth Authentication"""

    content += """

*** Variables ***
${TOKEN}    None

*** Keywords ***
Setup Session
    # Create a session without SSL verification to avoid SSL warnings
    Create Session    api_session    https://login.qa.zinnia.com    verify=False
    # For the API call (case), base URL will be https://qa.api.zinnia.io
    Create Session    api_session_case    https://qa.api.zinnia.io    verify=False
    # For BPM case management APIs
    Create Session    api_session_bpm    https://qa-bpm.se2.com    verify=False"""

    # Always add Execute Token API keyword
    content += """

Execute Token API
    [Arguments]    ${endpoint}    ${method}    ${headers}    ${payload}
    # Convert payload to form data for OAuth
    ${form_data}=    Create Dictionary
    FOR    ${key}    ${value}    IN    &{payload}
        Set To Dictionary    ${form_data}    ${key}=${value}
    END
    
    # Execute request
    ${response}=    POST On Session    api_session    ${endpoint}    data=${form_data}    headers=${headers}
    
    # Extract and store token
    ${token}=    Get From Dictionary    ${response.json()}    access_token
    Set Global Variable    ${TOKEN}    ${token}
    Set Suite Variable    ${OAUTH_TOKEN_DISPLAY}    ${token}
    
    # Log for Allure
    Log    Token received: ${token}    INFO

Execute Normal API
    [Arguments]    ${api}    ${endpoint}    ${method}    ${headers}    ${payload}    ${base_url}=None
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

    # Store response details for steps (no console output here)
    Set Suite Variable    ${API_ENDPOINT_DISPLAY}    ${endpoint}
    Set Suite Variable    ${API_SESSION_DISPLAY}    ${session_name}
    Set Suite Variable    ${API_STATUS_DISPLAY}    ${response.status_code}
    Set Suite Variable    ${API_RESPONSE_DISPLAY}    ${response.text}
    Set Suite Variable    ${BASE_URL_DISPLAY}    ${base_url}"""

    # Add background OAuth setup if needed
    if needs_background_oauth:
        content += f"""

Background OAuth Authentication
    [Documentation]    Silently authenticate with OAuth for API access
    Setup Session
    
    # OAuth Configuration (hardcoded for background auth)
    ${{endpoint}}=    Set Variable    {oauth_api['endpoint']}
    ${{method}}=      Set Variable    {oauth_api['method']}
    ${{headers}}=     Create Dictionary"""
        
        # Add headers for OAuth
        if 'headers' in oauth_api:
            for key, value in oauth_api['headers'].items():
                content += f"    {key}={value}"
        
        content += f"""
    
    # OAuth Payload
    ${{payload}}=     Create Dictionary"""
        if 'payload' in oauth_api:
            for key, value in oauth_api['payload'].items():
                if isinstance(value, str):
                    content += f"    {key}={value}"
                else:
                    content += f"    {key}={value}"
        
        content += """
    
    # Execute OAuth silently (no console output)
    Execute Token API    ${endpoint}    ${method}    ${headers}    ${payload}
    Log    Background OAuth authentication completed    INFO"""

    content += """

# Individual Allure Step Keywords that match exact console output
Step: Executing API
    [Arguments]    ${api_name}
    [Documentation]    === Executing: ${api_name} ===
    Log To Console    \\n=== Executing: ${api_name} ===
    Log    === Executing: ${api_name} ===    INFO

Step: Using Session
    [Arguments]    ${base_url}
    [Documentation]    Using session: api_session_bpm for base URL: ${base_url}
    Log To Console    Using session: api_session_bpm for base URL: ${base_url}
    Log    Using session: api_session_bpm for base URL: ${base_url}    INFO

Step: API Endpoint
    [Documentation]    API: ${API_ENDPOINT_DISPLAY}
    Log To Console    API: ${API_ENDPOINT_DISPLAY}
    Log    API: ${API_ENDPOINT_DISPLAY}    INFO

Step: Session Used
    [Documentation]    Session: ${API_SESSION_DISPLAY}
    Log To Console    Session: ${API_SESSION_DISPLAY}
    Log    Session: ${API_SESSION_DISPLAY}    INFO

Step: Status Code
    [Documentation]    Status: ${API_STATUS_DISPLAY}
    Log To Console    Status: ${API_STATUS_DISPLAY}
    Log    Status: ${API_STATUS_DISPLAY}    INFO

Step: Response Data
    [Documentation]    Response: ${API_RESPONSE_DISPLAY}
    Log To Console    Response: ${API_RESPONSE_DISPLAY}
    Log    Response: ${API_RESPONSE_DISPLAY}    INFO

Step: Completed API
    [Arguments]    ${api_name}
    [Documentation]    === Completed: ${api_name} ===
    Log To Console    === Completed: ${api_name} ===
    Log    === Completed: ${api_name} ===    INFO

Step: Token Received
    [Documentation]    Token received: ${OAUTH_TOKEN_DISPLAY}
    Log To Console    Token received: ${OAUTH_TOKEN_DISPLAY}
    Log    Token received: ${OAUTH_TOKEN_DISPLAY}    INFO

*** Test Cases ***
"""

    # Generate individual test cases for each selected API
    test_case_number = 1
    for api in apis:
        api_name = api['name']
        
        # Skip OAuth if it's not explicitly selected (it will run as suite setup instead)
        if api_name == 'Get OAuth Token' and not oauth_explicitly_selected:
            continue
            
        safe_name = api_name.replace(' ', '_').replace(',', '_')
        
        content += f"""
Test_{test_case_number:02d}_{safe_name}
    [Documentation]    Execute {api_name}
    [Setup]    Setup Session"""
        
        if api_name == 'Get OAuth Token':
            # OAuth is explicitly selected - show full console output
            content += f"""
    
    # API Configuration
    ${{endpoint}}=    Set Variable    {api['endpoint']}
    ${{method}}=      Set Variable    {api['method']}
    ${{headers}}=     Create Dictionary"""
            
            # Add headers
            if 'headers' in api:
                for key, value in api['headers'].items():
                    content += f"    {key}={value}"
            
            content += f"""
    ${{base_url}}=    Set Variable    {api.get('base_url', 'None')}
    
    # Payload (if any)"""
            
            if 'payload' in api:
                content += f"""
    ${{payload}}=     Create Dictionary"""
                for key, value in api['payload'].items():
                    if isinstance(value, str):
                        content += f"    {key}={value}"
                    else:
                        content += f"    {key}={value}"
            else:
                content += """
    ${payload}=     Set Variable    ${None}"""
            
            content += f"""
    
    # Execute OAuth with individual console-matching Allure steps
    Step: Executing API    {api_name}
    Execute Token API    ${{endpoint}}    ${{method}}    ${{headers}}    ${{payload}}
    Step: Token Received
    Step: Completed API    {api_name}
"""
        else:
            # Normal API configuration
            content += f"""
    
    # API Configuration
    ${{endpoint}}=    Set Variable    {api['endpoint']}
    ${{method}}=      Set Variable    {api['method']}
    ${{headers}}=     Create Dictionary"""
            
            # Add headers
            if 'headers' in api:
                for key, value in api['headers'].items():
                    content += f"    {key}={value}"
            
            content += f"""
    ${{base_url}}=    Set Variable    {api.get('base_url', 'None')}
    
    # Payload (if any)"""
            
            if 'payload' in api:
                content += f"""
    ${{payload}}=     Create Dictionary"""
                for key, value in api['payload'].items():
                    if isinstance(value, str):
                        content += f"    {key}={value}"
                    else:
                        content += f"    {key}={value}"
            else:
                content += """
    ${payload}=     Set Variable    ${None}"""
            
            # Create API dictionary for normal APIs
            content += f"""
    
    # Create API dictionary
    ${{api_dict}}=    Create Dictionary    name={api_name}    endpoint=${{endpoint}}    method=${{method}}    headers=${{headers}}"""
            
            if 'default_case_id' in api:
                content += f"    default_case_id={api['default_case_id']}"
            
            content += f"""
    
    # Execute API with individual console-matching Allure steps
    Step: Executing API    {api_name}
    Step: Using Session    ${{base_url}}
    Execute Normal API    ${{api_dict}}    ${{endpoint}}    ${{method}}    ${{headers}}    ${{payload}}    ${{base_url}}
    Step: API Endpoint
    Step: Session Used
    Step: Status Code
    Step: Response Data
    Step: Completed API    {api_name}
"""
        
        test_case_number += 1

    return content

if __name__ == "__main__":
    dynamic_file = create_dynamic_robot_file()
    print(f"Dynamic Robot file created: {dynamic_file}")
