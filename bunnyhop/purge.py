from bunnyhop.base import BaseBunny


class Purge(BaseBunny):
    
    def create(self, url):
        api_url = self._URL + '/purge?url=' + url
        header = self.get_header()
        response = self._CallApi(api_url, "POST", header)
        return self._FormatResponse(response)