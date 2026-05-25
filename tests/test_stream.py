import collections
import collections.abc
import json
import unittest
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


LIBRARY_DATA = {
    "Id": 1, "Name": "My Library", "VideoCount": 5, "TrafficUsage": 1024,
    "StorageUsage": 2048, "DateCreated": "2024-01-01T00:00:00Z",
    "ApiKey": "", "ReadOnlyApiKey": "ro-key", "ReplicationRegions": ["DE"],
    "AllowedReferrers": [], "BlockedReferrers": [], "BlockNoneReferrer": False,
    "EnableTokenAuthentication": False, "EnableTokenIPVerification": False,
    "PlayerKeyColor": "#ffffff", "CustomHTML": "",
    "WatermarkPositionLeft": 0, "WatermarkPositionTop": 0,
    "WatermarkWidth": 0, "WatermarkHeight": 0,
    "EnableMP4Fallback": False, "KeepOriginalFiles": False,
    "AllowDirectPlay": False, "EnableDRM": False,
    "EnableTranscribing": False, "TranscribingLanguage": "en",
    "StorageZoneId": 10, "PullZoneId": 20,
}

LIST_RESPONSE = {
    "totalItems": 1,
    "currentPage": 1,
    "itemsPerPage": 100,
    "items": [LIBRARY_DATA],
}


class TestStreamList(unittest.TestCase):

    def setUp(self):
        from bunnyhop.stream import Stream, StreamLibrary
        self.StreamLibrary = StreamLibrary
        self.stream = Stream(API_KEY)

    @patch("requests.request")
    def test_list_returns_list_of_stream_libraries(self, mock_request):
        mock_request.return_value = make_mock_response(json_data=LIST_RESPONSE)
        result = self.stream.list()
        self.assertIsInstance(result[0], self.StreamLibrary)
        self.assertEqual(result[0].Name, "My Library")

    @patch("requests.request")
    def test_list_calls_get_on_correct_url(self, mock_request):
        mock_request.return_value = make_mock_response(json_data=LIST_RESPONSE)
        self.stream.list()
        call_kwargs = mock_request.call_args
        self.assertEqual(call_kwargs[1]["method"], "GET")
        self.assertIn("video.bunnycdn.com/videolibrary", call_kwargs[1]["url"])

    @patch("requests.request")
    def test_list_passes_page_and_per_page(self, mock_request):
        mock_request.return_value = make_mock_response(json_data=LIST_RESPONSE)
        self.stream.list(page=2, per_page=50)
        call_kwargs = mock_request.call_args
        params = call_kwargs[1]["params"]
        self.assertEqual(params["page"], 2)
        self.assertEqual(params["perPage"], 50)

    @patch("requests.request")
    def test_list_passes_search_param(self, mock_request):
        mock_request.return_value = make_mock_response(json_data=LIST_RESPONSE)
        self.stream.list(search="test")
        call_kwargs = mock_request.call_args
        params = call_kwargs[1]["params"]
        self.assertEqual(params["search"], "test")

    @patch("requests.request")
    def test_list_returns_empty_list_on_empty_items(self, mock_request):
        empty_response = {
            "totalItems": 0, "currentPage": 1, "itemsPerPage": 100, "items": []
        }
        mock_request.return_value = make_mock_response(json_data=empty_response)
        result = self.stream.list()
        self.assertEqual(result, [])


class TestStreamGet(unittest.TestCase):

    def setUp(self):
        from bunnyhop.stream import Stream, StreamLibrary
        self.StreamLibrary = StreamLibrary
        self.stream = Stream(API_KEY)

    @patch("requests.request")
    def test_get_returns_stream_library_instance(self, mock_request):
        mock_request.return_value = make_mock_response(json_data=LIBRARY_DATA)
        result = self.stream.get(1)
        self.assertIsInstance(result, self.StreamLibrary)
        self.assertEqual(result.Id, 1)

    @patch("requests.request")
    def test_get_calls_correct_url(self, mock_request):
        mock_request.return_value = make_mock_response(json_data=LIBRARY_DATA)
        self.stream.get(1)
        call_kwargs = mock_request.call_args
        self.assertIn("/videolibrary/1", call_kwargs[1]["url"])

    @patch("requests.request")
    def test_get_uses_http_get(self, mock_request):
        mock_request.return_value = make_mock_response(json_data=LIBRARY_DATA)
        self.stream.get(1)
        call_kwargs = mock_request.call_args
        self.assertEqual(call_kwargs[1]["method"], "GET")


