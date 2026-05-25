from bunnyhop import base


class DNSRecord(base.BaseBunny):
    Id = base.IntegerProperty()
    Type = base.IntegerProperty()
    Ttl = base.IntegerProperty()
    Value = base.CharProperty()
    Name = base.CharProperty()
    Weight = base.IntegerProperty()
    Priority = base.IntegerProperty()
    Port = base.IntegerProperty()
    Flags = base.IntegerProperty()
    Tag = base.CharProperty()
    Accelerated = base.BooleanProperty(default_value=False)
    AcceleratedPullZoneId = base.IntegerProperty()
    LinkName = base.CharProperty()
    MonitorType = base.IntegerProperty()
    GeolocationLat = base.FloatProperty()
    GeolocationLong = base.FloatProperty()
    EnvironmentTagId = base.IntegerProperty()
    Comment = base.CharProperty()

    def __str__(self):
        return f"{self.Name} ({self.Type})"


class DNSZone(base.BaseBunny):
    Id = base.IntegerProperty()
    Domain = base.CharProperty()
    Records = base.ListProperty()
    DateModified = base.DateTimeProperty(required=False)
    DateCreated = base.DateTimeProperty(required=False)
    NameserversDetected = base.BooleanProperty(default_value=False)
    CustomNameserversEnabled = base.BooleanProperty(default_value=False)
    Nameserver1 = base.CharProperty()
    Nameserver2 = base.CharProperty()
    SoaEmail = base.CharProperty()
    DnsSecEnabled = base.BooleanProperty(default_value=False)
    LoggingEnabled = base.BooleanProperty(default_value=False)
    LoggingIPAnonymizationEnabled = base.BooleanProperty(default_value=False)
    LogAnonymizationType = base.IntegerProperty()

    def __str__(self):
        return self.Domain or ""

    @property
    def dns_records(self):
        return [DNSRecord(self.api_key, **r) for r in (self.Records or [])]


class DNS(base.BaseBunny):

    def list(self, page=1, per_page=100, search=None):
        params = {"page": page, "perPage": per_page}
        if search is not None:
            params["search"] = search
        response = self.call_api("/dnszone", "GET", params=params)
        return [DNSZone(self.api_key, **z) for z in response.get("Items", [])]

    def get(self, id):
        response = self.call_api(f"/dnszone/{id}", "GET")
        try:
            if response.get("Id"):
                return DNSZone(self.api_key, **response)
        except (AttributeError, TypeError):
            pass
        return response

    def create(self, domain):
        response = self.call_api("/dnszone", "POST", json_data={"Domain": domain})
        if response.get("Id"):
            return DNSZone(self.api_key, **response)
        return response

    def update(self, id, **kwargs):
        response = self.call_api(f"/dnszone/{id}", "POST", json_data=kwargs)
        if type(response) is bytes:
            return "DNS zone updated."
        return response

    def delete(self, id):
        response = self.call_api(f"/dnszone/{id}", "DELETE")
        if type(response) is bytes:
            return "DNS zone deleted."
        return response

    def enable_dnssec(self, id):
        response = self.call_api(f"/dnszone/{id}/dnssec", "POST")
        if type(response) is bytes:
            return "DNSSEC enabled."
        return response

    def disable_dnssec(self, id):
        response = self.call_api(f"/dnszone/{id}/dnssec", "DELETE")
        if type(response) is bytes:
            return "DNSSEC disabled."
        return response

    def create_record(self, zone_id, Type, Name, Value, Ttl=300, **kwargs):
        json_data = {"Type": Type, "Name": Name, "Value": Value, "Ttl": Ttl}
        json_data.update(kwargs)
        response = self.call_api(f"/dnszone/{zone_id}/records", "PUT", json_data=json_data)
        if isinstance(response, dict) and response.get("Id"):
            return DNSRecord(self.api_key, **response)
        return response

    def update_record(self, zone_id, record_id, **kwargs):
        response = self.call_api(f"/dnszone/{zone_id}/records/{record_id}", "POST", json_data=kwargs)
        if type(response) is bytes:
            return "DNS record updated."
        return response

    def delete_record(self, zone_id, record_id):
        response = self.call_api(f"/dnszone/{zone_id}/records/{record_id}", "DELETE")
        if type(response) is bytes:
            return "DNS record deleted."
        return response
