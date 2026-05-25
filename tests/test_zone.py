import collections
import collections.abc
import json
import unittest
from unittest.mock import MagicMock, patch

# Python 3.10+ removed collections.Callable; valley 1.5.x still uses it.
if not hasattr(collections, 'Callable'):
    collections.Callable = collections.abc.Callable

from bunnyhop.zone import Zone


API_KEY = "test-api-key"


def make_mock_response(json_data=None, content=b"", status_code=200):
    """Return a mock requests.Response-like object."""
    mock_resp = MagicMock()
    mock_resp.status_code = status_code
    if json_data is not None:
        mock_resp.json.return_value = json_data
    else:
        from json import JSONDecodeError
        mock_resp.json.side_effect = JSONDecodeError("no json", "", 0)
        mock_resp.content = content
    return mock_resp


class TestZoneGet(unittest.TestCase):
    """C3-adjacent / M1: get() with a 404-like (empty/error) response."""

    def test_get_returns_zone_not_found_for_empty_response(self):
        """get() should return 'Zone not found.' (not raise) when response has no Id."""
        zone = Zone(API_KEY)
        with patch("requests.request") as mock_req:
            mock_req.return_value = make_mock_response(json_data={})
            result = zone.get(999)
        # Should not raise; should return sentinel string or None (not a Zone)
        self.assertNotIsInstance(result, Zone)

    def test_get_returns_zone_not_found_for_none_response(self):
        """get() should return 'Zone not found.' when response is not dict-like."""
        zone = Zone(API_KEY)
        with patch("requests.request") as mock_req:
            # Simulate response that is not a dict (bytes content, no JSON)
            mock_req.return_value = make_mock_response(content=b"Not Found")
            result = zone.get(999)
        self.assertEqual(result, "Zone not found.")

    def test_get_returns_zone_for_valid_response(self):
        """get() should return a Zone instance when response has a valid Id."""
        zone = Zone(API_KEY)
        with patch("requests.request") as mock_req:
            mock_req.return_value = make_mock_response(json_data={"Id": 42, "Name": "testzone"})
            result = zone.get(42)
        self.assertIsInstance(result, Zone)
        self.assertEqual(result.Id, 42)


class TestZoneUpdate(unittest.TestCase):
    """M4: update() must not send None values in JSON payload."""

    def test_update_excludes_none_values(self):
        """update() should filter out None parameters before sending to API."""
        zone = Zone(API_KEY)
        captured_calls = []

        def fake_request(**kwargs):
            captured_calls.append(kwargs)
            return make_mock_response(json_data={})

        with patch("requests.request", side_effect=fake_request):
            zone.update(id=1, OriginUrl="https://example.com")

        self.assertEqual(len(captured_calls), 1)
        sent_json = captured_calls[0].get("json", {})
        # OriginUrl should be present
        self.assertIn("OriginUrl", sent_json)
        self.assertEqual(sent_json["OriginUrl"], "https://example.com")
        # None-valued keys must NOT be present
        none_keys = [k for k, v in sent_json.items() if v is None]
        self.assertEqual(none_keys, [], f"None values found in payload: {none_keys}")

    def test_update_sends_only_provided_values(self):
        """update() with multiple explicit values should only send those values."""
        zone = Zone(API_KEY)
        captured_calls = []

        def fake_request(**kwargs):
            captured_calls.append(kwargs)
            return make_mock_response(json_data={})

        with patch("requests.request", side_effect=fake_request):
            zone.update(id=1, OriginUrl="https://example.com", EnableLogging=True)

        sent_json = captured_calls[0].get("json", {})
        self.assertIn("OriginUrl", sent_json)
        self.assertIn("EnableLogging", sent_json)
        # All other params are None and should be absent
        self.assertNotIn("AllowedReferrers", sent_json)
        self.assertNotIn("BlockedIps", sent_json)


class TestZonePurgeFile(unittest.TestCase):
    """M5: purge_file() should raise ValueError when zone has no hostnames."""

    def test_purge_file_raises_when_no_hostnames(self):
        """purge_file() must raise ValueError if Hostnames list is empty."""
        zone = Zone(API_KEY, Hostnames=[])
        with self.assertRaises(ValueError) as ctx:
            zone.purge_file("some/file.css")
        self.assertIn("no hostnames", str(ctx.exception).lower())

    def test_purge_file_works_with_hostname(self):
        """purge_file() should succeed when at least one hostname is present."""
        zone = Zone(API_KEY, Hostnames=[{"Id": 1, "Value": "cdn.example.com"}])
        with patch("requests.request") as mock_req:
            mock_req.return_value = make_mock_response(content=b"")
            result = zone.purge_file("styles/main.css")
        self.assertEqual(result, "Purge Queue was finished.")


