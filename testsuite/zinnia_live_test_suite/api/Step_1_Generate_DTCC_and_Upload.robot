*** Settings ***
Library    SeleniumLibrary
Resource    resources/zinnialive.resource

*** Variables ***
${group_id}    one

*** Test Cases ***
Generate DTCC File Upload To NSCC Folder And Prepare Test Data
    Generate DTCC File, Upload To NSCC Folder, And Prepare Test Data    ${group_id}


    

