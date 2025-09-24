*** Settings ***
Documentation    Docker Selenium Grid Configuration for Automation Framework
Library          SeleniumLibrary
Library          OperatingSystem

*** Variables ***
# Docker Selenium Grid Configuration
${SELENIUM_HUB_URL}    http://selenium-hub:4444/wd/hub
${LOCAL_HUB_URL}       http://localhost:4444/wd/hub
${DEFAULT_BROWSER}     chrome
${DEFAULT_TIMEOUT}     30s
${IMPLICIT_WAIT}       10s
${PAGE_LOAD_TIMEOUT}   30s

# Browser capabilities for different browsers
&{CHROME_OPTIONS}      add_argument=--no-sandbox
...                    add_argument=--disable-dev-shm-usage
...                    add_argument=--disable-gpu
...                    add_argument=--window-size=1920,1080

&{FIREFOX_OPTIONS}     add_argument=--width=1920
...                    add_argument=--height=1080

&{EDGE_OPTIONS}        add_argument=--no-sandbox
...                    add_argument=--disable-dev-shm-usage
...                    add_argument=--window-size=1920,1080

*** Keywords ***
Open Browser In Docker Grid
    [Documentation]    Opens browser using Docker Selenium Grid
    [Arguments]    ${url}    ${browser}=${DEFAULT_BROWSER}    ${grid_url}=${EMPTY}
    
    # Determine if running in Docker or locally
    ${is_docker}=    Is Running In Docker
    ${hub_url}=      Set Variable If    ${is_docker}    ${SELENIUM_HUB_URL}    ${LOCAL_HUB_URL}
    ${hub_url}=      Set Variable If    '${grid_url}' != '${EMPTY}'    ${grid_url}    ${hub_url}
    
    Log    Opening browser: ${browser} at Grid URL: ${hub_url}
    
    # Set browser-specific options
    ${options}=    Get Browser Options    ${browser}
    
    # Open browser with Grid configuration
    Open Browser    ${url}    ${browser}    
    ...    remote_url=${hub_url}
    ...    options=${options}
    
    # Set timeouts
    Set Selenium Timeout         ${DEFAULT_TIMEOUT}
    Set Selenium Implicit Wait    ${IMPLICIT_WAIT}
    Set Selenium Page Load Timeout    ${PAGE_LOAD_TIMEOUT}
    
    # Maximize window
    Maximize Browser Window

Get Browser Options
    [Documentation]    Returns browser-specific options
    [Arguments]    ${browser}
    
    ${browser_lower}=    Convert To Lower Case    ${browser}
    
    ${options}=    Run Keyword If    '${browser_lower}' == 'chrome'      Set Variable    ${CHROME_OPTIONS}
    ...    ELSE IF                   '${browser_lower}' == 'firefox'     Set Variable    ${FIREFOX_OPTIONS}  
    ...    ELSE IF                   '${browser_lower}' == 'edge'        Set Variable    ${EDGE_OPTIONS}
    ...    ELSE                      Set Variable                        ${CHROME_OPTIONS}
    
    RETURN    ${options}

Is Running In Docker
    [Documentation]    Detects if tests are running inside Docker container
    
    # Check for Docker environment indicators
    ${docker_env}=        Get Environment Variable    SELENIUM_HUB_URL    ${EMPTY}
    ${is_container}=      Run Keyword And Return Status    
    ...                   Should Not Be Empty    ${docker_env}
    
    # Additional check for container environment
    ${proc_result}=       Run Keyword And Return Status    
    ...                   File Should Exist    /.dockerenv
    
    ${is_docker}=         Evaluate    ${is_container} or ${proc_result}
    
    Log    Running in Docker: ${is_docker}
    RETURN    ${is_docker}

Open Browser Cross Platform
    [Documentation]    Opens browser that works both locally and in Docker
    [Arguments]    ${url}    ${browser}=${DEFAULT_BROWSER}
    
    # Try Docker Grid first, fallback to local
    ${status}=    Run Keyword And Return Status    
    ...           Open Browser In Docker Grid    ${url}    ${browser}
    
    Run Keyword If    not ${status}
    ...    Open Browser    ${url}    ${browser}

Wait For Selenium Grid
    [Documentation]    Waits for Selenium Grid to be ready
    [Arguments]    ${timeout}=60s    ${grid_url}=${LOCAL_HUB_URL}
    
    Log    Waiting for Selenium Grid at: ${grid_url}
    
    FOR    ${i}    IN RANGE    30
        ${status}=    Run Keyword And Return Status    
        ...           Evaluate    requests.get('${grid_url}/status').status_code == 200    
        ...           modules=requests
        
        Exit For Loop If    ${status}
        Sleep    2s
    END
    
    Should Be True    ${status}    Selenium Grid is not ready at ${grid_url}
    Log    Selenium Grid is ready!

Close All Browsers And Cleanup
    [Documentation]    Cleanup keyword for Docker and local environments
    
    # Close all browser sessions
    Close All Browsers
    
    # Additional cleanup for Docker environment
    ${is_docker}=    Is Running In Docker
    Run Keyword If    ${is_docker}    Log    Docker cleanup completed

*** Test Cases ***
# Example test case showing Docker integration
Docker Grid Verification Test
    [Documentation]    Verifies Docker Selenium Grid functionality
    [Tags]    docker    verification    smoke
    
    Wait For Selenium Grid
    Open Browser In Docker Grid    https://www.google.com
    Title Should Be    Google
    Close All Browsers And Cleanup

