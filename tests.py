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


if __name__ == '__main__': 
    unittest.main()