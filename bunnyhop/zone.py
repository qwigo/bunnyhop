from bunnyhop import base


class Zone(base.BaseBunny):
    Id = base.IntegerProperty()
    Name = base.CharProperty()
    OriginUrl = base.CharProperty()
    Enabled = base.BooleanProperty(default_value=False)
    Hostnames = base.ListProperty()
    StorageZoneId = base.IntegerProperty()
    AllowedReferrers = base.ListProperty()
    BlockedReferrers = base.ListProperty()
    BlockedIps = base.ListProperty()
    EnableGeoZoneUS = base.BooleanProperty(default_value=False)
    EnableGeoZoneEU = base.BooleanProperty(default_value=False)
    EnableGeoZoneASIA = base.BooleanProperty(default_value=False)
    EnableGeoZoneSA = base.BooleanProperty(default_value=False)
    EnableGeoZoneAF = base.BooleanProperty(default_value=False)
    ZoneSecurityEnabled = base.BooleanProperty(default_value=False)
    ZoneSecurityKey = base.CharProperty()
    ZoneSecurityIncludeHashRemoteIP = base.BooleanProperty(default_value=False)
    IgnoreQueryStrings = base.BooleanProperty(default_value=False)
    MonthlyBandwidthLimit = base.IntegerProperty()
    MonthlyBandwidthUsed = base.IntegerProperty()
    MonthlyCharges = base.FloatProperty()
    AddHostHeader = base.BooleanProperty(default_value=False)
    Type = base.IntegerProperty()
    CustomNginxConfig = base.CharProperty()
    AccessControlOriginHeaderExtensions = base.ListProperty()
    EnableAccessControlOriginHeader = base.BooleanProperty(default_value=False)
    DisableCookies = base.BooleanProperty(default_value=False)
    BudgetRedirectedCountries = base.ListProperty()
    BlockedCountries = base.ListProperty()
    EnableOriginShield = base.BooleanProperty(default_value=False)
    CacheControlMaxAgeOverride = base.IntegerProperty()
    CacheControlPublicMaxAgeOverride = base.IntegerProperty()
    BurstSize = base.IntegerProperty()
    RequestLimit = base.IntegerProperty()
    BlockRootPathAccess = base.BooleanProperty(default_value=False)
    BlockPostRequests = base.BooleanProperty(default_value=False)
    CacheQuality = base.IntegerProperty()
    LimitRatePerSecond = base.FloatProperty()
    LimitRateAfter = base.FloatProperty()
    ConnectionLimitPerIPCount = base.IntegerProperty()
    PriceOverride = base.FloatProperty()
    AddCanonicalHeader = base.BooleanProperty(default_value=False)
    EnableLogging = base.BooleanProperty(default_value=False)
    IgnoreVaryHeader = base.BooleanProperty(default_value=False)
    EnableCacheSlice = base.BooleanProperty(default_value=False)
    EdgeRules = base.ListProperty()
    EnableWebPVary = base.BooleanProperty(default_value=False)
    EnableCountryCodeVary = base.BooleanProperty(default_value=False)
    EnableMobileVary = base.BooleanProperty(default_value=False)
    EnableHostnameVary = base.BooleanProperty(default_value=False)
    CnameDomain = base.CharProperty()
    AWSSigningEnabled = base.BooleanProperty(default_value=False)
    AWSSigningKey = base.CharProperty()
    AWSSigningSecret = base.CharProperty()
    AWSSigningRegionName = base.CharProperty()
    LoggingIPAnonymizationEnabled = base.BooleanProperty(default_value=False)
    EnableTLS1 = base.BooleanProperty(default_value=False)
    EnableTLS1_1 = base.BooleanProperty(default_value=False)
    VerifyOriginSSL = base.BooleanProperty(default_value=False)
    OriginShieldZoneCode = base.CharProperty()

    def __str__(self):
        return self.Name

    @property
    def host_names(self):
        return [Hostname(self.api_key, **i) for i in self.Hostnames]

    def get(self, id):
        response = self.call_api(f"/pullzone/{id}", "GET")
        try:
            if response.get('Id', None):
                return Zone(self.api_key, **response)
        except:
            return "Zone not found."

    def create(self, Name, Type, OriginUrl, StorageZoneId=None):
        api_data = {
            'Name': Name,
            'Type': Type,
            'OriginUrl': OriginUrl,
            'StorageZoneId': StorageZoneId
        }
        response = self.call_api(f"/pullzone", "POST", self.get_header(),
                                 json_data=api_data)

        if response.get('Id', None):
            return Zone(self.api_key, **response)
        return response

    def list(self):
        return [Zone(self.api_key, **i) for i in self.call_api(f"/pullzone",
                                                               "GET")]

    def update(
            self,
            id,
            OriginUrl=None,
            AllowedReferrers=None,
            BlockedIps=None,
            EnableCacheSlice=None,
            EnableGeoZoneUS=None,
            EnableGeoZoneEU=None,
            EnableGeoZoneASIA=None,
            EnableGeoZoneSA=None,
            EnableGeoZoneAF=None,
            ZoneSecurityEnabled=None,
            ZoneSecurityIncludeHashRemoteIP=None,
            IgnoreQueryStrings=None,
            MonthlyBandwidthLimit=None,
            AccessControlOriginHeaderExtensions=None,
            EnableAccessControlOriginHeader=None,
            BlockRootPathAccess=None,
            EnableWebpVary=None,
            EnableLogging=None,
            DisableCookies=None,
            BudgetRedirectedCountries=None,
            BlockedCountries=None,
            EnableOriginShield=None,
            OriginShieldZoneCode=None,
            AddCanonicalHeader=None,
            CacheControlMaxAgeOverride=None,
            AddHostHeader=None,
            AWSSigningEnabled=None,
            AWSSigningKey=None,
            AWSSigningRegionName=None,
            AWSSigningSecret=None,
            EnableTLS1=None,
            EnableTLS1_1=None):
        api_data = {
            "OriginUrl": OriginUrl,
            "AllowedReferrers": AllowedReferrers,
            "BlockedIps": BlockedIps,
            "EnableCacheSlice": EnableCacheSlice,
            "EnableGeoZoneUS": EnableGeoZoneUS,
            "EnableGeoZoneEU": EnableGeoZoneEU,
            "EnableGeoZoneASIA": EnableGeoZoneASIA,
            "EnableGeoZoneSA": EnableGeoZoneSA,
            "EnableGeoZoneAF": EnableGeoZoneAF,
            "ZoneSecurityEnabled": ZoneSecurityEnabled,
            "ZoneSecurityIncludeHashRemoteIP": ZoneSecurityIncludeHashRemoteIP,
            "IgnoreQueryStrings": IgnoreQueryStrings,
            "MonthlyBandwidthLimit": MonthlyBandwidthLimit,
            "AccessControlOriginHeaderExtensions":
                AccessControlOriginHeaderExtensions,
            "EnableAccessControlOriginHeader": EnableAccessControlOriginHeader,
            "BlockRootPathAccess": BlockRootPathAccess,
            "EnableWebpVary": EnableWebpVary,
            "EnableLogging": EnableLogging,
            "DisableCookies": DisableCookies,
            "BudgetRedirectedCountries": BudgetRedirectedCountries,
            "BlockedCountries": BlockedCountries,
            "EnableOriginShield": EnableOriginShield,
            "OriginShieldZoneCode": OriginShieldZoneCode,
            "AddCanonicalHeader": AddCanonicalHeader,
            "CacheControlMaxAgeOverride": CacheControlMaxAgeOverride,
            "AddHostHeader": AddHostHeader,
            "AWSSigningEnabled": AWSSigningEnabled,
            "AWSSigningKey": AWSSigningKey,
            "AWSSigningRegionName": AWSSigningRegionName,
            "AWSSigningSecret": AWSSigningSecret,
            "EnableTLS1": EnableTLS1,
            "EnableTLS1_1": EnableTLS1_1
        }
        return self.call_api(f"/pullzone/{id}", "POST", self.get_header(),
                             json_data=api_data)

    def delete(self, id):
        response = self.call_api(f"/pullzone/{id}", "DELETE",
                                 self.get_header())
        if type(response) is bytes:
            return "Zone deleted."
        return response

    def purge(self, id):
        response = self.call_api(f"/pullzone/{id}/purgeCache", "POST",
                                 self.get_header())
        if type(response) is bytes:
            return "Purge Queue was finished."
        return response

    def purge_file(self, filename):
        url = (f"http://{self.host_names[0].Value}/{filename}")
        response = self.call_api(f"/purge", "POST", params={'url': url})
        if type(response) is bytes:
            return "Purge Queue was finished."
        return response

    def create_edge_rule(
            self,
            id,
            Guid=None,
            ActionParameter1=None,
            ActionParameter2=None,
            Enabled=None,
            Description=None,
            ActionType=None,
            TriggerMatchingType=None,
            Triggers=None):
        api_data = {
            "Guid": Guid,
            "ActionParameter1": ActionParameter1,
            "ActionParameter2": ActionParameter2,
            "Enabled": Enabled,
            "Description": Description,
            "ActionType": ActionType,
            "TriggerMatchingType": TriggerMatchingType,
            "Triggers": Triggers
        }
        response = self.call_api(f"/pullzone/{id}/edgerules/addOrUpdate",
                                 "POST", self.get_header(), json_data=api_data)
        if type(response) is bytes:
            return"Successfully Added/Updated an edge rule."
        return response


class Hostname(base.BaseBunny):
    Id = base.IntegerProperty()
    Value = base.CharProperty()
    ForceSSL = base.BooleanProperty(default_value=False)
    IsSystemHostname = base.BooleanProperty(default_value=False)
    HasCertificate = base.BooleanProperty(default_value=False)

    def __str__(self):
        return f"{self.Value}"
