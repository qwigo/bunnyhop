from bunnyhop.base import BaseBunny


class Storage(BaseBunny):

    def create(self, name=None, main_storage_region=None, replica_regions=None):
        api_data = {
            'Name': name,
            'Region': main_storage_region,
            'ReplicationRegions': replica_regions,
        }
        return self.call_api(f"{self.endpoint_url}/storagezone", "POST", self.get_header(), api_data)
        

    def all(self):
        return self.call_api(f"{self.endpoint_url}/storagezone", "GET", self.get_header())

    def delete(self, id):
        return self.call_api(f"{self.endpoint_url}/storagezone/{id}", "DELETE", self.get_header())
    

    def get(self, id):
        return self.call_api(f"{self.endpoint_url}/storagezone/{id}", "GET", self.get_header())