class TestStreamCreate(unittest.TestCase):

    def setUp(self):
        from bunnyhop.stream import Stream, StreamLibrary
        self.StreamLibrary = StreamLibrary
        self.stream = Stream(API_KEY)

    @patch("requests.request")
    def test_create_returns_stream_library_instance(self, mock_request):
        mock_request.return_value = make_mock_response(json_data=LIBRARY_DATA)
        result = self.stream.create("My Library")
        self.assertIsInstance(result, self.StreamLibrary)

    @patch("requests.request")
    def test_create_calls_post_on_videolibrary(self, mock_request):
        mock_request.return_value = make_mock_response(json_data=LIBRARY_DATA)
        self.stream.create("My Library")
        call_kwargs = mock_request.call_args
        self.assertEqual(call_kwargs[1]["method"], "POST")
        self.assertTrue(call_kwargs[1]["url"].endswith("/videolibrary"))

    @patch("requests.request")
    def test_create_sends_name_in_body(self, mock_request):
        mock_request.return_value = make_mock_response(json_data=LIBRARY_DATA)
        self.stream.create("My Library")
        call_kwargs = mock_request.call_args
        self.assertEqual(call_kwargs[1]["json"]["Name"], "My Library")

    @patch("requests.request")
    def test_create_sends_replication_regions_when_given(self, mock_request):
        mock_request.return_value = make_mock_response(json_data=LIBRARY_DATA)
        self.stream.create("My Library", replication_regions=["DE", "NY"])
        call_kwargs = mock_request.call_args
        self.assertEqual(call_kwargs[1]["json"]["ReplicationRegions"], ["DE", "NY"])

    @patch("requests.request")
    def test_create_raises_value_error_on_failure(self, mock_request):
        mock_request.return_value = make_mock_response(json_data={"message": "error"})
        with self.assertRaises(ValueError):
            self.stream.create("My Library")


class TestStreamUpdate(unittest.TestCase):

    def setUp(self):
        from bunnyhop.stream import Stream
        self.stream = Stream(API_KEY)

    @patch("requests.request")
    def test_update_calls_post_on_correct_url(self, mock_request):
        mock_request.return_value = make_mock_response(json_data={})
        self.stream.update(1, Name="New")
        call_kwargs = mock_request.call_args
        self.assertEqual(call_kwargs[1]["method"], "POST")
        self.assertIn("/videolibrary/1", call_kwargs[1]["url"])

    @patch("requests.request")
    def test_update_excludes_none_values_from_body(self, mock_request):
        mock_request.return_value = make_mock_response(json_data={})
        self.stream.update(1, Name="New", PlayerKeyColor=None)
        call_kwargs = mock_request.call_args
        body = call_kwargs[1]["json"]
        self.assertIn("Name", body)
        self.assertNotIn("PlayerKeyColor", body)

    @patch("requests.request")
    def test_update_returns_success_string_on_bytes_response(self, mock_request):
        mock_request.return_value = make_mock_response(json_data=None, content=b"")
        result = self.stream.update(1, Name="New")
        self.assertIsInstance(result, str)


class TestStreamDelete(unittest.TestCase):

    def setUp(self):
        from bunnyhop.stream import Stream
        self.stream = Stream(API_KEY)

    @patch("requests.request")
    def test_delete_calls_delete_on_correct_url(self, mock_request):
        mock_request.return_value = make_mock_response(json_data=None, content=b"")
        self.stream.delete(1)
        call_kwargs = mock_request.call_args
        self.assertEqual(call_kwargs[1]["method"], "DELETE")
        self.assertIn("/videolibrary/1", call_kwargs[1]["url"])

    @patch("requests.request")
    def test_delete_returns_success_string_on_bytes_response(self, mock_request):
        mock_request.return_value = make_mock_response(json_data=None, content=b"")
        result = self.stream.delete(1)
        self.assertIsInstance(result, str)


