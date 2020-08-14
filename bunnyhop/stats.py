from bunnyhop.base import BaseBunny


class Stats(BaseBunny):

    def get(self, date_from, date_to, pull_zone, server_zone_id):
        return self.call_api(
            f"/statistics?dateFrom={date_from}&dateTo={date_to}&pullZone={pull_zone}&serverZoneId={server_zone_id}",
            "GET")
