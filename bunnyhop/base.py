import requests

from envs import env
from valley.contrib import Schema
# Imports for other modules
from valley.properties import FloatProperty, CharProperty, ListProperty, IntegerProperty, EmailProperty, \
    DateTimeProperty, BooleanProperty, SlugProperty


class BaseBunny(Schema):
    endpoint_url = env('BUNNYCDN_API_ENDPOINT', 'https://bunnycdn.com/api')

    def __init__(self,
                 api_key,
                 endpoint_url=None,
                 **kwargs
                 ):
        self.api_key = api_key
        if endpoint_url:
            self.endpoint_url = endpoint_url
        super().__init__(**kwargs)

    def get_header(self):
        header = {
            'Content-Type': 'application/json',
            'Accept': 'application/json',
            'accesskey': self.api_key
        }
        return header

    def call_api(self, api_url, api_method, header, params={}, data={}):
        r = requests.request(method=api_method, url=api_url, headers=header, params=params, data=data)
        return r.json()

