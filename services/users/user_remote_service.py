import requests
from decouple import config

from schemas.user import UserIn


class UserRemoteService:
    def __init__(self):
        self.user_service_base_url = config("user_service_base_url")
        self.user_service_api_key = config("user_service_api_key")

    def base_request(self, url, method, data=None, params=None):
        requested_url = self.user_service_base_url + "v1/" + url
        headers = {
            "x-api-key": self.user_service_api_key
        }
        if method == "GET":
            resp = requests.get(requested_url, headers=headers, params=params, timeout=5)

        elif method == "POST":
            resp = requests.post(requested_url, json=data, headers=headers, params=params, timeout=5)

        elif method == "DELETE":
            resp = requests.delete(requested_url, headers=headers, params=params)
            return resp

        return resp.json(), resp.status_code

    def fetch_all_users(self):
        url = "users/"
        method = "GET"
        return self.base_request(url, method)

    def fetch_single_user(self, user_id):
        url = f"users/{user_id}"
        method = "GET"
        return self.base_request(url, method)

    def create_user(self, data: UserIn):
        url = f"users/create"
        method = "POST"
        data = {
            "username": data.username
        }
        return self.base_request(url, method, data)

    def delete_user(self, user_id):
        url = f"users/delete/{user_id}"
        method = "DELETE"
        return self.base_request(url, method)