class TestZoneAddHostname(unittest.TestCase):
    """M9: add_hostname() must call POST /pullzone/{id}/addHostname."""

    def test_add_hostname_uses_correct_endpoint(self):
        """add_hostname() must POST to /pullzone/{id}/addHostname."""
        zone = Zone(API_KEY, Id=123)
        captured_calls = []

        def fake_request(**kwargs):
            captured_calls.append(kwargs)
            return make_mock_response(content=b"")

        with patch("requests.request", side_effect=fake_request):
            zone.add_hostname("cdn.example.com")

        self.assertEqual(len(captured_calls), 1)
        call = captured_calls[0]
        self.assertEqual(call["method"], "POST")
        self.assertIn("/pullzone/123/addHostname", call["url"])

    def test_add_hostname_does_not_use_old_endpoint(self):
        """add_hostname() must NOT call the old /pullzone/addHostname endpoint."""
        zone = Zone(API_KEY, Id=123)
        captured_calls = []

        def fake_request(**kwargs):
            captured_calls.append(kwargs)
            return make_mock_response(content=b"")

        with patch("requests.request", side_effect=fake_request):
            zone.add_hostname("cdn.example.com")

        url = captured_calls[0]["url"]
        # Old endpoint had no zone id — just /pullzone/addHostname
        self.assertNotRegex(url, r"/pullzone/addHostname$")


class TestZoneDeleteHostname(unittest.TestCase):
    """M9: delete_hostname() must call DELETE /pullzone/{id}/removeHostname."""

    def test_delete_hostname_uses_correct_method_and_endpoint(self):
        """delete_hostname() must DELETE /pullzone/{id}/removeHostname."""
        zone = Zone(API_KEY, Id=456)
        captured_calls = []

        def fake_request(**kwargs):
            captured_calls.append(kwargs)
            return make_mock_response(content=b"")

        with patch("requests.request", side_effect=fake_request):
            zone.delete_hostname("cdn.example.com")

        self.assertEqual(len(captured_calls), 1)
        call = captured_calls[0]
        self.assertEqual(call["method"], "DELETE")
        self.assertIn("/pullzone/456/removeHostname", call["url"])

    def test_delete_hostname_does_not_use_old_endpoint(self):
        """delete_hostname() must NOT call old POST /pullzone/deleteHostname."""
        zone = Zone(API_KEY, Id=456)
        captured_calls = []

        def fake_request(**kwargs):
            captured_calls.append(kwargs)
            return make_mock_response(content=b"")

        with patch("requests.request", side_effect=fake_request):
            zone.delete_hostname("cdn.example.com")

        call = captured_calls[0]
        # Must not be POST
        self.assertNotEqual(call["method"], "POST")
        # Must not hit old path
        self.assertNotIn("deleteHostname", call["url"])


class TestZoneDeleteEdgeRule(unittest.TestCase):
    """m10: delete_edge_rule() must exist and call DELETE /pullzone/{id}/edgerules/{guid}."""

    def test_delete_edge_rule_method_exists(self):
        """Zone must have a delete_edge_rule() method."""
        zone = Zone(API_KEY)
        self.assertTrue(hasattr(zone, "delete_edge_rule"), "Zone.delete_edge_rule does not exist")
        self.assertTrue(callable(zone.delete_edge_rule))

    def test_delete_edge_rule_uses_correct_endpoint(self):
        """delete_edge_rule() must DELETE /pullzone/{id}/edgerules/{guid}."""
        zone = Zone(API_KEY)
        captured_calls = []

        def fake_request(**kwargs):
            captured_calls.append(kwargs)
            return make_mock_response(content=b"")

        with patch("requests.request", side_effect=fake_request):
            zone.delete_edge_rule("some-guid-abc", id=789)

        self.assertEqual(len(captured_calls), 1)
        call = captured_calls[0]
        self.assertEqual(call["method"], "DELETE")
        self.assertIn("/pullzone/789/edgerules/some-guid-abc", call["url"])

    def test_delete_edge_rule_uses_self_id_when_no_id_given(self):
        zone = Zone(API_KEY, Id=789)
        captured_calls = []
        def fake_request(**kwargs):
            captured_calls.append(kwargs)
            return make_mock_response(content=b"")
        with patch("requests.request", side_effect=fake_request):
            result = zone.delete_edge_rule("some-guid-abc")  # no id kwarg
        self.assertEqual(len(captured_calls), 1)
        call = captured_calls[0]
        self.assertEqual(call["method"], "DELETE")
        self.assertIn("/pullzone/789/edgerules/some-guid-abc", call["url"])

    def test_delete_edge_rule_returns_string_on_success(self):
        zone = Zone(API_KEY, Id=789)
        with patch("requests.request") as mock_req:
            mock_req.return_value = make_mock_response(content=b"")
            result = zone.delete_edge_rule("some-guid-abc")
        self.assertIsInstance(result, str)
        self.assertIn("edge rule", result.lower())

    def test_delete_edge_rule_explicit_id_overrides_self_id(self):
        zone = Zone(API_KEY, Id=111)
        captured_calls = []
        def fake_request(**kwargs):
            captured_calls.append(kwargs)
            return make_mock_response(content=b"")
        with patch("requests.request", side_effect=fake_request):
            zone.delete_edge_rule("some-guid-abc", id=999)
        call = captured_calls[0]
        self.assertIn("/pullzone/999/edgerules/some-guid-abc", call["url"])
        self.assertNotIn("/pullzone/111/", call["url"])


