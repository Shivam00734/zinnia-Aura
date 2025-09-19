*** Variables ***
${PRIORITY_P0}    @allure.label.priority:P0
${PRIORITY_P1}    @allure.label.priority:P1
${PRIORITY_P2}    @allure.label.priority:P2
${PRIORITY_P3}    @allure.label.priority:P3

*** Keywords ***
Set Test Priority
    [Arguments]    ${priority}
    Set Tags    ${priority}

Mark As Critical Priority
    Set Test Priority    ${PRIORITY_P0}

Mark As High Priority
    Set Test Priority    ${PRIORITY_P1}

Mark As Medium Priority
    Set Test Priority    ${PRIORITY_P2}

Mark As Low Priority
    Set Test Priority    ${PRIORITY_P3} 