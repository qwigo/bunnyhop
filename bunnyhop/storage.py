from bunnyhop.base import BaseBunny


class Storage(BaseBunny):

    def create(self, name, main_storage_region, replica_regions):
        api_url = self._URL + '/storagezone'
        header = self._GetHeaders()
        api_data = {
            'Name': name,
            'Region': main_storage_region,
            'ReplicationRegions': replica_regions,
        }
        response = self._CallApi(api_url, "POST", header, api_data)
        return self._FormatResponse(response)

    def all(self):
        api_url = self._URL + '/storagezone'
        header = self._GetHeaders()
        response = self._CallApi(api_url, "GET", header)
        return response.text

    def delete(self, id):
        api_url = self._URL + '/storagezone/' + id
        header = self._GetHeaders()
        response = self._CallApi(api_url, "DELETE", header)
        return self._FormatResponse(response)

    def get(self, id):
        api_url = self._URL + '/storagezone/' + id
        header = self._GetHeaders()
        response = self._CallApi(api_url, "GET", header)
        return self._FormatResponse(response)
