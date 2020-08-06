from bunnyhop.base import BaseBunny


class Storage(BaseBunny):

    def create(self, name, main_storage_region, replica_regions):
        api_url = self.endpoint_url + '/storagezone'
        header = self.get_header()
        api_data = {
            'Name': name,
            'Region': main_storage_region,
            'ReplicationRegions': replica_regions,
        }
        response = self.call_api(api_url, "POST", header, api_data)
        return self.format_response(response)

    def all(self):
        api_url = self.endpoint_url + '/storagezone'
        header = self.get_header()
        response = self.call_api(api_url, "GET", header)
        return response.text

    def delete(self, id):
        api_url = self.endpoint_url + '/storagezone/' + id
        header = self.get_header()
        response = self.call_api(api_url, "DELETE", header)
        return self.format_response(response)

    def get(self, id):
        api_url = self.endpoint_url + '/storagezone/' + id
        header = self.get_header()
        response = self.call_api(api_url, "GET", header)
        return response.text
