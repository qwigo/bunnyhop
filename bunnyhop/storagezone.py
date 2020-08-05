from bunnyhop.base import BaseBunny


class StorageZone(BaseBunny):
    
    def get(self, id):
        api_url = self._URL + '/storagezone/' + id
        header = self._GetHeaders()
        response = self._CallApi(api_url, "GET", header)
        return response.text