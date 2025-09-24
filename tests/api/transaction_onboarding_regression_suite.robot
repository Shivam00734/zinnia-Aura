*** Settings ***
Library    OperatingSystem
Library    Collections
Test Setup    Add Project Root To Python Path
Library    SeleniumLibrary

Library    BuiltIn
Library    ../../resources/utilities/ExcelUtilities.py    WITH NAME    ExcelUtils
Suite Setup    Filter Test Date By Execution Flag
Library    DataDriver    file=\\\\sbgcommon\\SYS\\DEPTS\\SE2\\Delivery Quality\\Automation DQ\\ZLCM\\Data\\Testdata\\transaction_onboarding.xlsx    sheet_name=output
Resource   ../../resources/Reporting/ReportingSetup.resource
Resource    ../../resources/zinnialive.resource


# Ensure browser always closes after each test case (even on failure)
Test Teardown    Close Browser
Suite Teardown    Close All Browsers

*** Test Cases ***
Perform ${automation_flow} Process for client ${client_name} testID: ${TestId}
    [Template]    Perform Transaction Onboarding Automation Flow
    # DataDriver will replace this with actual test data from Excel
    default_testid    default_flow    default_client    default_plan    default_xml    default_contract    default_payee    default_status    default_loan    default_repay    default_autopay    default_manage    default_premium    default_withdraw    default_rmd    default_freq1    default_freq2    default_mode    default_fund    default_account1    default_account2    default_fix    default_cap    default_participation    default_transfer    default_systematic    default_communication


*** Keywords ***
Add Project Root To Python Path
    ${project_root}=    Normalize Path    ${CURDIR}/../../
    Evaluate    sys.path.insert(0, r'${project_root}')    sys

Perform Transaction Onboarding Automation Flow
    [Arguments]    ${TestId}    ${automation_flow}    ${client_name}    ${client_plan_code}    ${old_xml_file_name}    ${manage_autopay_contract_number}    ${payee_name}    ${expected_policy_status}    ${start_loan_amount}    ${loan_repayment_amount}    ${loan_autopay_amount}    ${loan_manage_autopay_amount}    ${systematic_premium_update_amount}    ${systematic_withdrawal_update_amount}    ${systematic_rmd_update_amount}    ${Payment_frequency}    ${Manage_payment_frequency}    ${payment_mode}    ${fund_allocation_type}    ${expected_account_name}    ${expected_account_number}    ${fix_fund_allocation_percent}    ${cap_account_allocation_percent}    ${participation_rate_allocation_percent}    ${transfer_amount}    ${systematic_withdrawal_and_rmd_amount}    ${preferred_communication}
    Transaction Onboarding Automation Process    ${automation_flow}    ${old_xml_file_name}    ${manage_autopay_contract_number}    ${payee_name}    ${expected_policy_status}    ${start_loan_amount}    ${loan_autopay_amount}    ${Payment_frequency}    ${loan_repayment_amount}    ${payment_mode}    ${fund_allocation_type}    ${expected_account_name}    ${expected_account_number}    ${loan_manage_autopay_amount}    ${Manage_payment_frequency}    ${fix_fund_allocation_percent}    ${cap_account_allocation_percent}    ${participation_rate_allocation_percent}    ${client_name}    ${client_plan_code}    ${transfer_amount}    ${systematic_withdrawal_and_rmd_amount}    ${systematic_premium_update_amount}    ${systematic_withdrawal_update_amount}    ${systematic_rmd_update_amount}    ${preferred_communication}


Transaction Onboarding Automation Process
    [Arguments]    ${automation_flow}    ${old_xml_file_name}    ${manage_autopay_contract_number}    ${payee_name}    ${expected_policy_status}    ${start_loan_amount}    ${loan_autopay_amount}    ${Payment_frequency}    ${loan_repayment_amount}    ${payment_mode}    ${fund_allocation_type}    ${expected_account_name}    ${expected_account_number}    ${loan_manage_autopay_amount}    ${Manage_payment_frequency}    ${fix_fund_allocation_percent}    ${cap_account_allocation_percent}    ${participation_rate_allocation_percent}    ${client_name}    ${client_plan_code}    ${transfer_amount}    ${systematic_withdrawal_and_rmd_amount}    ${systematic_premium_update_amount}    ${systematic_withdrawal_update_amount}    ${systematic_rmd_update_amount}    ${preferred_communication}
    Transaction Onboarding Automation Flow Until Lifecycle Completion    ${automation_flow}    ${old_xml_file_name}    ${manage_autopay_contract_number}    ${payee_name}    ${expected_policy_status}    ${start_loan_amount}    ${loan_autopay_amount}    ${Payment_frequency}    ${loan_repayment_amount}    ${payment_mode}    ${fund_allocation_type}    ${expected_account_name}    ${expected_account_number}    ${loan_manage_autopay_amount}    ${Manage_payment_frequency}    ${fix_fund_allocation_percent}    ${cap_account_allocation_percent}    ${participation_rate_allocation_percent}    ${client_name}    ${client_plan_code}    ${transfer_amount}    ${systematic_withdrawal_and_rmd_amount}    ${systematic_premium_update_amount}    ${systematic_withdrawal_update_amount}    ${systematic_rmd_update_amount}    ${preferred_communication}



