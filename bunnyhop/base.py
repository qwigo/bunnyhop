import requests
import json

class BaseBunny(object):

    def __init__(self, api_key):
        self.api_key = api_key
        self._URL = "https://bunnycdn.com/api"

    def get_header(self):
        header = {
            'Content-Type': 'application/json',
            'accesskey': self.api_key
        }
        return header

    def _CallApi(self, api_url, api_method, header, api_data={}):
        if api_method == "GET":
            r = requests.get(api_url, headers=header, params=api_data)
        elif api_method == "POST":
            r = requests.post(api_url, headers=header, json=api_data)
        elif api_method == "DELETE":
            r = requests.delete(api_url, headers=header, params=api_data)
        return r

    def _FormatResponse(self, r):
        if r.status_code == 201:
            response = {
                "status": "successfully created",
                "status_code": r.status_code,
                "result": None,
            }
            return json.dumps(response)
            
        elif r.status_code != 200:
            response = {
                "status": "error",
                "status_code": r.status_code,
                "result": None,
            }
            return json.dumps(response)
        else:
            response = {
                "status": "success",
                "status_code": r.status_code,
                "result": r.text,
            }
            return json.dumps(response)