*** Settings ***
Library    ../../resources/json/TestDataLib.py
Library    OperatingSystem



*** Variables ***

${BASE_URL}    https://dummyjson.com/
${EXPECTED_FILE}    ${CURDIR}/../../resources/json/jsondata.json


*** Test Cases ***
Read Test Data from json file
    ${data}=    Load Json Data    ${EXPECTED_FILE}
 #   ${user}=    Get User By Index    ${data}    1
    Log To Console    Name: ${data}[carts][0][products][0][title]
    