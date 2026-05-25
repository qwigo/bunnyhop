import collections, collections.abc, unittest
from unittest.mock import MagicMock, patch
from json import JSONDecodeError

if not hasattr(collections, 'Callable'):
    collections.Callable = collections.abc.Callable

API_KEY = "test-api-key"

def make_mock_response(json_data=None, content=b"", status_code=200):
    mock_resp = MagicMock()
    mock_resp.status_code = status_code
    if json_data is not None:
        mock_resp.json.return_value = json_data
    else:
        mock_resp.json.side_effect = JSONDecodeError("no json", "", 0)
        mock_resp.content = content
    return mock_resp


DNS_ZONE_DATA = {
    "Id": 1, "Domain": "example.com", "Records": [],
    "DateModified": "2024-01-01T00:00:00Z", "DateCreated": "2024-01-01T00:00:00Z",
    "NameserversDetected": False, "CustomNameserversEnabled": False,
    "Nameserver1": "ns1.bunny.net", "Nameserver2": "ns2.bunny.net",
    "SoaEmail": "admin@example.com", "DnsSecEnabled": False,
    "LoggingEnabled": False, "LoggingIPAnonymizationEnabled": False, "LogAnonymizationType": 0,
}
DNS_ZONE_LIST_RESPONSE = {"Items": [DNS_ZONE_DATA, {**DNS_ZONE_DATA, "Id": 2, "Domain": "other.com"}], "TotalItems": 2, "CurrentPage": 1, "HasMoreItems": False}
DNS_RECORD_DATA = {"Id": 456, "Type": 0, "Ttl": 300, "Value": "1.2.3.4", "Name": "www", "Weight": 0, "Priority": 0, "Port": 0, "Flags": 0, "Tag": "", "Accelerated": False, "AcceleratedPullZoneId": 0, "LinkName": "", "MonitorType": 0, "GeolocationLat": 0.0, "GeolocationLong": 0.0, "EnvironmentTagId": 0, "Comment": ""}


class TestDNSList(unittest.TestCase):

    def setUp(self):
        from bunnyhop.dns import DNS, DNSZone, DNSRecord
        self.DNS = DNS
        self.DNSZone = DNSZone
        self.DNSRecord = DNSRecord

    @patch('requests.request')
    def test_list_returns_list_of_dns_zones(self, mock_request):
        mock_request.return_value = make_mock_response(json_data=DNS_ZONE_LIST_RESPONSE)
        dns = self.DNS(API_KEY)
        result = dns.list()
        self.assertIsInstance(result, list)
        self.assertEqual(len(result), 2)
        self.assertIsInstance(result[0], self.DNSZone)

    @patch('requests.request')
    def test_list_uses_get_method_and_correct_url(self, mock_request):
        mock_request.return_value = make_mock_response(json_data=DNS_ZONE_LIST_RESPONSE)
        dns = self.DNS(API_KEY)
        dns.list()
        call_kwargs = mock_request.call_args
        self.assertEqual(call_kwargs[1]['method'], 'GET')
        self.assertIn('/dnszone', call_kwargs[1]['url'])

    @patch('requests.request')
    def test_list_passes_pagination_params(self, mock_request):
        mock_request.return_value = make_mock_response(json_data=DNS_ZONE_LIST_RESPONSE)
        dns = self.DNS(API_KEY)
        dns.list(page=2, per_page=50)
        call_kwargs = mock_request.call_args
        params = call_kwargs[1]['params']
        self.assertEqual(params['page'], 2)
        self.assertEqual(params['perPage'], 50)

    @patch('requests.request')
    def test_list_passes_search_param(self, mock_request):
        mock_request.return_value = make_mock_response(json_data=DNS_ZONE_LIST_RESPONSE)
        dns = self.DNS(API_KEY)
        dns.list(search="example")
        call_kwargs = mock_request.call_args
        params = call_kwargs[1]['params']
        self.assertEqual(params['search'], 'example')

    @patch('requests.request')
    def test_list_omits_none_search_param(self, mock_request):
        mock_request.return_value = make_mock_response(json_data=DNS_ZONE_LIST_RESPONSE)
        dns = self.DNS(API_KEY)
        dns.list()
        call_kwargs = mock_request.call_args
        params = call_kwargs[1]['params']
        self.assertNotIn('search', params)


