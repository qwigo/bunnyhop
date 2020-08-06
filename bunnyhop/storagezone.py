from bunnyhop.base import BaseBunny


class StorageZone(BaseBunny):
    
    def get(self, id):
        api_url = self.endpoint_url + '/storagezone/' + id
        header = self.get_header()
        response = self._CallApi(api_url, "GET", header)
        return response.text