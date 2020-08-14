from bunnyhop.base import BaseBunny


class Zone(BaseBunny):

    def get(self, id):
        return self.call_api(f"{self.endpoint_url}/pullzone/{id}", "GET", self.get_header())

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
