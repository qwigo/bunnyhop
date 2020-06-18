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

## Storage

### Storage Zones

```python

# Create a Storage Zone (available regions are listed below)
b.Storage.create(name='example-a', main_storage_region='NY', replica_regions=['DE', 'SG', 'SYD'])
# Returns: <StorageZone: example-a (id: 1234)>

# List Storage Zones
b.Storage.all()
# Returns: [<StorageZone: example-a (id: 1234)>, <StorageZone: example-b (id: 12345)>]

# Delete a Storage Zone
b.Storage.delete(1234)
# Returns: None

# Get a Storage Zone
zone = b.Storage.get(1234)
# Returns: <StorageZone: example-a (id: 1234)>

```

#### Storage Regions

- DE - Europe (Falkenstein)
- NY - North America (New York)
- SG - Asia (Singapore)
- SYD - Oceania (Sydney)

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