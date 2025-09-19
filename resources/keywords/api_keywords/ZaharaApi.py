import requests
from robot.api.deco import library, keyword
from robot.libraries.BuiltIn import BuiltIn
import json

from resources.utilities.FileUtils import FileUtils


@library
class ZaharaApi:
    file = FileUtils()

    @keyword
    def call_lifecycle_api(self, policy_number, lifecycle_date, client_plan_code):
        url = f"https://qa-zahara-api.zinnia.io/v1/lifecycle/{client_plan_code}/{policy_number}/{lifecycle_date}T23%3A00%3A00.000Z"

        headers = {
            "accept": "application/json, text/plain, */*",
            "origin": "https://qa-zahara-ui.zinnia.io",
            "priority": "u=1, i",
            "referer": "https://qa-zahara-ui.zinnia.io/"
        }

        response = requests.post(url, headers=headers)

        try:
            response_data = response.json()
            BuiltIn().log(f"Lifecycle executed successfully: {json.dumps(response_data)}")
            BuiltIn().log_to_console(f"Lifecycle executed successfully: {json.dumps(response_data)}")
            return response_data
        except ValueError:
            BuiltIn().log(f"Lifecycle execution failed", {response.text})
            BuiltIn().log_to_console(f"Lifecycle execution failed", {response.text})
            return {"error": "Invalid JSON response"}


    @keyword
    def initiate_transaction_on_zahara(self, policy_number, effective_date, plan_code):
        corr_id = self.file.generate_random_uuid()
        url = f"https://qa-zahara-api.zinnia.io/v1/policies/{plan_code}/{policy_number}/initialpremium"

        headers = {
            'accept': 'application/json, text/plain, */*',
            'content-type': 'application/json',
            'origin': 'https://qa-zahara-ui.zinnia.io',
            'referer': 'https://qa-zahara-ui.zinnia.io/'
        }

        payload = {
            "correlationId": f"{corr_id}",
            "effectiveDate": f"{effective_date}",
            "reverseInitiator": False,
            "transactionAmounts": {
                "requestedAmount": "109999.47"
            },
            "fundAllocation": {
                "allocationOption": "DEFAULT"
            },
            "payor": {
                "partyId": "Party_Owner_1",
                "paymentForm": "CHECK",
                "bankId": "1"
            },
            "exchange": None,
            "taxBasis": None
        }

        response = requests.post(url, headers=headers, data=json.dumps(payload))

        if response.status_code == 200:
            BuiltIn().log(f"Transaction initiated successfully on Zahara")
            BuiltIn().log_to_console(f"Transaction initiated successfully on Zahara")
        else:
            raise AssertionError('Transaction initiation failed on Zahara')


    @keyword
    def get_access_token(self):
        url = "https://login.qa.zinnia.com/oauth/token"

        headers = {
            "Content-Type": "application/json"
        }

        payload = {
            "audience": "https://qa.api.zinnia.io",
            "grant_type": "client_credentials",
            "client_id": "UuMribrP3e8zVhfHy6wPJ25lVYh1CWN3",
            "client_secret": "WQ4ZBFI0RaYnhlhrZBdw4ltrMk8IKT9bDm1DX_U28doSk4F4Au5KiAsoBCSNYWix"
        }

        response = requests.post(url, headers=headers, json=payload)

        if response.status_code == 200:
            data = response.json()
            return data.get("access_token")
        else:
            raise Exception(f"Failed to fetch token. Status: {response.status_code}, Response: {response.text}")

    @keyword
    def update_party_phones(self, plan_code, policy_number, token):
        corr_id = self.file.generate_random_uuid()
        current_date = self.file.get_cst_date("%Y-%m-%d")
        url = f"https://qa.api.zinnia.io/policy/v1/transactions/{plan_code}/{policy_number}/parties/Party_PI_1/phones"

        headers = {
            "Content-Type": "application/json",
            "Authorization": f'Bearer {token}'
        }

        payload = {
            "correlationId": f"{corr_id}",
            "effectiveDate": f"{current_date}",
            "phones": [
                {
                    "startDate": f"{current_date}",
                    "phoneType": "MOBILE",
                    "countryCode": "+1",
                    "areaCode": "415",
                    "dialNumber": "5551234",
                    "bestTime": "Evening",
                    "timeZone": "PST",
                    "preferredPhoneIndicator": False
                },
                {
                    "startDate": f"{current_date}",
                    "endDate": None,
                    "phoneType": "HOME",
                    "countryCode": "+1",
                    "areaCode": "212",
                    "dialNumber": "5559876",
                    "bestTime": "Morning",
                    "timeZone": "EST",
                    "preferredPhoneIndicator": True
                }
            ]
        }

        response = requests.put(url, headers=headers, json=payload)

        if response.status_code == 202:
            BuiltIn().log("Phone change API call successful")
            BuiltIn().log_to_console("Phone change API call successful")
            result =  response.json() if response.content else None
            BuiltIn().log(f"API Response: {result}")
            BuiltIn().log_to_console(f"API Response: {result}")
            return result

        else:
            raise Exception(f"API call failed. Status: {response.status_code}, Response: {response.text}")

    @keyword
    def update_party_emails(self, plan_code, policy_number, token):
        corr_id = self.file.generate_random_uuid()
        current_date = self.file.get_cst_date("%Y-%m-%d")
        url = f"https://qa.api.zinnia.io/bpm/v1/policies/{plan_code}/{policy_number}/parties/Party_PI_1/emailaddresses"

        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {token}"
        }

        payload = {
            "correlationId": f"{corr_id}",
            "effectiveDate": f"{current_date}",
            "emails": [
                {
                    "startDate": f"{current_date}",
                    "emailType": "PERSONAL",
                    "emailAddress": "first.email@example.com",
                    "preferredEmailIndicator": False
                },
                {
                    "startDate": f"{current_date}",
                    "emailType": "BUSINESS",
                    "emailAddress": "second.email@workplace.com",
                    "preferredEmailIndicator": True
                },
                {
                    "startDate": f"{current_date}",
                    "emailType": "PERSONAL",
                    "emailAddress": "third.email@somewhere.net",
                    "preferredEmailIndicator": False
                }
            ]
        }

        response = requests.put(url, headers=headers, json=payload)

        if response.status_code == 202:
            BuiltIn().log("Email change API call successful")
            BuiltIn().log_to_console("Email change API call successful")
            result = response.json() if response.content else None
            BuiltIn().log(f"API Response: {result}")
            BuiltIn().log_to_console(f"API Response: {result}")
            return result
        else:
            raise Exception(f"API call failed. Status: {response.status_code}, Response: {response.text}")



#
# obj = ZaharaApi()
# token = obj.get_access_token()
# plan = "TL0101"
# policy = "FTL2560530187777"
# obj.update_party_emails(plan, policy, token)