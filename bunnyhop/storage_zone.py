from bunnyhop.base import BaseBunny
from .url_settings import *
import json
import os

class StorageZone(BaseBunny):
    
    def get(self, id):
        response = self.call_api(f"{self.endpoint_url}/storagezone/{id}", "GET", self.get_header(), format=False)
        response_json = json.loads(response.text)
        return StorageObject(response_json['Name'])
    

class StorageObject(BaseBunny):
    
    def __init__(self, zone_name):
        self.zone_name = zone_name
        self.endpoint_url = bunnycdn_storage_url
    
    def all(self, path):
        header = {
            'Accept': 'application/json',
        }
        return self.call_api(f"{self.endpoint_url}/{self.zone_name}/{path}", "GET", header)
    
    def get(self, path, file_name):
        return self.call_api(f"{self.endpoint_url}/{self.zone_name}/{path}/{file_name}", "GET", {})
    
    def delete(self, path, file_name):
        return self.call_api(f"{self.endpoint_url}/{self.zone_name}/{path}/{file_name}", "DELETE", {})
    
    def upload_file(self, dest_path, local_path):
        header = {
            'Checksum': None,
        }
        return self.call_api(f"{self.endpoint_url}/{self.zone_name}/{dest_path}/{local_path}", "PUT", header)

    def create_file(self, file_name, content):
        f = open(file_name, 'w+')
        f.write(content)
        f.close()
        return f"file name: {file_name}, path: {os.path.dirname(os.path.abspath(file_name))}"
    
    def create_json(self, file_name, content):
        with open(file_name, 'w+') as f:
            json.dump(content, f)
        return f"file name: {file_name}, path: {os.path.dirname(os.path.abspath(file_name))}"
        