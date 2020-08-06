from bunnyhop.base import BaseBunny


class Billing(BaseBunny):
    
    def get(self):
        api_url = self.endpoint_url + '/billing'
        header = self.get_header()
        response = self.call_api(api_url, "GET", header)
        return self.format_response(response)

    def applycode(self, couponCode):
        api_url = self.endpoint_url + '/billing/applycode?couponCode=' + couponCode
        header = self.get_header()
        response = self.call_api(api_url, "GET", header)
        return self.format_response(response)