class TestDNSGet(unittest.TestCase):

    def setUp(self):
        from bunnyhop.dns import DNS, DNSZone, DNSRecord
        self.DNS = DNS
        self.DNSZone = DNSZone
        self.DNSRecord = DNSRecord

    @patch('requests.request')
    def test_get_returns_dns_zone_for_valid_id(self, mock_request):
        mock_request.return_value = make_mock_response(json_data=DNS_ZONE_DATA)
        dns = self.DNS(API_KEY)
        result = dns.get(1)
        self.assertIsInstance(result, self.DNSZone)
        self.assertEqual(result.Id, 1)
        self.assertEqual(result.Domain, "example.com")

    @patch('requests.request')
    def test_get_uses_correct_url(self, mock_request):
        mock_request.return_value = make_mock_response(json_data=DNS_ZONE_DATA)
        dns = self.DNS(API_KEY)
        dns.get(1)
        call_kwargs = mock_request.call_args
        self.assertIn('/dnszone/1', call_kwargs[1]['url'])

    @patch('requests.request')
    def test_get_returns_raw_when_no_id(self, mock_request):
        mock_request.return_value = make_mock_response(json_data={})
        dns = self.DNS(API_KEY)
        result = dns.get(999)
        self.assertNotIsInstance(result, self.DNSZone)


class TestDNSCreate(unittest.TestCase):

    def setUp(self):
        from bunnyhop.dns import DNS, DNSZone, DNSRecord
        self.DNS = DNS
        self.DNSZone = DNSZone
        self.DNSRecord = DNSRecord

    @patch('requests.request')
    def test_create_returns_dns_zone(self, mock_request):
        mock_request.return_value = make_mock_response(json_data=DNS_ZONE_DATA)
        dns = self.DNS(API_KEY)
        result = dns.create("example.com")
        self.assertIsInstance(result, self.DNSZone)

    @patch('requests.request')
    def test_create_posts_to_correct_endpoint(self, mock_request):
        mock_request.return_value = make_mock_response(json_data=DNS_ZONE_DATA)
        dns = self.DNS(API_KEY)
        dns.create("newzone.com")
        call_kwargs = mock_request.call_args
        self.assertEqual(call_kwargs[1]['method'], 'POST')
        self.assertTrue(call_kwargs[1]['url'].endswith('/dnszone'))

    @patch('requests.request')
    def test_create_sends_domain_in_body(self, mock_request):
        mock_request.return_value = make_mock_response(json_data=DNS_ZONE_DATA)
        dns = self.DNS(API_KEY)
        dns.create("newzone.com")
        call_kwargs = mock_request.call_args
        self.assertEqual(call_kwargs[1]['json']['Domain'], 'newzone.com')


class TestDNSUpdate(unittest.TestCase):

    def setUp(self):
        from bunnyhop.dns import DNS, DNSZone, DNSRecord
        self.DNS = DNS
        self.DNSZone = DNSZone
        self.DNSRecord = DNSRecord

    @patch('requests.request')
    def test_update_returns_success_string(self, mock_request):
        mock_request.return_value = make_mock_response(content=b"")
        dns = self.DNS(API_KEY)
        result = dns.update(42, CustomNameserversEnabled=True)
        self.assertIsInstance(result, str)

    @patch('requests.request')
    def test_update_posts_to_correct_url(self, mock_request):
        mock_request.return_value = make_mock_response(content=b"")
        dns = self.DNS(API_KEY)
        dns.update(42, CustomNameserversEnabled=True)
        call_kwargs = mock_request.call_args
        self.assertIn('/dnszone/42', call_kwargs[1]['url'])

    @patch('requests.request')
    def test_update_sends_only_provided_kwargs(self, mock_request):
        mock_request.return_value = make_mock_response(content=b"")
        dns = self.DNS(API_KEY)
        dns.update(42, CustomNameserversEnabled=True)
        call_kwargs = mock_request.call_args
        json_body = call_kwargs[1]['json']
        self.assertIn('CustomNameserversEnabled', json_body)
        self.assertTrue(json_body['CustomNameserversEnabled'])
        # No None keys
        for v in json_body.values():
            self.assertIsNotNone(v)


