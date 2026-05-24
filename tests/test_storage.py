"""
Tests for bunnyhop/storage.py — covers all bugs listed in the code quality review.
All HTTP calls are mocked; no real network traffic is made.
"""
import collections
import collections.abc
import json
import unittest
from io import BytesIO
from unittest.mock import MagicMock, mock_open, patch

# Python 3.10+ removed collections.Callable; valley 1.5.x still uses it.
# Restore the alias before any bunnyhop imports so valley initialises cleanly.
if not hasattr(collections, 'Callable'):
    collections.Callable = collections.abc.Callable

# ---------------------------------------------------------------------------
# Minimal fixture data so StorageZone / Storage instances can be constructed
# without touching real env vars.
# ---------------------------------------------------------------------------
STORAGE_ZONE_DATA = {
    'Id': 1,
    'UserId': 'user-guid-1234',
    'Name': 'testzone',
    'Password': 'test-password',
    'DateModified': '2024-01-01T00:00:00Z',
    'Deleted': False,
    'StorageUsed': 0,
    'FilesStored': 0,
    'Region': 'NY',
    'ReplicationRegions': [],
    'PullZones': [],
    'ReadOnlyPassword': 'ro-password',
}

STORAGE_OBJECT_DATA = {
    'Guid': 'obj-guid-1234',
    'StorageZoneName': 'testzone',
    'Path': '/testzone/',
    'ObjectName': 'hello.txt',
    'Length': 5,
    'LastChanged': '2024-01-01T00:00:00Z',
    'ServerId': 1,
    'IsDirectory': False,
    'UserId': 'user-guid-1234',
    'ContentType': 'text/plain',
    'DateCreated': '2024-01-01T00:00:00Z',
    'StorageZoneId': 1,
    'Checksum': 'abc123',
    'ReplicatedZones': [],
}


def _make_storage_zone():
    """Return a StorageZone instance without making any HTTP calls."""
    from bunnyhop.storage import StorageZone
    return StorageZone('test-api-key', **STORAGE_ZONE_DATA)


def _make_storage():
    """Return a Storage instance without making any HTTP calls."""
    from bunnyhop.storage import Storage
    return Storage('test-api-key')


def _mock_response(json_data=None, content=b''):
    """Build a mock requests.Response-like object."""
    mock_resp = MagicMock()
    if json_data is not None:
        mock_resp.json.return_value = json_data
        mock_resp.content = json.dumps(json_data).encode()
    else:
        # Use JSONDecodeError (subclass of ValueError) so base.py's except clause catches it
        mock_resp.json.side_effect = json.JSONDecodeError("no json", "", 0)
        mock_resp.content = content
    return mock_resp


# ===========================================================================
# M2 — create_file() is an unimplemented stub
# ===========================================================================
class TestCreateFile(unittest.TestCase):

    def setUp(self):
        self.zone = _make_storage_zone()

    @patch('requests.request')
    def test_create_file_bytes_calls_api(self, mock_request):
        """create_file() must call the storage API (not silently return None)."""
        mock_request.return_value = _mock_response(json_data={'HttpCode': 201})
        result = self.zone.create_file('hello.txt', b'hello')
        # Must have made exactly one HTTP call
        mock_request.assert_called_once()
        # The result must NOT be None (stub returns None)
        self.assertIsNotNone(result)

    @patch('requests.request')
    def test_create_file_str_content_encoded_to_utf8(self, mock_request):
        """create_file() with str content must encode to UTF-8 before sending."""
        mock_request.return_value = _mock_response(json_data={'HttpCode': 201})
        self.zone.create_file('hello.txt', 'hello world')
        mock_request.assert_called_once()
        # Inspect the 'data' keyword argument passed to requests.request
        _, kwargs = mock_request.call_args
        sent_data = kwargs.get('data', b'')
        self.assertIsInstance(sent_data, bytes)
        self.assertEqual(sent_data, 'hello world'.encode('utf-8'))

    @patch('requests.request')
    def test_create_file_bytes_content_sent_as_is(self, mock_request):
        """create_file() with bytes content must send the bytes unchanged."""
        mock_request.return_value = _mock_response(json_data={'HttpCode': 201})
        payload = b'\x00\x01\x02\x03'
        self.zone.create_file('binary.bin', payload)
        _, kwargs = mock_request.call_args
        self.assertEqual(kwargs.get('data', None), payload)

    @patch('requests.request')
    def test_create_file_uses_correct_url(self, mock_request):
        """create_file() must PUT to /{zone_name}/{file_name}."""
        mock_request.return_value = _mock_response(json_data={'HttpCode': 201})
        self.zone.create_file('subdir/page.html', b'<html/>')
        all_args = mock_request.call_args
        url_arg = all_args[1].get('url') if all_args[1].get('url') else all_args[0][1]
        self.assertIn('/testzone/subdir/page.html', url_arg)

    @patch('requests.request')
    def test_create_file_uses_put_method(self, mock_request):
        """create_file() must use the PUT HTTP method."""
        mock_request.return_value = _mock_response(json_data={'HttpCode': 201})
        self.zone.create_file('hello.txt', b'data')
        all_args = mock_request.call_args
        method_arg = all_args[1].get('method') if all_args[1].get('method') else all_args[0][0]
        self.assertEqual(method_arg.upper(), 'PUT')


