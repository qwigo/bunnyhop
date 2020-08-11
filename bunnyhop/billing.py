from bunnyhop import base


class Billing(base.BaseBunny):
    
    def get(self):

        return BillingSummary(self.api_key, **self.call_api(f"{self.endpoint_url}/billing", "GET", self.get_header()))

    def applycode(self, couponCode):
        return self.call_api(f"{self.endpoint_url}/billing/applycode?couponCode={couponCode}", "GET", self.get_header())


class BillingRecord(base.BaseBunny):
    Id = base.IntegerProperty()
    PaymentId = base.CharProperty()
    Amount = base.FloatProperty()
    Payer = base.EmailProperty()
    Timestamp = base.DateTimeProperty()
    Type = base.IntegerProperty()
    InvoiceAvailable = base.BooleanProperty()


class BillingSummary(base.BaseBunny):
    Balance = base.FloatProperty(required=True)
    ThisMonthCharges = base.FloatProperty(required=True)
    BillingRecords = base.ListProperty(BillingRecord)
    MonthlyChargesStorage = base.FloatProperty(required=True)
    MonthlyChargesEUTraffic = base.FloatProperty(required=True)
    MonthlyChargesUSTraffic = base.FloatProperty(required=True)
    MonthlyChargesASIATraffic = base.FloatProperty(required=True)
    MonthlyChargesSATraffic = base.FloatProperty(required=True)

    @property
    def billing_records(self):
        return [BillingRecord(self.api_key, **i) for i in self.BillingRecords]