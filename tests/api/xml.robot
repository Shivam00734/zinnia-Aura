*** Settings ***
Library      RequestsLibrary
#Library      ../../Libraries/xmlDataLib.py
Library      Collections
Library     XML
Library     OperatingSystem


*** Variables ***

${baseurl}    https://www.w3schools.com
${expectedfile}    ${CURDIR}/../../resources/xml/XML.xml



*** Test Cases ***    
Get xml data and compare
    
    Create session    mysession    ${baseurl}    
    ${response}=    GET On Session    mysession    /xml/simple.xml
   # Log To Console    ${response.content}

    ${xml_string}=    Convert To String    ${response.content}
    ${xml_obj}=    Parse XML    ${xml_string} 

    Should Be Equal     ${xml_obj}    ${expectedfile}
 
    



    


    