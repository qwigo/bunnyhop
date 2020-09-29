from bunnyhop import base


class Zone(base.BaseBunny):
    Id = base.IntegerProperty()
    Name = base.CharProperty()
    OriginUrl = base.CharProperty()
    Enabled = base.BooleanProperty()
    Hostnames = base.ListProperty()
    StorageZoneId = base.IntegerProperty()
    AllowedReferrers = base.ListProperty()
    BlockedReferrers = base.ListProperty()
    BlockedIps = base.ListProperty()
    EnableGeoZoneUS = base.BooleanProperty()
    EnableGeoZoneEU = base.BooleanProperty()
    EnableGeoZoneASIA = base.BooleanProperty()
    EnableGeoZoneSA = base.BooleanProperty()
    EnableGeoZoneAF = base.BooleanProperty()
    ZoneSecurityEnabled = base.BooleanProperty()
    ZoneSecurityKey = base.CharProperty()
    ZoneSecurityIncludeHashRemoteIP = base.BooleanProperty()
    IgnoreQueryStrings = base.BooleanProperty()
    
    # {'Id': 158540,
    #  'Name': 'dnsly',
    #  'OriginUrl': 'http://dnsly.net',
    #  'Enabled': True,
    #  'Hostnames': [{'Id': 284382,
    #                 'Value': 'dnsly.b-cdn.net',
    #                 'ForceSSL': False,
    #                 'IsSystemHostname': True,
    #                 'HasCertificate': True}],
    #  'StorageZoneId': 0,
    #  'AllowedReferrers': [],
    #  'BlockedReferrers': [],
    #  'BlockedIps': [],
    #  'EnableGeoZoneUS': True,
    #  'EnableGeoZoneEU': True,
    #  'EnableGeoZoneASIA': True,
    #  'EnableGeoZoneSA': True,
    #  'EnableGeoZoneAF': True,
    #  'ZoneSecurityEnabled': False,
    #  'ZoneSecurityKey': 'afb60141-1654-4f9c-a9ed-40eb1678bcea',
    #  'ZoneSecurityIncludeHashRemoteIP': False,
    #  'IgnoreQueryStrings': False,
    #  'MonthlyBandwidthLimit': 0,
    #  'MonthlyBandwidthUsed': 0,
    #  'MonthlyCharges': 0.0,
    #  'AddHostHeader': False,
    #  'Type': 1,
    #  'CustomNginxConfig': '',
    #  'AccessControlOriginHeaderExtensions': ['eot', 'ttf', 'woff', 'woff2', 'css'],
    #  'EnableAccessControlOriginHeader': True,
    #  'DisableCookies': True,
    #  'BudgetRedirectedCountries': [],
    #  'BlockedCountries': [],
    #  'EnableOriginShield': True,
    #  'CacheControlMaxAgeOverride': -1,
    #  'CacheControlPublicMaxAgeOverride': -1,
    #  'BurstSize': 0,
    #  'RequestLimit': 0,
    #  'BlockRootPathAccess': False,
    #  'BlockPostRequests': False,
    #  'CacheQuality': 75,
    #  'LimitRatePerSecond': 0.0,
    #  'LimitRateAfter': 0.0,
    #  'ConnectionLimitPerIPCount': 0,
    #  'PriceOverride': 0.0,
    #  'AddCanonicalHeader': False,
    #  'EnableLogging': True,
    #  'IgnoreVaryHeader': True,
    #  'EnableCacheSlice': True,
    #  'EdgeRules': [],
    #  'EnableWebPVary': False,
    #  'EnableCountryCodeVary': False,
    #  'EnableMobileVary': False,
    #  'EnableHostnameVary': False,
    #  'CnameDomain': 'b-cdn.net',
    #  'AWSSigningEnabled': False,
    #  'AWSSigningKey': None,
    #  'AWSSigningSecret': None,
    #  'AWSSigningRegionName': None,
    #  'LoggingIPAnonymizationEnabled': False,
    #  'EnableTLS1': True,
    #  'EnableTLS1_1': True,
    #  'VerifyOriginSSL': False,
    #  'OriginShieldZoneCode': 'IL'}
    def get(self, id):
        return self.call_api(f"/pullzone/{id}", "GET", self.get_header())

    def create(self, Name=None, OriginUrl=None, StorageZoneId=None, Type=None):
        api_data = {
            'Name': Name,
            'Type': Type,
            'OriginUrl': OriginUrl,
            'StorageZoneId': StorageZoneId
        }
        return self.call_api(f"/pullzone", "POST", self.get_header(), api_data)

    def list(self):
        return self.call_api(f"/pullzone", "GET", self.get_header())

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
        return self.call_api(f"/pullzone/{id}", "POST", self.get_header(), api_data)

    def delete(self, id):
        return self.call_api(f"/pullzone/{id}", "DELETE", self.get_header())

    def purge(self, id):
        return self.call_api(f"/pullzone/{id}/purgeCache", "POST", self.get_header())

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
        return self.call_api(f"/pullzone/{id}/edgerules/addOrUpdate", "POST", self.get_header(), api_data)
