from bunnyhop import base

STREAM_ENDPOINT = "https://video.bunnycdn.com"


class StreamLibrary(base.BaseBunny):
    Id = base.IntegerProperty()
    Name = base.CharProperty()
    VideoCount = base.IntegerProperty()
    TrafficUsage = base.IntegerProperty()
    StorageUsage = base.IntegerProperty()
    DateCreated = base.DateTimeProperty(required=False)
    ApiKey = base.CharProperty(required=False)
    ReadOnlyApiKey = base.CharProperty(required=False)
    ReplicationRegions = base.ListProperty()
    AllowedReferrers = base.ListProperty()
    BlockedReferrers = base.ListProperty()
    BlockNoneReferrer = base.BooleanProperty(default_value=False)
    EnableTokenAuthentication = base.BooleanProperty(default_value=False)
    EnableTokenIPVerification = base.BooleanProperty(default_value=False)
    PlayerKeyColor = base.CharProperty(required=False)
    CustomHTML = base.CharProperty(required=False)
    WatermarkPositionLeft = base.IntegerProperty(required=False)
    WatermarkPositionTop = base.IntegerProperty(required=False)
    WatermarkWidth = base.IntegerProperty(required=False)
    WatermarkHeight = base.IntegerProperty(required=False)
    EnableMP4Fallback = base.BooleanProperty(default_value=False)
    KeepOriginalFiles = base.BooleanProperty(default_value=False)
    AllowDirectPlay = base.BooleanProperty(default_value=False)
    EnableDRM = base.BooleanProperty(default_value=False)
    EnableTranscribing = base.BooleanProperty(default_value=False)
    TranscribingLanguage = base.CharProperty(required=False)
    StorageZoneId = base.IntegerProperty(required=False)
    PullZoneId = base.IntegerProperty(required=False)

    def __str__(self):
        return self.Name or ""

    def add_allowed_referrer(self, hostname):
        referrers = list(self.AllowedReferrers or [])
        if hostname not in referrers:
            referrers.append(hostname)
        return self.call_api(f"/videolibrary/{self.Id}", "POST",
                             json_data={"AllowedReferrers": referrers},
                             endpoint_url=STREAM_ENDPOINT)

    def remove_allowed_referrer(self, hostname):
        referrers = [r for r in (self.AllowedReferrers or []) if r != hostname]
        return self.call_api(f"/videolibrary/{self.Id}", "POST",
                             json_data={"AllowedReferrers": referrers},
                             endpoint_url=STREAM_ENDPOINT)


class Stream(base.BaseBunny):

    def list(self, page=1, per_page=100, search=None, include_access_key=False):
        params = {"page": page, "perPage": per_page}
        if search is not None:
            params["search"] = search
        if include_access_key:
            params["includeAccessKey"] = True
        response = self.call_api("/videolibrary", "GET", params=params,
                                 endpoint_url=STREAM_ENDPOINT)
        return [StreamLibrary(self.api_key, **item) for item in response.get("items", [])]

    def get(self, library_id, include_access_key=False):
        params = {}
        if include_access_key:
            params["includeAccessKey"] = True
        response = self.call_api(f"/videolibrary/{library_id}", "GET", params=params,
                                 endpoint_url=STREAM_ENDPOINT)
        return StreamLibrary(self.api_key, **response)

    def create(self, name, replication_regions=None):
        api_data = {"Name": name}
        if replication_regions is not None:
            api_data["ReplicationRegions"] = replication_regions
        response = self.call_api("/videolibrary", "POST", json_data=api_data,
                                 endpoint_url=STREAM_ENDPOINT)
        if isinstance(response, dict) and response.get("Id"):
            return StreamLibrary(self.api_key, **response)
        raise ValueError(
            f"Stream library creation failed: "
            f"{response.get('message', response) if isinstance(response, dict) else response}"
        )

    def update(self, library_id, **kwargs):
        api_data = {k: v for k, v in kwargs.items() if v is not None}
        response = self.call_api(f"/videolibrary/{library_id}", "POST",
                                 json_data=api_data, endpoint_url=STREAM_ENDPOINT)
        if isinstance(response, bytes):
            return "Library updated."
        return response

    def delete(self, library_id):
        response = self.call_api(f"/videolibrary/{library_id}", "DELETE",
                                 endpoint_url=STREAM_ENDPOINT)
        if isinstance(response, bytes):
            return "Library deleted."
        return response

    def add_allowed_referrer(self, library_id, hostname):
        lib = self.get(library_id)
        referrers = list(lib.AllowedReferrers or [])
        if hostname not in referrers:
            referrers.append(hostname)
        return self.update(library_id, AllowedReferrers=referrers)

    def remove_allowed_referrer(self, library_id, hostname):
        lib = self.get(library_id)
        referrers = [r for r in (lib.AllowedReferrers or []) if r != hostname]
        return self.update(library_id, AllowedReferrers=referrers)