#Transaction Process Flow:
#Step 1: Policy create on zahara and lifeCycle run
#Step 2: Process to complete the transaction flow on Zinnia Live Platform


# *** Settings ***
# Library    OperatingSystem
# Library    Collections
# Test Setup    Add Project Root To Python Path
# Library    SeleniumLibrary
# Resource    ../../../resources/zinnialive.resource
# Library    BuiltIn
# Library    ../../../resources/utilities/ExcelUtilities.py    WITH NAME    ExcelUtils
# Suite Setup    Filter Test Date By Execution Flag
# Library    DataDriver    file=\\\\sbgcommon\\SYS\\DEPTS\\SE2\\Delivery Quality\\Automation DQ\\ZLCM\\Data\\Testdata\\transaction_onboarding.xlsx    sheet_name=output



# *** Test Cases ***
# Perform ${automation_flow} Process for client ${client_name} testID: ${TestId}
#     [Template]    Perform Transaction Onboarding Automation Flow
#     # DataDriver will replace this with actual test data from Excel
#     default_testid    default_flow    default_client    default_plan    default_xml    default_contract    default_payee    default_status    default_loan    default_repay    default_autopay    default_manage    default_premium    default_withdraw    default_rmd    default_freq1    default_freq2    default_mode    default_fund    default_account1    default_account2    default_fix    default_cap    default_participation    default_transfer    default_systematic    default_communication


# *** Keywords ***
# Add Project Root To Python Path
#     ${project_root}=    Normalize Path    ${CURDIR}/../../../
#     Evaluate    sys.path.insert(0, r'${project_root}')    sys

# Perform Transaction Onboarding Automation Flow
#     [Arguments]    ${TestId}    ${automation_flow}    ${client_name}    ${client_plan_code}    ${old_xml_file_name}    ${manage_autopay_contract_number}    ${payee_name}    ${expected_policy_status}    ${start_loan_amount}    ${loan_repayment_amount}    ${loan_autopay_amount}    ${loan_manage_autopay_amount}    ${systematic_premium_update_amount}    ${systematic_withdrawal_update_amount}    ${systematic_rmd_update_amount}    ${Payment_frequency}    ${Manage_payment_frequency}    ${payment_mode}    ${fund_allocation_type}    ${expected_account_name}    ${expected_account_number}    ${fix_fund_allocation_percent}    ${cap_account_allocation_percent}    ${participation_rate_allocation_percent}    ${transfer_amount}    ${systematic_withdrawal_and_rmd_amount}    ${preferred_communication}
#     Transaction Onboarding Automation Process    ${automation_flow}    ${old_xml_file_name}    ${manage_autopay_contract_number}    ${payee_name}    ${expected_policy_status}    ${start_loan_amount}    ${loan_autopay_amount}    ${Payment_frequency}    ${loan_repayment_amount}    ${payment_mode}    ${fund_allocation_type}    ${expected_account_name}    ${expected_account_number}    ${loan_manage_autopay_amount}    ${Manage_payment_frequency}    ${fix_fund_allocation_percent}    ${cap_account_allocation_percent}    ${participation_rate_allocation_percent}    ${client_name}    ${client_plan_code}    ${transfer_amount}    ${systematic_withdrawal_and_rmd_amount}    ${systematic_premium_update_amount}    ${systematic_withdrawal_update_amount}    ${systematic_rmd_update_amount}    ${preferred_communication}



# #Transaction Process Flow:
# #Step 1: Policy create on zahara and lifeCycle run
# #Step 2: Process to complete the transaction flow on Zinnia Live Platform