class TestZoneCreateEdgeRule(unittest.TestCase):
    """m5: create_edge_rule() must return a str, not bytes."""

    def test_create_edge_rule_returns_string_on_success(self):
        """create_edge_rule() must return a string (not bytes) on success."""
        zone = Zone(API_KEY)
        with patch("requests.request") as mock_req:
            mock_req.return_value = make_mock_response(content=b"")
            result = zone.create_edge_rule(id=1, Guid="guid-123", ActionType=0)
        self.assertIsInstance(result, str)
        self.assertIn("edge rule", result.lower())

    def test_create_edge_rule_uses_self_id_when_no_id_given(self):
        zone = Zone(API_KEY, Id=42)
        captured_calls = []
        def fake_request(**kwargs):
            captured_calls.append(kwargs)
            return make_mock_response(content=b"")
        with patch("requests.request", side_effect=fake_request):
            zone.create_edge_rule(Guid="guid-abc", ActionType=0)
        call = captured_calls[0]
        self.assertEqual(call["method"], "POST")
        self.assertIn("/pullzone/42/edgerules/addOrUpdate", call["url"])


class TestZoneLoadFreeCertificate(unittest.TestCase):
    def test_load_free_certificate_uses_get_and_correct_path(self):
        zone = Zone(API_KEY)
        captured = []
        def fake_req(**kwargs): captured.append(kwargs); return make_mock_response(content=b"")
        with patch("requests.request", side_effect=fake_req):
            zone.load_free_certificate("cdn.example.com")
        self.assertEqual(captured[0]["method"], "GET")
        self.assertIn("/pullzone/loadFreeCertificate", captured[0]["url"])

    def test_load_free_certificate_sends_hostname_as_query_param(self):
        zone = Zone(API_KEY)
        captured = []
        def fake_req(**kwargs): captured.append(kwargs); return make_mock_response(content=b"")
        with patch("requests.request", side_effect=fake_req):
            zone.load_free_certificate("cdn.example.com")
        self.assertEqual(captured[0]["params"]["hostname"], "cdn.example.com")

    def test_load_free_certificate_returns_string_on_success(self):
        zone = Zone(API_KEY)
        with patch("requests.request") as m:
            m.return_value = make_mock_response(content=b"")
            result = zone.load_free_certificate("cdn.example.com")
        self.assertIsInstance(result, str)

    def test_load_free_certificate_returns_error_dict_on_failure(self):
        zone = Zone(API_KEY)
        err = {"ErrorKey": "validation.error", "Message": "Hostname not found"}
        with patch("requests.request") as m:
            m.return_value = make_mock_response(json_data=err)
            result = zone.load_free_certificate("cdn.example.com")
        self.assertEqual(result, err)


