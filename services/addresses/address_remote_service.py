import requests
from decouple import config
from circuitbreaker import circuit
from requests.exceptions import RequestException
from schemas.address import AddressIn


class AddressRemoteService:

    def __init__(self):
        self.address_service_base_url = config("address_service_base_url")
        self.address_service_api_key = config("address_service_api_key")

    def base_request(self, url, method, data=None, params=None):
        requested_url = "http://" + self.address_service_base_url + "v1/" + url
        headers = {
            "x-api-key": self.address_service_api_key
        }
        if method == "GET":
            resp = requests.get(requested_url, headers=headers, params=params)

        elif method == "POST":
            resp = requests.post(requested_url, json=data, headers=headers, params=params)

        elif method == "DELETE":
            resp = requests.delete(requested_url, headers=headers, params=params)
            return resp

        return resp.json(), resp.status_code

    @circuit(failure_threshold=5, recovery_timeout=120, expected_exception=RequestException)
    def fetch_all_address(self):
        url = "addresses/"
        method = "GET"
        return self.base_request(url, method)

    @circuit(failure_threshold=5, recovery_timeout=120, expected_exception=RequestException)
    def fetch_user_addresses(self, user_id):
        url = f"addresses/{user_id}/"
        method = "GET"
        return self.base_request(url, method)

    @circuit(failure_threshold=5, recovery_timeout=120, expected_exception=RequestException)
    def create_address(self, address_input: AddressIn):
        url = f"addresses/create"
        method = "POST"
        data = {
            "userId": address_input.userId,
            "city": address_input.city,
            "country": address_input.country
        }
        return self.base_request(url, method, data=data)

    @circuit(failure_threshold=5, recovery_timeout=120, expected_exception=RequestException)
    def delete_address(self, user_id):
        url = f"addresses/delete/{user_id}/"
        method = "DELETE"
        return self.base_request(url, method)
