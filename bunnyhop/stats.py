from bunnyhop.base import BaseBunny


class Stats(BaseBunny):
    
    def get(self, dateFrom, dateTo, pullZone, serverZoneId):
        api_url = self._URL + '/statistics?dateFrom=/' + dateFrom + '&dateTo='
        + dateTo + '&pullZone=' + pullZone + '&serverZoneId=' + serverZoneId
        header = self._GetHeaders()
        response = self._CallApi(api_url, "GET", header)
        return self._FormatResponse(response)