class TestDNSDelete(unittest.TestCase):

    def setUp(self):
        from bunnyhop.dns import DNS, DNSZone, DNSRecord
        self.DNS = DNS
        self.DNSZone = DNSZone
        self.DNSRecord = DNSRecord

    @patch('requests.request')
    def test_delete_returns_success_string(self, mock_request):
        mock_request.return_value = make_mock_response(content=b"")
        dns = self.DNS(API_KEY)
        result = dns.delete(1)
        self.assertIsInstance(result, str)

    @patch('requests.request')
    def test_delete_uses_delete_method_and_correct_url(self, mock_request):
        mock_request.return_value = make_mock_response(content=b"")
        dns = self.DNS(API_KEY)
        dns.delete(1)
        call_kwargs = mock_request.call_args
        self.assertEqual(call_kwargs[1]['method'], 'DELETE')
        self.assertIn('/dnszone/1', call_kwargs[1]['url'])


class TestDNSSec(unittest.TestCase):

    def setUp(self):
        from bunnyhop.dns import DNS, DNSZone, DNSRecord
        self.DNS = DNS
        self.DNSZone = DNSZone
        self.DNSRecord = DNSRecord

    @patch('requests.request')
    def test_enable_dnssec_posts_to_correct_url(self, mock_request):
        mock_request.return_value = make_mock_response(content=b"")
        dns = self.DNS(API_KEY)
        dns.enable_dnssec(42)
        call_kwargs = mock_request.call_args
        self.assertEqual(call_kwargs[1]['method'], 'POST')
        self.assertIn('/dnszone/42/dnssec', call_kwargs[1]['url'])

    @patch('requests.request')
    def test_enable_dnssec_returns_string(self, mock_request):
        mock_request.return_value = make_mock_response(content=b"")
        dns = self.DNS(API_KEY)
        result = dns.enable_dnssec(42)
        self.assertIsInstance(result, str)

    @patch('requests.request')
    def test_disable_dnssec_deletes_correct_url(self, mock_request):
        mock_request.return_value = make_mock_response(content=b"")
        dns = self.DNS(API_KEY)
        dns.disable_dnssec(42)
        call_kwargs = mock_request.call_args
        self.assertEqual(call_kwargs[1]['method'], 'DELETE')
        self.assertIn('/dnszone/42/dnssec', call_kwargs[1]['url'])

    @patch('requests.request')
    def test_disable_dnssec_returns_string(self, mock_request):
        mock_request.return_value = make_mock_response(content=b"")
        dns = self.DNS(API_KEY)
        result = dns.disable_dnssec(42)
        self.assertIsInstance(result, str)


class TestDNSCreateRecord(unittest.TestCase):

    def setUp(self):
        from bunnyhop.dns import DNS, DNSZone, DNSRecord
        self.DNS = DNS
        self.DNSZone = DNSZone
        self.DNSRecord = DNSRecord

    @patch('requests.request')
    def test_create_record_returns_dns_record(self, mock_request):
        mock_request.return_value = make_mock_response(json_data=DNS_RECORD_DATA)
        dns = self.DNS(API_KEY)
        result = dns.create_record(123, Type=0, Name="www", Value="1.2.3.4", Ttl=300)
        self.assertIsInstance(result, self.DNSRecord)
        self.assertEqual(result.Id, 456)

    @patch('requests.request')
    def test_create_record_uses_put_method_and_correct_url(self, mock_request):
        mock_request.return_value = make_mock_response(json_data=DNS_RECORD_DATA)
        dns = self.DNS(API_KEY)
        dns.create_record(123, Type=0, Name="www", Value="1.2.3.4", Ttl=300)
        call_kwargs = mock_request.call_args
        self.assertEqual(call_kwargs[1]['method'], 'PUT')
        self.assertIn('/dnszone/123/records', call_kwargs[1]['url'])

    @patch('requests.request')
    def test_create_record_sends_required_fields_in_body(self, mock_request):
        mock_request.return_value = make_mock_response(json_data=DNS_RECORD_DATA)
        dns = self.DNS(API_KEY)
        dns.create_record(123, Type=0, Name="www", Value="1.2.3.4", Ttl=300)
        call_kwargs = mock_request.call_args
        json_body = call_kwargs[1]['json']
        self.assertIn('Type', json_body)
        self.assertIn('Name', json_body)
        self.assertIn('Value', json_body)
        self.assertIn('Ttl', json_body)

    @patch('requests.request')
    def test_create_record_forwards_optional_kwargs(self, mock_request):
        mock_request.return_value = make_mock_response(json_data=DNS_RECORD_DATA)
        dns = self.DNS(API_KEY)
        dns.create_record(123, Type=0, Name="www", Value="1.2.3.4", Ttl=300, Priority=10)
        call_kwargs = mock_request.call_args
        json_body = call_kwargs[1]['json']
        self.assertEqual(json_body['Priority'], 10)


