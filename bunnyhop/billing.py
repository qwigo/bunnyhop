from bunnyhop.base import BaseBunny


class Billing(BaseBunny):
    
    def get(self):
        return self.call_api(f"{self.endpoint_url}/billing", "GET", self.get_header())

    def applycode(self, couponCode):
        return self.call_api(f"{self.endpoint_url}/billing/applycode?couponCode={couponCode}", "GET", self.get_header())
    