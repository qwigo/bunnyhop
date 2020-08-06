from bunnyhop.base import BaseBunny


class Purge(BaseBunny):
    
    def create(self, url):
        return self.call_api(f"{self.endpoint_url}/purge?url=", "POST", self.get_header())
        