*** Settings ***
Library    keywords/core_logic_keywords/ZinniaLiveValidation.py
Library    keywords/data_creation_keywords/GenerateDTCC.py
Library    keywords/helper_keywords/EappHelper.py
Library    keywords/ui_keywords/ZinniaLive.py
Library    keywords/ui_keywords/Zahara.py


*** Keywords ***
Generate DTCC File, Upload to NSCC Folder, and Prepare Test Data
    [Arguments]    ${group_id}
    Generate DTCC File And Upload DTCC    ${group_id}


Validate eApp, Create Attachment, and Upload to Incoming Folder
    [Arguments]    ${eapp_id}
    Validate eApp    ${eapp_id}
    Create Attachment For eApp    ${eapp_id}
    Upload Attachment To Incoming Folder    ${eapp_id}

Validate All zinnia Live Case Statuses, LifeCad Policy Code Status, NIGO Exception IDs, and Kafka Event ID
    [Arguments]    ${test_case_id}    ${client_code}    ${automation_flow_category}    ${company_hierarchy_id}
    Validate Zinnia Live Case Flow    ${test_case_id}    ${client_code}    ${automation_flow_category}    ${company_hierarchy_id}

Transaction Onboarding Automation Process
    [Arguments]    ${automation_flow}    ${old_xml_file_name}    ${manage_autopay_contract_number}    ${payee_name}    ${expected_policy_status}    ${start_loan_amount}    ${loan_autopay_amount}    ${Payment_frequency}    ${loan_repayment_amount}    ${payment_mode}    ${fund_allocation_type}    ${expected_account_name}    ${expected_account_number}    ${loan_manage_autopay_amount}    ${Manage_payment_frequency}    ${fix_fund_allocation_percent}    ${cap_account_allocation_percent}    ${participation_rate_allocation_percent}    ${client_name}    ${client_plan_code}    ${transfer_amount}    ${systematic_withdrawal_and_rmd_amount}    ${systematic_premium_update_amount}    ${systematic_withdrawal_update_amount}    ${systematic_rmd_update_amount}    ${preferred_communication}
    Transaction Onboarding Automation Flow    ${automation_flow}    ${old_xml_file_name}    ${manage_autopay_contract_number}    ${payee_name}    ${expected_policy_status}    ${start_loan_amount}    ${loan_autopay_amount}    ${Payment_frequency}    ${loan_repayment_amount}    ${payment_mode}    ${fund_allocation_type}    ${expected_account_name}    ${expected_account_number}    ${loan_manage_autopay_amount}    ${Manage_payment_frequency}    ${fix_fund_allocation_percent}    ${cap_account_allocation_percent}    ${participation_rate_allocation_percent}    ${client_name}    ${client_plan_code}    ${transfer_amount}    ${systematic_withdrawal_and_rmd_amount}    ${systematic_premium_update_amount}    ${systematic_withdrawal_update_amount}    ${systematic_rmd_update_amount}    ${preferred_communication}


