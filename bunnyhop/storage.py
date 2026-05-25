import json
import os
from io import BytesIO

from envs import env

from bunnyhop import base


class StorageZoneStats(base.BaseBunny):
    TotalStorageUsed = base.IntegerProperty()
    TotalFilesStored = base.IntegerProperty()
    StorageUsedChart = base.DictProperty()
    FilesStoredChart = base.DictProperty()
    StorageUsedBySizeChart = base.DictProperty()

    def __str__(self):
        return f"StorageUsed: {self.TotalStorageUsed} | FilesStored: {self.TotalFilesStored}"


class Storage(base.BaseBunny):

    def create(self, name, main_storage_region: str = None, replica_regions: list = None):
        api_data = {
            'Name': name,
            'Region': main_storage_region,
            'ReplicationRegions': replica_regions
        }

        response = self.call_api(f"/storagezone", "POST", json_data=api_data)
        if response.get('Id', None):
            return StorageZone(response.get('Password'), **response)
        else:
            raise ValueError(f"Storage zone creation failed [{response.get('ErrorKey')}]: {response.get('Message', '')}")

    def update(self, id, **kwargs):
        return self.call_api(f"/storagezone/{id}", "POST", json_data=kwargs)

    def all(self):
        return [StorageZone(i.get('Password'), **i) for i in
                self.call_api(f"/storagezone", "GET")]

    def delete(self, id):
        return self.call_api(f"/storagezone/{id}", "DELETE")

    def get(self, id):
        response = self.call_api(f"/storagezone/{id}", "GET")
        if response.get('Id', None):
            return StorageZone(response.get('Password'), **response)
        return response

    def get_stats(self, id, date_from=None, date_to=None):
        params = {'dateFrom': date_from, 'dateTo': date_to}
        return StorageZoneStats(
            self.api_key,
            **self.call_api(f"/storagezone/{id}/statistics", "GET", params=params)
        )


class StorageZone(base.BaseStorageBunny):
    Id = base.IntegerProperty()
    UserId = base.CharProperty()
    Name = base.CharProperty()
    Password = base.CharProperty()
    DateModified = base.DateTimeProperty(required=False)
    Deleted = base.BooleanProperty(default_value=False)
    StorageUsed = base.IntegerProperty(required=False)
    FilesStored = base.IntegerProperty(required=False)
    Region = base.CharProperty()
    ReplicationRegions = base.ListProperty()
    PullZones = base.ListProperty()
    ReadOnlyPassword = base.CharProperty(required=False)

    def __str__(self):
        return self.Name

    def all(self, folder=''):
        if not folder.endswith('/'):
            folder = f"{folder}/"
        return [StorageObject(self.api_key, self, **i) for i in self.call_storage_api(f"/{self.Name}/{folder}", "GET")]

    def get(self, file_path):
        response = self.call_storage_api(f"/{self.Name}/{file_path}", "GET")
        if isinstance(response,dict) and response.get('HttpCode',0) == 404:
            raise Exception(f"Error:{response.get('Message','')}")
        return response

    def get_object(self, file_path):
        items = self.call_storage_api(f"/{self.Name}/", "GET")
        if not isinstance(items, list):
            raise FileNotFoundError(f"Could not list storage zone '{self.Name}'")
        matches = [StorageObject(self.api_key, self, **i) for i in items if file_path == i.get('ObjectName', '')]
        if not matches:
            raise FileNotFoundError(f"'{file_path}' not found in storage zone '{self.Name}'")
        return matches[0]

    def head_file(self, file_path):
        return self.call_storage_api(f"/{self.Name}/{file_path}", "HEAD")

    def upload_file(self, dest_path, file_name, local_path):
        with open(local_path, 'rb') as f:
            data = f.read()
        return self.call_storage_api(f"/{self.Name}/{dest_path}/{file_name}", "PUT", data=data)

    def create_file(self, file_name, content):
        if isinstance(content, str):
            content = content.encode('utf-8')
        return self.call_storage_api(f"/{self.Name}/{file_name}", "PUT", data=content)

    def create_json(self, key, data_dict):
        f = BytesIO(json.dumps(data_dict).encode())
        return self.call_storage_api(f"/{self.Name}/{key}", "PUT",
                                     data=f.read())

    def delete(self):
        return self.call_api(f"/storagezone/{self.Id}", "DELETE")

    def get_stats(self, date_from=None, date_to=None):
        params = {'dateFrom': date_from, 'dateTo': date_to}
        return StorageZoneStats(
            self.api_key,
            **self.call_api(f"/storagezone/{self.Id}/statistics", "GET", params=params)
        )

    def delete_file(self, file_path):
        response = self.call_storage_api(f"/{self.Name}/{file_path}", "DELETE")
        if isinstance(response, dict) and response.get('HttpCode', 0) == 404:
            raise FileNotFoundError(f"Error: {response.get('Message', '')}")
        return response



class StorageObject(base.BaseStorageBunny):
    endpoint_url = env('BUNNYCDN_STORAGE_API_ENDPOINT', 'https://storage.bunnycdn.com')

    Guid = base.SlugProperty(required=True)
    StorageZoneName = base.CharProperty(required=True)
    Path = base.CharProperty(required=True)
    ObjectName = base.CharProperty(required=True)
    Length = base.IntegerProperty()
    LastChanged = base.DateTimeProperty()
    ServerId = base.IntegerProperty()
    IsDirectory = base.BooleanProperty()
    UserId = base.SlugProperty(required=True)
    ContentType = base.CharProperty()
    DateCreated = base.DateTimeProperty()
    StorageZoneId = base.IntegerProperty(required=True)
    Checksum = base.CharProperty()
    ReplicatedZones = base.ListProperty()

    def __init__(self,
                 api_key,
                 storage_zone,
                 endpoint_url=None,
                 **kwargs
                 ):
        self.storage_zone = storage_zone
        super().__init__(api_key, endpoint_url=endpoint_url, **kwargs)

    def __str__(self):
        return f"{self.Path}{self.ObjectName}"

    def get_region(self):
        return self.storage_zone.Region.lower()

    def delete(self):
        return self.call_storage_api(f"/{self.storage_zone.Name}/{self.Path}/{self.ObjectName}", "DELETE")


