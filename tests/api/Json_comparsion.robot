*** Settings ***
Library    Collections
Library    RequestsLibrary
Library    OperatingSystem
Library    BuiltIn
Library    JSONLibrary


*** Variables ***
#${BASE_URL}    https://dummyjson.com/
${BASE_URL}    https://dev.api.zinnia.io
${EXPECTED_FILE}    ${CURDIR}/../../resources/json/jsondata.json


*** Test Cases ***
Comparison between data
    
    [Documentation]    Compare API response with local JSON data.
    Create Session    mysession    ${BASE_URL}
   # ${response}=    GET On Session   mysession    /carts
    ${response}=    GET On Session   mysession    /case/v1/cases/12398305
    Log To Console   Status code: ${response.status_code}
    
 
 #   log to console    ${response.content}
    log to console    Headers: ${response.headers}

 #validations

    log to console    checking status code
    ${ststuscode}=    Convert To String    ${response.status_code}
    should be equal     ${ststuscode}    200



    log to console    checking status code
   # ${response_body}=    Set Variable   ${response.content}
  #  Log To Console    ${response_body}

  
#Read the json file (jsonformatter.txt)

    #Get data from json file
    Log    Reading expected data from JSON file
    ${json_file}=    Get File     ${EXPECTED_FILE}
    ${json_data}=    Evaluate    json.loads('''${json_file}''')   
  #  ${title}=    Set Variable    json_data['carts'][0]['products'][0]['title']  
    ${title}=    Set Variable    ${json_data}[carts][0][products][0][title]
    Log To Console     ${title}

    
  #Get the API response as a Python object

    
    # Get the API response as a Python object
    ${response_body}=    Evaluate    json.loads('''${response.content}''')    

    # Get the data from the local JSON file
    ${json_file}=    Get File     ${EXPECTED_FILE}
    ${json_data}=    Evaluate    json.loads('''${json_file}''')  

    # Compare the two Python objects (deep comparison)
 
    
    Should Be Equal       ${response_body}         ${json_data}
    Log To Console         The JSON objects are correctly different.
    
    
    



   
    
    
    