class TestDNSUpdateRecord(unittest.TestCase):

    def setUp(self):
        from bunnyhop.dns import DNS, DNSZone, DNSRecord
        self.DNS = DNS
        self.DNSZone = DNSZone
        self.DNSRecord = DNSRecord

    @patch('requests.request')
    def test_update_record_posts_to_correct_url(self, mock_request):
        mock_request.return_value = make_mock_response(content=b"")
        dns = self.DNS(API_KEY)
        dns.update_record(123, 456, Ttl=600)
        call_kwargs = mock_request.call_args
        self.assertIn('/dnszone/123/records/456', call_kwargs[1]['url'])

    @patch('requests.request')
    def test_update_record_returns_string(self, mock_request):
        mock_request.return_value = make_mock_response(content=b"")
        dns = self.DNS(API_KEY)
        result = dns.update_record(123, 456, Ttl=600)
        self.assertIsInstance(result, str)

    @patch('requests.request')
    def test_update_record_sends_kwargs_in_body(self, mock_request):
        mock_request.return_value = make_mock_response(content=b"")
        dns = self.DNS(API_KEY)
        dns.update_record(123, 456, Ttl=600)
        call_kwargs = mock_request.call_args
        json_body = call_kwargs[1]['json']
        self.assertEqual(json_body['Ttl'], 600)


class TestDNSDeleteRecord(unittest.TestCase):

    def setUp(self):
        from bunnyhop.dns import DNS, DNSZone, DNSRecord
        self.DNS = DNS
        self.DNSZone = DNSZone
        self.DNSRecord = DNSRecord

    @patch('requests.request')
    def test_delete_record_uses_delete_method_and_correct_url(self, mock_request):
        mock_request.return_value = make_mock_response(content=b"")
        dns = self.DNS(API_KEY)
        dns.delete_record(123, 456)
        call_kwargs = mock_request.call_args
        self.assertEqual(call_kwargs[1]['method'], 'DELETE')
        self.assertIn('/dnszone/123/records/456', call_kwargs[1]['url'])

    @patch('requests.request')
    def test_delete_record_returns_string(self, mock_request):
        mock_request.return_value = make_mock_response(content=b"")
        dns = self.DNS(API_KEY)
        result = dns.delete_record(123, 456)
        self.assertIsInstance(result, str)


class TestDNSZoneModel(unittest.TestCase):

    def setUp(self):
        from bunnyhop.dns import DNS, DNSZone, DNSRecord
        self.DNS = DNS
        self.DNSZone = DNSZone
        self.DNSRecord = DNSRecord

    def test_dns_zone_str(self):
        zone = self.DNSZone(API_KEY, **DNS_ZONE_DATA)
        self.assertEqual(str(zone), "example.com")

    def test_dns_zone_dns_records_property(self):
        zone_data = {**DNS_ZONE_DATA, "Records": [DNS_RECORD_DATA]}
        zone = self.DNSZone(API_KEY, **zone_data)
        records = zone.dns_records
        self.assertEqual(len(records), 1)
        self.assertIsInstance(records[0], self.DNSRecord)

    def test_dns_record_str(self):
        record = self.DNSRecord(API_KEY, **DNS_RECORD_DATA)
        self.assertIn("www", str(record))


class TestBunnyFacadeDNS(unittest.TestCase):

    def setUp(self):
        from bunnyhop.dns import DNS
        self.DNS = DNS

    def test_bunny_facade_has_dns_attribute(self):
        from bunnyhop.core import Bunny
        bunny = Bunny(API_KEY)
        self.assertTrue(hasattr(bunny, 'DNS'))

    def test_bunny_facade_dns_is_dns_instance(self):
        from bunnyhop.core import Bunny
        bunny = Bunny(API_KEY)
        self.assertIsInstance(bunny.DNS, self.DNS)


if __name__ == '__main__':
    unittest.main()
