from bunnyhop.base import BaseBunny


class Purge(BaseBunny):
    
    def create(self, url):
        api_url = self.endpoint_url + '/purge?url=' + url
        header = self.get_header()
        response = self.call_api(api_url, "POST", header)
        return self.format_response(response)