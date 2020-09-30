from json import JSONDecodeError

import requests

from envs import env
from valley.contrib import Schema
# Imports for other modules
from valley.properties import FloatProperty, CharProperty, ListProperty, IntegerProperty, EmailProperty, \
    DateTimeProperty, BooleanProperty, SlugProperty, DictProperty


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

    def __repr__(self):
        return '<{class_name}: {uni} >'.format(
            class_name=self.__class__.__name__, uni=self.__str__())

    def get_header(self):
        header = {
            'Content-Type': 'application/json',
            'Accept': 'application/json',
            'accesskey': self.api_key
        }
        return header

    def get_url(self, api_url, endpoint_url):
        if endpoint_url:
            url = f"{endpoint_url}{api_url}"
        else:
            url = f"{self.endpoint_url}{api_url}"
        return url

    def call_api(self, api_url, api_method, header=None, params={}, data={}, json_data={}, endpoint_url=None):
        if not header:
            header = self.get_header()
        r = requests.request(
                method=api_method, url=self.get_url(api_url, endpoint_url), headers=header, params=params, data=data,
                json=json_data)
        try:
            return r.json()
        except JSONDecodeError:
            return r.content


class BaseStorageBunny(BaseBunny):
    storage_endpoint_url = env('BUNNYCDN_STORAGE_API_ENDPOINT', 'storage.bunnycdn.com')

    def get_storage_header(self):
        return {
            'Content-Type': 'application/json',
            'Accept': 'application/json',
            'AccessKey': self.api_key
        }

    def get_storage_endpoint(self, region):
        return f"https://{region}.{self.storage_endpoint_url}"

    def get_region(self):
        return self.Region.lower()

    def call_storage_api(self, api_url, api_method, header=None, params={}, data={}, json_data={}, files=None,
                         endpoint_url=None):
        if not header:
            header = self.get_storage_header()
        if not endpoint_url:
            endpoint_url = self.get_storage_endpoint(self.get_region())
        if files:
            return requests.put(self.get_url(api_url, endpoint_url), headers=header, files=files)
        return self.call_api(api_url, api_method, header=header, params={}, data=data, json_data=json_data,
                             endpoint_url=endpoint_url)