class TestStreamAddAllowedReferrer(unittest.TestCase):

    def setUp(self):
        from bunnyhop.stream import Stream
        self.stream = Stream(API_KEY)

    @patch("requests.request")
    def test_add_allowed_referrer_makes_two_calls(self, mock_request):
        mock_request.side_effect = [
            make_mock_response(json_data=LIBRARY_DATA),
            make_mock_response(json_data={}),
        ]
        self.stream.add_allowed_referrer(1, "example.com")
        self.assertEqual(mock_request.call_count, 2)

    @patch("requests.request")
    def test_add_allowed_referrer_sends_updated_list(self, mock_request):
        mock_request.side_effect = [
            make_mock_response(json_data=LIBRARY_DATA),
            make_mock_response(json_data={}),
        ]
        self.stream.add_allowed_referrer(1, "example.com")
        # second call is the POST update
        post_call_kwargs = mock_request.call_args_list[1]
        body = post_call_kwargs[1]["json"]
        self.assertEqual(body["AllowedReferrers"], ["example.com"])

    @patch("requests.request")
    def test_add_allowed_referrer_deduplicates(self, mock_request):
        library_with_referrer = dict(LIBRARY_DATA, AllowedReferrers=["example.com"])
        mock_request.side_effect = [
            make_mock_response(json_data=library_with_referrer),
            make_mock_response(json_data={}),
        ]
        self.stream.add_allowed_referrer(1, "example.com")
        post_call_kwargs = mock_request.call_args_list[1]
        body = post_call_kwargs[1]["json"]
        self.assertEqual(len(body["AllowedReferrers"]), 1)


class TestStreamRemoveAllowedReferrer(unittest.TestCase):

    def setUp(self):
        from bunnyhop.stream import Stream
        self.stream = Stream(API_KEY)

    @patch("requests.request")
    def test_remove_allowed_referrer_sends_filtered_list(self, mock_request):
        library_with_referrers = dict(LIBRARY_DATA, AllowedReferrers=["a.com", "b.com"])
        mock_request.side_effect = [
            make_mock_response(json_data=library_with_referrers),
            make_mock_response(json_data={}),
        ]
        self.stream.remove_allowed_referrer(1, "a.com")
        post_call_kwargs = mock_request.call_args_list[1]
        body = post_call_kwargs[1]["json"]
        self.assertEqual(body["AllowedReferrers"], ["b.com"])

    @patch("requests.request")
    def test_remove_allowed_referrer_no_op_if_not_present(self, mock_request):
        mock_request.side_effect = [
            make_mock_response(json_data=LIBRARY_DATA),
            make_mock_response(json_data={}),
        ]
        # Should not raise, still makes 2 calls
        self.stream.remove_allowed_referrer(1, "nonexistent.com")
        self.assertEqual(mock_request.call_count, 2)


class TestStreamLibraryModel(unittest.TestCase):

    def setUp(self):
        from bunnyhop.stream import StreamLibrary
        self.lib = StreamLibrary(API_KEY, **LIBRARY_DATA)

    def test_stream_library_str(self):
        self.assertEqual(str(self.lib), "My Library")

    def test_stream_library_fields(self):
        self.assertEqual(self.lib.Id, 1)
        self.assertEqual(self.lib.ReplicationRegions, ["DE"])


class TestBunnyCoreStream(unittest.TestCase):

    def setUp(self):
        from bunnyhop.core import Bunny
        self.bunny = Bunny(API_KEY)

    def test_bunny_has_stream_attribute(self):
        self.assertTrue(hasattr(self.bunny, "Stream"))

    def test_bunny_stream_is_stream_instance(self):
        from bunnyhop.stream import Stream
        self.assertIsInstance(self.bunny.Stream, Stream)


if __name__ == "__main__":
    unittest.main()
