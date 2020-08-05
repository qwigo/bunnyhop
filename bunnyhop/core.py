from bunnyhop.storage import Storage
from bunnyhop.zone import Zone


class Bunny(object):

    def __init__(self, api_key):
        self.api_key = api_key
        self.Storage = Storage(self.api_key)
        self.Zone = Zone(self.api_key)
