from bunnyhop.base import BaseBunny


class Zone(BaseBunny):

    def get(self, id):
        api_url = self._URL + '/pullzone/' + id
        header = self._GetHeaders()
        response = self._CallApi(api_url, "GET", header)
        return self._FormatResponse(response)

    def create(self, Name, OriginUrl, StorageZoneId, Type=0):
        api_url = self._URL + '/pullzone'
        header = self._GetHeaders()
        api_data = {
            'Name': Name,
            'Type': Type,
            'OriginUrl': OriginUrl,
            'StorageZoneId': StorageZoneId
        }
        response = self._CallApi(api_url, "POST", header, api_data)
        return self._FormatResponse(response)

    def list(self):
        api_url = self._URL + '/pullzone'
        header = self._GetHeaders()
        response = self._CallApi(api_url, "GET", header)
        return self._FormatResponse(response)

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
        api_url = self._URL + '/pullzone/' + id
        header = self._GetHeaders()
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
        response = self._CallApi(api_url, "POST", header, api_data)
        return self._FormatResponse(response)

    def delete(self, id):
        api_url = self._URL + '/pullzone/' + id
        header = self._GetHeaders()
        response = self._CallApi(api_url, "DELETE", header)
        return self._FormatResponse(response)

    def purge(self, id):
        api_url = self._URL + '/pullzone/' + id + '/purgeCache'
        header = self._GetHeaders()
        response = self._CallApi(api_url, "POST", header, {})
        return self._FormatResponse(response)

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
        api_url = self._URL + '/pullzone/' + id + '/edgerules/addOrUpdate'
        header = self._GetHeaders()
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
        response = self._CallApi(api_url, "POST", header, api_data)
        return self._FormatResponse(response)
