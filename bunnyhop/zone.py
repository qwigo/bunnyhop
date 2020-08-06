from bunnyhop.base import BaseBunny


class Zone(BaseBunny):

    def get(self, id):
        api_url = self.endpoint_url + '/pullzone/' + id
        header = self.get_header()
        response = self.call_api(api_url, "GET", header)
        return response.text

    def create(self, Name, OriginUrl, StorageZoneId, Type=0):
        api_url = self.endpoint_url + '/pullzone'
        header = self.get_header()
        api_data = {
            'Name': Name,
            'Type': Type,
            'OriginUrl': OriginUrl,
            'StorageZoneId': StorageZoneId
        }
        response = self.call_api(api_url, "POST", header, api_data)
        return self.format_response(response)

    def list(self):
        api_url = self.endpoint_url + '/pullzone'
        header = self.get_header()
        response = self.call_api(api_url, "GET", header)
        return response.text

    def update(
                self,
                id,
                OriginUrl,
                AllowedReferrers,
                BlockedIps,
                EnableCacheSlice,
                EnableGeoZoneUS,
                EnableGeoZoneEU,
                EnableGeoZoneASIA,
                EnableGeoZoneSA,
                EnableGeoZoneAF,
                ZoneSecurityEnabled,
                ZoneSecurityIncludeHashRemoteIP,
                IgnoreQueryStrings,
                MonthlyBandwidthLimit,
                AccessControlOriginHeaderExtensions,
                EnableAccessControlOriginHeader,
                BlockRootPathAccess,
                EnableWebpVary,
                EnableLogging,
                DisableCookies,
                BudgetRedirectedCountries,
                BlockedCountries,
                EnableOriginShield,
                OriginShieldZoneCode,
                AddCanonicalHeader,
                CacheControlMaxAgeOverride,
                AddHostHeader,
                AWSSigningEnabled,
                AWSSigningKey,
                AWSSigningRegionName,
                AWSSigningSecret,
                EnableTLS1,
                EnableTLS1_1):
        api_url = self.endpoint_url + '/pullzone/' + id
        header = self.get_header()
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
        response = self.call_api(api_url, "POST", header, api_data)
        return self.format_response(response)

    def delete(self, id):
        api_url = self.endpoint_url + '/pullzone/' + id
        header = self.get_header()
        response = self.call_api(api_url, "DELETE", header)
        return self.format_response(response)

    def purge(self, id):
        api_url = self.endpoint_url + '/pullzone/' + id + '/purgeCache'
        header = self.get_header()
        response = self.call_api(api_url, "POST", header, {})
        return self.format_response(response)

    def create_edge_rule(
                         self,
                         id,
                         Guid,
                         ActionParameter1,
                         ActionParameter2,
                         Enabled,
                         Description,
                         ActionType,
                         TriggerMatchingType,
                         Triggers):
        api_url = self.endpoint_url + '/pullzone/' + id + '/edgerules/addOrUpdate'
        header = self.get_header()
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
        response = self.call_api(api_url, "POST", header, api_data)
        return self.format_response(response)
