import json
import os

from envs import env

from bunnyhop import base


class Storage(base.BaseBunny):

    def create(self, name, main_storage_region=None, replica_regions=None):
        api_data = {
            'Name': name
        }
        if main_storage_region:
            api_data['Region'] = main_storage_region
        if replica_regions:
            api_data['ReplicationRegions'] = replica_regions

        return self.call_api(f"{self.endpoint_url}/storagezone", "POST", self.get_header(), data=api_data)

    def all(self):
        return [StorageZone(self.api_key, **i) for i in self.call_api(f"{self.endpoint_url}/storagezone", "GET", self.get_header())]

    def delete(self, id):
        return self.call_api(f"{self.endpoint_url}/storagezone/{id}", "DELETE", self.get_header())

    def get(self, id):
        return self.call_api(f"{self.endpoint_url}/storagezone/{id}", "GET", self.get_header())


class StorageZone(base.BaseBunny):
    Id = base.IntegerProperty()
    UserId = base.CharProperty()
    Name = base.CharProperty()
    Password = base.CharProperty()
    DateModified = base.DateTimeProperty()
    Deleted = base.BooleanProperty()
    StorageUsed = base.IntegerProperty()
    FilesStored = base.IntegerProperty()
    Region = base.CharProperty()
    ReplicationRegions = base.ListProperty()
    PullZones = base.ListProperty()
    ReadOnlyPassword = base.CharProperty()

    def __str__(self):
        return self.Name

    def delete(self):
        return self.call_api(f"{self.endpoint_url}/storagezone/{self.Id}", "DELETE", self.get_header())


class StorageObject(base.BaseBunny):
    endpoint_url = env('BUNNYCDN_STORAGE_API_ENDPOINT', 'https://storage.bunnycdn.com')

    def __init__(self,
                 api_key,
                 zone_name,
                 endpoint_url=None,
                 **kwargs
                 ):
        self.zone_name = zone_name
        super().__init__(api_key, endpoint_url=endpoint_url, **kwargs)

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