# ===========================================================================
# M3 — upload_file() file handle leak
# ===========================================================================
class TestUploadFile(unittest.TestCase):

    def setUp(self):
        self.zone = _make_storage_zone()

    @patch('requests.request')
    def test_upload_file_uses_context_manager(self, mock_request):
        """upload_file() must open the file with a context manager (with open(...))."""
        mock_request.return_value = _mock_response(json_data={'HttpCode': 201})
        file_content = b'file contents here'
        m = mock_open(read_data=file_content)
        with patch('builtins.open', m):
            self.zone.upload_file('dest/path', 'myfile.txt', '/local/path/myfile.txt')
        # The context manager protocol must be used: __enter__ and __exit__ called
        m.assert_called_once_with('/local/path/myfile.txt', 'rb')
        m().__enter__.assert_called()
        m().__exit__.assert_called()

    @patch('requests.request')
    def test_upload_file_sends_correct_data(self, mock_request):
        """upload_file() must pass the file contents to call_storage_api."""
        mock_request.return_value = _mock_response(json_data={'HttpCode': 201})
        file_content = b'some binary data'
        m = mock_open(read_data=file_content)
        with patch('builtins.open', m):
            self.zone.upload_file('dest', 'file.bin', '/tmp/file.bin')
        _, kwargs = mock_request.call_args
        self.assertEqual(kwargs.get('data'), file_content)


# ===========================================================================
# m1 — get_object() IndexError risk and double API call
# ===========================================================================
class TestGetObject(unittest.TestCase):

    def setUp(self):
        self.zone = _make_storage_zone()

    @patch('requests.request')
    def test_get_object_raises_file_not_found_when_missing(self, mock_request):
        """get_object() must raise FileNotFoundError when file is absent from listing."""
        # API returns a list that does NOT contain the requested file
        mock_request.return_value = _mock_response(json_data=[STORAGE_OBJECT_DATA])
        with self.assertRaises(FileNotFoundError):
            self.zone.get_object('nonexistent.txt')

    @patch('requests.request')
    def test_get_object_raises_file_not_found_on_non_list_response(self, mock_request):
        """get_object() must raise FileNotFoundError when API returns a non-list."""
        mock_request.return_value = _mock_response(
            json_data={'HttpCode': 401, 'Message': 'Unauthorized'}
        )
        with self.assertRaises(FileNotFoundError):
            self.zone.get_object('hello.txt')

    @patch('requests.request')
    def test_get_object_returns_storage_object_when_found(self, mock_request):
        """get_object() must return a StorageObject when the file exists."""
        from bunnyhop.storage import StorageObject
        mock_request.return_value = _mock_response(json_data=[STORAGE_OBJECT_DATA])
        result = self.zone.get_object('hello.txt')
        self.assertIsInstance(result, StorageObject)

    @patch('requests.request')
    def test_get_object_makes_single_api_call(self, mock_request):
        """get_object() must make only ONE API call (not two)."""
        mock_request.return_value = _mock_response(json_data=[STORAGE_OBJECT_DATA])
        self.zone.get_object('hello.txt')
        self.assertEqual(mock_request.call_count, 1)


