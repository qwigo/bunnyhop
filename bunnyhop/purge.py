from bunnyhop.base import BaseBunny


class Purge(BaseBunny):

    def create(self, url):
        return self.call_api("/purge", "GET", params={'url': url})
