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


class TestPurgeCreate(unittest.TestCase):
    def setUp(self):
        from bunnyhop.purge import Purge
        self.purge = Purge(API_KEY)

    def test_create_uses_get_method(self):
        with patch("requests.request") as mock_req:
            mock_req.return_value = make_mock_response(json_data={"result": "ok"})
            self.purge.create("https://cdn.example.com/style.css")
        call_kwargs = mock_req.call_args[1]
        self.assertEqual(call_kwargs["method"], "GET")

    def test_create_url_in_query_params(self):
        with patch("requests.request") as mock_req:
            mock_req.return_value = make_mock_response(json_data={"result": "ok"})
            self.purge.create("https://cdn.example.com/style.css")
        params = mock_req.call_args[1].get("params", {})
        self.assertEqual(params.get("url"), "https://cdn.example.com/style.css")

    def test_create_url_not_in_request_body(self):
        with patch("requests.request") as mock_req:
            mock_req.return_value = make_mock_response(json_data={"result": "ok"})
            self.purge.create("https://cdn.example.com/style.css")
        json_body = mock_req.call_args[1].get("json", {})
        self.assertNotIn("url", json_body)

    def test_create_endpoint_is_slash_purge(self):
        with patch("requests.request") as mock_req:
            mock_req.return_value = make_mock_response(json_data={"result": "ok"})
            self.purge.create("https://cdn.example.com/style.css")
        url = mock_req.call_args[1].get("url", "")
        self.assertTrue(url.endswith("/purge"))

    def test_create_returns_dict_on_json_response(self):
        with patch("requests.request") as mock_req:
            mock_req.return_value = make_mock_response(json_data={"ErrorKey": "purge.hostname_not_found"})
            result = self.purge.create("https://cdn.example.com/style.css")
        self.assertIsInstance(result, dict)


class TestZonePurgeFileMethod(unittest.TestCase):
    def setUp(self):
        from bunnyhop.zone import Zone
        self.zone = Zone(API_KEY, Hostnames=[{"Id": 1, "Value": "cdn.example.com", "ForceSSL": False, "IsSystemHostname": False, "HasCertificate": False}])

    def test_purge_file_uses_get_method(self):
        with patch("requests.request") as mock_req:
            mock_req.return_value = make_mock_response(content=b"")
            self.zone.purge_file("styles/main.css")
        call_kwargs = mock_req.call_args[1]
        self.assertEqual(call_kwargs["method"], "GET")

    def test_purge_file_url_in_query_params(self):
        with patch("requests.request") as mock_req:
            mock_req.return_value = make_mock_response(content=b"")
            self.zone.purge_file("styles/main.css")
        params = mock_req.call_args[1].get("params", {})
        self.assertIn("url", params)
        self.assertIn("cdn.example.com", params["url"])
        self.assertIn("styles/main.css", params["url"])

    def test_purge_file_endpoint_is_slash_purge(self):
        with patch("requests.request") as mock_req:
            mock_req.return_value = make_mock_response(content=b"")
            self.zone.purge_file("styles/main.css")
        url = mock_req.call_args[1].get("url", "")
        self.assertTrue(url.endswith("/purge"))


if __name__ == "__main__":
    unittest.main()
