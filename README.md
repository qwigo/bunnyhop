# bunnyhop
Python library for BunnyCDN

## Status
Documentation only phase

## Install

```shell script
pip install bunnyhop
```

## Getting Started 

```python
from bunnyhop import Bunny

b = Bunny('<api_key>')
```
## Pull Zones

#### Get a Pull Zone

```python
zone = b.Zone.get(id='myzone')
#Returns: <Zone: myzone > 
```

#### Create a Pull Zone
```python
b.Zone.create(
    Name='myzone',
    Type=0, # 0 = Standard and 1 = High Volume
    OriginUrl='https://example.org',
    StorageZoneId='storage-zone-id'
)
```

#### List Pull Zones
```python
b.Zone.list()
```

#### Update a Pull Zone
```python
b.Zone.update(
    id='zone-id', #Positional Argument
    OriginUrl='http://example.org',
    AllowedReferrers=['app.example.org', 'www.example.org'],
    BlockedIps=['122.33.22.11'],
    EnableCacheSlice=False,
    EnableGeoZoneUS=True,
    EnableGeoZoneEU=True,
    EnableGeoZoneASIA=True,
    EnableGeoZoneSA=True,
    EnableGeoZoneAF=True,
    ZoneSecurityEnabled=True,
    ZoneSecurityIncludeHashRemoteIP=True,
    IgnoreQueryStrings=True,
    MonthlyBandwidthLimit=1073741824,
    AccessControlOriginHeaderExtensions=['jpg', 'png'],
    EnableAccessControlOriginHeader=True,
    BlockRootPathAccess=True,
    EnableWebpVary=True,
    EnableLogging=True,
    DisableCookies=False,
    BudgetRedirectedCountries=['RU', 'BR'],
    BlockedCountries=['RU', 'BR'],
    EnableOriginShield=True,
    OriginShieldZoneCode='FR',
    AddCanonicalHeader=0,
    CacheControlMaxAgeOverride=-1,
    AddHostHeader=True,
    AWSSigningEnabled=True,
    AWSSigningKey='AK_EXAMPLEKEY',
    AWSSigningRegionName='us-east-1',
    AWSSigningSecret='SK_EXAMPLESECRETKET',
    EnableTLS1=True,
    EnableTLS1_1=True
    
)
# From Zone object
zone.update(
    OriginUrl='http://example.org',
    AllowedReferrers=['app.example.org', 'www.example.org'],
    BlockedIps=['122.33.22.11'],
    EnableCacheSlice=False,
    EnableGeoZoneUS=True,
    EnableGeoZoneEU=True,
    EnableGeoZoneASIA=True,
    EnableGeoZoneSA=True,
    EnableGeoZoneAF=True,
    ZoneSecurityEnabled=True,
    ZoneSecurityIncludeHashRemoteIP=True,
    IgnoreQueryStrings=True,
    MonthlyBandwidthLimit=1073741824,
    AccessControlOriginHeaderExtensions=['jpg', 'png'],
    EnableAccessControlOriginHeader=True,
    BlockRootPathAccess=True,
    EnableWebpVary=True,
    EnableLogging=True,
    DisableCookies=False,
    BudgetRedirectedCountries=['RU', 'BR'],
    BlockedCountries=['RU', 'BR'],
    EnableOriginShield=True,
    OriginShieldZoneCode='FR',
    AddCanonicalHeader=0,
    CacheControlMaxAgeOverride=-1,
    AddHostHeader=True,
    AWSSigningEnabled=True,
    AWSSigningKey='AK_EXAMPLEKEY',
    AWSSigningRegionName='us-east-1',
    AWSSigningSecret='SK_EXAMPLESECRETKET',
    EnableTLS1=True,
    EnableTLS1_1=True 
)
```

#### Delete Pull Zone
```python
#From top-level
b.Zone.delete(id='myzone')

#From Zone object
zone.delete()
```

#### Purge File From Pull Zone
```python
# From top-level
b.Purge.create(url='https://myzone.b-cdn.net/css/style.css')

# From Zone Object
zone.purge_file('css/style.css')
```

#### Purge Esntire Pull Zone
```python
# From top-level
b.Zone.purge(
    id='myzone'
)
# From Zone object
zone.purge()
```

#### Add Edge Rule to Pull Zone
```python
b.Zone.create_edge_rule(
    id='myzone',
    Guid="6a2e94df-8aa9-4cd2-b89d-16752102ef9f", # GUID of the edge rule
    ActionParameter1 = "My-Header",
    ActionParameter2 = "HeaderValue",
    Enabled = True,
    Description = "My header value",
    ActionType = 0, # 0 = ForceSSL, 1 = Redirect, 2 = OriginUrl, 3 = OverrideCacheTime, 4 = BlockRequest, 5 = SetResponseHeader, 6 = SetRequestHeader, 7 = ForceDownload, 8 = DisableTokenAuthentication, 9 = EnableTokenAuthentication
    TriggerMatchingType = 1    
    Triggers = []
)
```
## Storage

### Storage Zones

#### Create Storage Zone
```python

# Create a Storage Zone (available regions are listed below)
b.Storage.create(name='example-a', main_storage_region='NY', replica_regions=['DE', 'SG', 'SYD'])
# Returns: <StorageZone: example-a (id: 1234)>
```

##### Storage Regions

- DE - Europe (Falkenstein)
- NY - North America (New York)
- SG - Asia (Singapore)
- SYD - Oceania (Sydney)

#### List Storage Zones
```python
b.Storage.all()
# Returns: [<StorageZone: example-a (id: 1234)>, <StorageZone: example-b (id: 12345)>]
```

#### Delete a Storage Zone
```python
b.Storage.delete(1234)
# Returns: None
```

#### Get a Storage Zone
```python
zone = b.Storage.get(1234)
# Returns: <StorageZone: example-a (id: 1234)>
```

### Storage Files

```python
# Get a Storage Zone
zone = b.StorageZone.get(1234)
# Returns: <StorageZone: example-a (id: 1234)>

# Lists files in the zone
obj_list = zone.all()
# Returns [<StorageFile: index.html>, <StorageFile: base.css>]

# Get a file
obj = zone.get('index.html')
#Returns <StorageFile: index.html>

# Download that File
obj.download()

# Delete a file
zone.delete('index.html')

# Upload a File
zone.upload_file(dest_path='folder/path/error.html', local_path='/home/mj/work/error.html')
# Returns: <StorageFile: error.html>

# Create a file from a string
zone.create_file('base.css', "body {background-color: powderblue;}")
# Returns: <StorageFile: base.css>
```

### Storage JSON Files

```python

# Create a json file
mj = zone.create_json('23.json', {'first_name':'Michael', 'last_name': 'Jordan'})
# Returns <StorageJSONFile: 23.json>

# Get information from file
mj['first_name']
# Returns: 'Michael'
```

# Purge

## Create a Purge
```python
# Purge a zone or file
b.Purge.create(url='https://myzone.b-cdn.net/style.css')
```

# Stats

```python
b.Stats.get(dateFrom='2018-12-01', dateTo='2020-01-01', pullZone='example-zone', serverZoneId='serverZoneID')
```
# Billing

#### Get Billing Summary
```python
b.Billing.get()
```

#### ApplyCode

```python
b.Billing.applycode(couponCode='somecode123')
```
