from bunnyhop.base import BaseBunny


class Billing(BaseBunny):
    
    def get(self):
        api_url = self.endpoint_url + '/billing'
        header = self.get_header()
        response = self._CallApi(api_url, "GET", header)
        return self._FormatResponse(response)

    def applycode(self, couponCode):
        api_url = self.endpoint_url + '/billing/applycode?couponCode=' + couponCode
        header = self.get_header()
        response = self._CallApi(api_url, "GET", header)
        return self._FormatResponse(response)