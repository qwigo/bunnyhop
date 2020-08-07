import unittest
import json
from unittest.mock import patch
from bunnyhop import Bunny
from bunnyhop.url_settings import bunnycdn_url


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


if __name__ == '__main__': 
    unittest.main()