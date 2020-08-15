from bunnyhop import base


class Stats(base.BaseBunny):
    TotalBandwidthUsed = base.IntegerProperty()
    TotalRequestsServed = base.IntegerProperty()
    CacheHitRate = base.FloatProperty()
    BandwidthUsedChart = base.DictProperty()
    BandwidthCachedChart = base.DictProperty()
    CacheHitRateChart = base.DictProperty()
    RequestsServedChart = base.DictProperty()
    PullRequestsPulledChart = base.DictProperty()
    OriginShieldBandwidthUsedChart = base.DictProperty()
    OriginShieldInternalBandwidthUsedChart = base.DictProperty()
    UserBalanceHistoryChart = base.DictProperty()
    GeoTrafficDistribution = base.DictProperty()
    Error3xxChart = base.DictProperty()
    Error4xxChart = base.DictProperty()
    Error5xxChart = base.DictProperty()

    def __str__(self):
        return f"Bandwidth: {self.TotalBandwidthUsed} | Total Requests: {self.TotalRequestsServed} | " \
               f"CacheHitRate: {self.CacheHitRate}"

    def get(self, date_from=None, date_to=None, pull_zone=None, server_zone_id=None):
        params = {
            'dateFrom': date_from,
            'dateTo': date_to,
            'pullZone': pull_zone,
            'serverZoneId': server_zone_id
        }
        return Stats(self.api_key, **self.call_api(
            f"/statistics?dateFrom", "GET", params=params))
