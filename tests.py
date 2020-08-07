import unittest
import json
from unittest.mock import patch, mock_open
from bunnyhop import Bunny
from bunnyhop.storage_zone import StorageObject


class TestBilling(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        self.b = Bunny('api-key')

    @classmethod
    def tearDownClass(self):
        self.b = None

    def test_get(self):
        response_json = json.loads(self.b.Billing.get())
        self.assertEqual(response_json['status_code'], 200)

    def test_apply_code(self):
        response_json = json.loads(self.b.Billing.applycode('123'))
        self.assertEqual(response_json['status_code'], 200)


class TestStats(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        self.b = Bunny('api-key')

    @classmethod
    def tearDownClass(self):
        self.b = None

    def test_get(self):
        response_json = json.loads(self.b.Stats.get(dateFrom='2018-12-01', dateTo='2020-01-01', pullZone='example-zone', serverZoneId='serverZoneID'))
        self.assertEqual(response_json['status_code'], 200)


class TestPurge(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        self.b = Bunny('api-key')

    @classmethod
    def tearDownClass(self):
        self.b = None

    def test_create(self):
        response_json = json.loads(self.b.Purge.create(url='https://myzone.b-cdn.net/style.css'))
        self.assertEqual(response_json['status_code'], 200)


class TestStorageZone(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        self.b = Bunny('api-key')

    @classmethod
    def tearDownClass(self):
        self.b = None

    def test_get(self):
        response = self.b.StorageZone.get(1234)
        self.assertIsInstance(response, StorageObject)


class TestStorageObject(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        self.b = Bunny('api-key')
        self.zone = self.b.StorageZone.get(1234)

    @classmethod
    def tearDownClass(self):
        self.b = None
        self.zone = None
        
    def test_all(self):
        response_json = json.loads(self.zone.all('path'))
        self.assertEqual(response_json['status_code'], 200)

    def test_get(self):
        response_json = json.loads(self.zone.get('path','filename'))
        self.assertEqual(response_json['status_code'], 200)

    def test_delete(self):
        response_json = json.loads(self.zone.delete('path','filename'))
        self.assertEqual(response_json['status_code'], 200)

    def test_upload_file(self):
        response_json = json.loads(self.zone.delete('dest_path','local_path'))
        self.assertEqual(response_json['status_code'], 200)

    def test_create_file(self):
        open_mock = mock_open()
        file_name = 'base.css'
        file_content = "body {background-color: powderblue;}"
        with patch("bunnyhop.storage_zone.open", open_mock, create=True):
            self.zone.create_file(file_name, file_content)
        open_mock.assert_called_with(file_name, "w+")
        open_mock.return_value.write.assert_called_once_with(file_content)

    def test_create_json(self):
        open_mock = mock_open()
        json_name = '23.json'
        json_content = {'first_name':'Michael', 'last_name': 'Jordan'}
        with patch("bunnyhop.storage_zone.open", open_mock, create=True):
            self.zone.create_json(json_name, json_content)
        open_mock.assert_called_with(json_name, "w+")
        open_mock.return_value.write.assert_called_with('}')


class TestStorage(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        self.b = Bunny('api-key')

    @classmethod
    def tearDownClass(self):
        self.b = None

    def test_create(self):
        response_json = json.loads(self.b.Storage.create())
        self.assertEqual(response_json['status_code'], 201)
        response_json = json.loads(self.b.Storage.create(name='example-a', main_storage_region='NY', replica_regions=['DE', 'SG', 'SYD']))
        self.assertEqual(response_json['status_code'], 201)

    def test_all(self):
        response_json = json.loads(self.b.Storage.all())
        self.assertEqual(response_json['status_code'], 200)

    def test_delete(self):
        response_json = json.loads(self.b.Storage.delete(1234))
        self.assertEqual(response_json['status_code'], 201)

    def test_get(self):
        response_json = json.loads(self.b.Storage.get(1234))
        self.assertEqual(response_json['status_code'], 200)


class TestZone(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        self.b = Bunny('api-key')

    @classmethod
    def tearDownClass(self):
        self.b = None

    def test_get(self):
        response_json = json.loads(self.b.Zone.get('myzone'))
        self.assertEqual(response_json['status_code'], 200)

    def test_create(self):
        response_json = json.loads(self.b.Zone.create())
        self.assertEqual(response_json['status_code'], 201)
        response_json = json.loads(self.b.Zone.create(
            Name='myzone',
            Type=0,
            OriginUrl='https://example.org',
            StorageZoneId='storage-zone-id'
            ))
        self.assertEqual(response_json['status_code'], 201)

    def test_list(self):
        response_json = json.loads(self.b.Zone.list())
        self.assertEqual(response_json['status_code'], 200)

    def test_update(self):
        response_json = json.loads(self.b.Zone.update(id=1))
        self.assertEqual(response_json['status_code'], 200)
        response_json = json.loads(self.b.Zone.update(
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
            ))
        self.assertEqual(response_json['status_code'], 200)

    def test_delete(self):
        response_json = json.loads(self.b.Zone.delete(id=1))
        self.assertEqual(response_json['status_code'], 204)

    def test_purge(self):
        response_json = json.loads(self.b.Zone.purge(id=1))
        self.assertEqual(response_json['status_code'], 200) 

    def test_create_edge_rule(self):
        response_json = json.loads(self.b.Zone.create_edge_rule(id=1))
        self.assertEqual(response_json['status_code'], 201)
        response_json = json.loads(self.b.Zone.create_edge_rule(
            id='myzone',
            Guid="6a2e94df-8aa9-4cd2-b89d-16752102ef9f",
            ActionParameter1 = "My-Header",
            ActionParameter2 = "HeaderValue",
            Enabled = True,
            Description = "My header value",
            ActionType = 0,
            TriggerMatchingType = 1,
            Triggers = []
            ))
        self.assertEqual(response_json['status_code'], 201)

if __name__ == '__main__': 
    unittest.main()