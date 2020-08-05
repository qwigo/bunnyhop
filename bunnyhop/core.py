from bunnyhop.storage import Storage
from bunnyhop.zone import Zone

class Bunny(object):

    def __init__(self, api_key):
        self.Zone = Zone(api_key)
        # self.Purge = Purge(api_key)
        self.Storage = Storage(api_key)
        # self.StorageZone = StorageZone(api_key)
        # self.Stats = Stats(api_key)
        # self.Billing = Billing(api_key)
