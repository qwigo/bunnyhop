from bunnyhop.base import BaseBunny


class Stats(BaseBunny):
    
    def get(self, dateFrom, dateTo, pullZone, serverZoneId):
        api_url = self.endpoint_url + '/statistics?dateFrom=/' + dateFrom + '&dateTo=' + dateTo + '&pullZone=' + pullZone + '&serverZoneId=' + serverZoneId
        header = self.get_header()
        response = self.call_api(api_url, "GET", header)
        return self.format_response(response)