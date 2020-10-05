from bunnyhop import base


class Billing(base.BaseBunny):

    def get(self):
        return BillingSummary(self.api_key, **self.call_api(f"/billing", "GET"))

    def apply_code(self, coupon_code):
        return self.call_api(f"/billing/applycode?couponCode={coupon_code}", "GET")


class BillingRecord(base.BaseBunny):
    Id = base.IntegerProperty()
    PaymentId = base.CharProperty()
    Amount = base.FloatProperty()
    Payer = base.EmailProperty()
    Timestamp = base.DateTimeProperty()
    Type = base.IntegerProperty()
    InvoiceAvailable = base.BooleanProperty()

    def __str__(self):
        return f"{self.Id} - {self.Amount}"


class BillingSummary(base.BaseBunny):
    Balance = base.FloatProperty(required=True)
    ThisMonthCharges = base.FloatProperty(required=True)
    BillingRecords = base.ListProperty(BillingRecord)
    MonthlyChargesStorage = base.FloatProperty(required=True)
    MonthlyChargesEUTraffic = base.FloatProperty(required=True)
    MonthlyChargesUSTraffic = base.FloatProperty(required=True)
    MonthlyChargesASIATraffic = base.FloatProperty(required=True)
    MonthlyChargesSATraffic = base.FloatProperty(required=True)

    def __str__(self):
        return f"{self.Balance}"

    @property
    def billing_records(self):
        return [BillingRecord(self.api_key, **i) for i in self.BillingRecords]
