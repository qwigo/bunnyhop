import requests
import json

class BaseBunny(object):

    def __init__(self, api_key):
        self.api_key = api_key
        self.endpoint_url = "https://private-anon-6e7694596b-bunnycdn.apiary-mock.com/api"

    def get_header(self):
        header = {
            'Content-Type': 'application/json',
            'accesskey': self.api_key
        }
        return header

    def call_api(self, api_url, api_method, header, api_data={}):
        r = requests.request(method=api_method, url=api_url, headers=header, params=api_data)
        return self.format_response(r)

    def format_response(self, r):
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