# ===========================================================================
# m2 — delete_file() unsafe attribute access
# ===========================================================================
class TestDeleteFile(unittest.TestCase):

    def setUp(self):
        self.zone = _make_storage_zone()

    @patch('requests.request')
    def test_delete_file_does_not_raise_on_bytes_response(self, mock_request):
        """delete_file() must NOT raise AttributeError when response is bytes."""
        # Simulate a successful DELETE that returns an empty body (bytes)
        mock_request.return_value = _mock_response(content=b'')
        try:
            self.zone.delete_file('hello.txt')
        except AttributeError:
            self.fail("delete_file() raised AttributeError on bytes response")

    @patch('requests.request')
    def test_delete_file_raises_on_404(self, mock_request):
        """delete_file() must raise an exception when API returns 404."""
        mock_request.return_value = _mock_response(
            json_data={'HttpCode': 404, 'Message': 'File not found'}
        )
        with self.assertRaises(Exception):
            self.zone.delete_file('missing.txt')

    @patch('requests.request')
    def test_delete_file_returns_response_on_success(self, mock_request):
        """delete_file() must return the response when deletion succeeds."""
        mock_request.return_value = _mock_response(content=b'')
        result = self.zone.delete_file('hello.txt')
        # Should return the bytes content (not raise, not return None from a crash)
        self.assertIsNotNone(result)


# ===========================================================================
# m8 — Storage.create() bare Exception replaced with ValueError
# ===========================================================================
class TestStorageCreate(unittest.TestCase):

    def setUp(self):
        self.storage = _make_storage()

    @patch('requests.request')
    def test_create_raises_value_error_on_api_error(self, mock_request):
        """Storage.create() must raise ValueError (not bare Exception) on failure."""
        mock_request.return_value = _mock_response(json_data={
            'ErrorKey': 'storagezone.validation',
            'Message': 'Validation failed'
        })
        with self.assertRaises(ValueError):
            self.storage.create('badzone')

    @patch('requests.request')
    def test_create_returns_storage_zone_on_success(self, mock_request):
        """Storage.create() must return a StorageZone on success."""
        from bunnyhop.storage import StorageZone
        mock_request.return_value = _mock_response(json_data=STORAGE_ZONE_DATA)
        result = self.storage.create('testzone', main_storage_region='NY')
        self.assertIsInstance(result, StorageZone)


# ===========================================================================
# m11 — Storage.update() missing method
# ===========================================================================
class TestStorageUpdate(unittest.TestCase):

    def setUp(self):
        self.storage = _make_storage()

    @patch('requests.request')
    def test_update_calls_post_on_correct_endpoint(self, mock_request):
        """Storage.update() must POST to /storagezone/{id}."""
        mock_request.return_value = _mock_response(json_data={})
        self.storage.update(42, ReplicationRegions=['DE'])
        mock_request.assert_called_once()
        all_args = mock_request.call_args
        method_arg = all_args[1].get('method') if all_args[1].get('method') else all_args[0][0]
        url_arg = all_args[1].get('url') if all_args[1].get('url') else all_args[0][1]
        self.assertEqual(method_arg.upper(), 'POST')
        self.assertIn('/storagezone/42', url_arg)

    @patch('requests.request')
    def test_update_sends_kwargs_as_json(self, mock_request):
        """Storage.update() must forward keyword arguments as the JSON body."""
        mock_request.return_value = _mock_response(json_data={})
        self.storage.update(42, ReplicationRegions=['DE', 'SG'], OriginUrl='https://example.com')
        all_args = mock_request.call_args
        sent_json = all_args[1].get('json', {})
        self.assertEqual(sent_json.get('ReplicationRegions'), ['DE', 'SG'])
        self.assertEqual(sent_json.get('OriginUrl'), 'https://example.com')

    def test_update_method_exists(self):
        """Storage.update() must exist (not AttributeError)."""
        self.assertTrue(hasattr(self.storage, 'update'),
                        "Storage class is missing the 'update' method")
        self.assertTrue(callable(self.storage.update))


if __name__ == '__main__':
    unittest.main()
