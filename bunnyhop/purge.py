from bunnyhop.base import BaseBunny


class Purge(BaseBunny):

    def create(self, url):
        return self.call_api(f"/purge?url=", "POST", self.get_header())