class TestZoneAddCertificate(unittest.TestCase):
    def test_add_certificate_uses_post_and_correct_path(self):
        zone = Zone(API_KEY, Id=123)
        captured = []
        def fake_req(**kwargs): captured.append(kwargs); return make_mock_response(content=b"")
        with patch("requests.request", side_effect=fake_req):
            zone.add_certificate("cdn.example.com", "CERT", "KEY")
        self.assertEqual(captured[0]["method"], "POST")
        self.assertIn("/pullzone/123/addCertificate", captured[0]["url"])

    def test_add_certificate_sends_correct_json_body(self):
        zone = Zone(API_KEY, Id=123)
        captured = []
        def fake_req(**kwargs): captured.append(kwargs); return make_mock_response(content=b"")
        with patch("requests.request", side_effect=fake_req):
            zone.add_certificate("cdn.example.com", "CERT_DATA", "KEY_DATA")
        self.assertEqual(captured[0]["json"]["Hostname"], "cdn.example.com")
        self.assertEqual(captured[0]["json"]["Certificate"], "CERT_DATA")
        self.assertEqual(captured[0]["json"]["CertificateKey"], "KEY_DATA")

    def test_add_certificate_returns_string_on_success(self):
        zone = Zone(API_KEY, Id=123)
        with patch("requests.request") as m:
            m.return_value = make_mock_response(content=b"")
            result = zone.add_certificate("cdn.example.com", "CERT", "KEY")
        self.assertIsInstance(result, str)

    def test_add_certificate_returns_error_dict_on_failure(self):
        zone = Zone(API_KEY, Id=123)
        err = {"ErrorKey": "error", "Message": "Invalid cert"}
        with patch("requests.request") as m:
            m.return_value = make_mock_response(json_data=err)
            result = zone.add_certificate("cdn.example.com", "CERT", "KEY")
        self.assertEqual(result, err)


class TestZoneRemoveCertificate(unittest.TestCase):
    def test_remove_certificate_uses_delete_and_correct_path(self):
        zone = Zone(API_KEY, Id=456)
        captured = []
        def fake_req(**kwargs): captured.append(kwargs); return make_mock_response(content=b"")
        with patch("requests.request", side_effect=fake_req):
            zone.remove_certificate("cdn.example.com")
        self.assertEqual(captured[0]["method"], "DELETE")
        self.assertIn("/pullzone/456/removeCertificate", captured[0]["url"])

    def test_remove_certificate_sends_hostname_in_body(self):
        zone = Zone(API_KEY, Id=456)
        captured = []
        def fake_req(**kwargs): captured.append(kwargs); return make_mock_response(content=b"")
        with patch("requests.request", side_effect=fake_req):
            zone.remove_certificate("cdn.example.com")
        self.assertEqual(captured[0]["json"]["Hostname"], "cdn.example.com")

    def test_remove_certificate_returns_string_on_success(self):
        zone = Zone(API_KEY, Id=456)
        with patch("requests.request") as m:
            m.return_value = make_mock_response(content=b"")
            result = zone.remove_certificate("cdn.example.com")
        self.assertIsInstance(result, str)


class TestZoneSetForceSSL(unittest.TestCase):
    def test_set_force_ssl_uses_post_and_correct_path(self):
        zone = Zone(API_KEY, Id=789)
        captured = []
        def fake_req(**kwargs): captured.append(kwargs); return make_mock_response(content=b"")
        with patch("requests.request", side_effect=fake_req):
            zone.set_force_ssl("cdn.example.com", True)
        self.assertEqual(captured[0]["method"], "POST")
        self.assertIn("/pullzone/789/setForceSSL", captured[0]["url"])

    def test_set_force_ssl_sends_correct_json_body(self):
        zone = Zone(API_KEY, Id=789)
        captured = []
        def fake_req(**kwargs): captured.append(kwargs); return make_mock_response(content=b"")
        with patch("requests.request", side_effect=fake_req):
            zone.set_force_ssl("cdn.example.com", True)
        self.assertEqual(captured[0]["json"]["Hostname"], "cdn.example.com")
        self.assertTrue(captured[0]["json"]["ForceSSL"])

    def test_set_force_ssl_returns_string_on_success(self):
        zone = Zone(API_KEY, Id=789)
        with patch("requests.request") as m:
            m.return_value = make_mock_response(content=b"")
            result = zone.set_force_ssl("cdn.example.com", True)
        self.assertIsInstance(result, str)
        self.assertIn("ssl", result.lower())

    def test_set_force_ssl_returns_error_dict_on_failure(self):
        zone = Zone(API_KEY, Id=789)
        err = {"ErrorKey": "error", "Message": "Hostname not found"}
        with patch("requests.request") as m:
            m.return_value = make_mock_response(json_data=err)
            result = zone.set_force_ssl("cdn.example.com", False)
        self.assertEqual(result, err)


if __name__ == "__main__":
    unittest.main()
