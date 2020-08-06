from bunnyhop.base import BaseBunny
import json

class StorageZone(BaseBunny):
    
    def get(self, id):
        response = self.call_api(f"{self.endpoint_url}/storagezone/{id}", "GET", self.get_header(), format=False)
        response_json = json.loads(response.text)
        return StorageObject(response_json['Name'])
    

class StorageObject(BaseBunny):
    
    def __init__(self, zone_name):
        self.zone_name = zone_name
        self.endpoint_url = "https://private-anon-3bc35a36a9-bunnycdnstorage.apiary-mock.com/"
    
    def get_header(self):
        header = {
            'Content-Type': 'application/json',
        }
        return header
    
    def all(self, path):
        return self.call_api(f"{self.endpoint_url}/{self.zone_name}/{path}", "GET", self.get_header())
    
    def get(self):
        pass
    
    def download(self):
        pass
    
    def delete(self):
        pass
    
    def upload_file(self):
        pass

    def create_json(self):
        pass