"""Tests for bunnyhop/base.py covering M6 (mutable defaults) and m3 (BunnyAPIError)."""
import unittest
from unittest.mock import MagicMock, patch


class TestMutableDefaultArguments(unittest.TestCase):
    """M6: Mutable default arguments in call_api should not be shared across calls."""

    def _make_bunny(self):
        from bunnyhop.base import BaseBunny
        # Bypass valley Schema validation by supplying api_key directly
        b = BaseBunny.__new__(BaseBunny)
        b.api_key = 'test-key'
        b.endpoint_url = 'https://bunnycdn.com/api'
        return b

    def _make_response(self, status_code=200, json_data=None, text=''):
        mock_resp = MagicMock()
        mock_resp.status_code = status_code
        mock_resp.text = text
        if json_data is not None:
            mock_resp.json.return_value = json_data
        else:
            mock_resp.json.return_value = {}
        return mock_resp

    def test_params_not_shared_between_calls(self):
        """Calling call_api twice: params dict used in second call must be fresh (empty),
        not polluted by anything from the first call."""
        b = self._make_bunny()
        captured_params = []

        def fake_request(**kwargs):
            # Capture a copy of params at call time
            captured_params.append(dict(kwargs.get('params', {})))
            resp = self._make_response(200, {})
            return resp

        with patch('bunnyhop.base.requests.request', side_effect=fake_request):
            # First call with explicit params
            b.call_api('/test', 'GET', params={'key': 'value'})
            # Second call with no params — should see empty dict, not the previous one
            b.call_api('/test', 'GET')

        self.assertEqual(captured_params[1], {},
                         "Second call without params should receive an empty dict, "
                         "not params from the first call (mutable default bug)")

    def test_data_not_shared_between_calls(self):
        """Calling call_api twice: data dict used in second call must be fresh."""
        b = self._make_bunny()
        captured_data = []

        def fake_request(**kwargs):
            captured_data.append(dict(kwargs.get('data', {})))
            return self._make_response(200, {})

        with patch('bunnyhop.base.requests.request', side_effect=fake_request):
            b.call_api('/test', 'POST', data={'body': 'content'})
            b.call_api('/test', 'POST')

        self.assertEqual(captured_data[1], {},
                         "Second call without data should receive an empty dict")

    def test_json_data_not_shared_between_calls(self):
        """Calling call_api twice: json_data dict used in second call must be fresh."""
        b = self._make_bunny()
        captured_json = []

        def fake_request(**kwargs):
            captured_json.append(dict(kwargs.get('json', {})))
            return self._make_response(200, {})

        with patch('bunnyhop.base.requests.request', side_effect=fake_request):
            b.call_api('/test', 'POST', json_data={'name': 'test'})
            b.call_api('/test', 'POST')

        self.assertEqual(captured_json[1], {},
                         "Second call without json_data should receive an empty dict")


class TestBunnyAPIError(unittest.TestCase):
    """m3: BunnyAPIError should be raised for 5xx responses, not for 4xx."""

    def _make_bunny(self):
        from bunnyhop.base import BaseBunny
        b = BaseBunny.__new__(BaseBunny)
        b.api_key = 'test-key'
        b.endpoint_url = 'https://bunnycdn.com/api'
        return b

    def _make_response(self, status_code, json_data=None, text=''):
        mock_resp = MagicMock()
        mock_resp.status_code = status_code
        mock_resp.text = text
        if json_data is not None:
            mock_resp.json.return_value = json_data
        else:
            from json import JSONDecodeError
            mock_resp.json.side_effect = JSONDecodeError('no json', '', 0)
        return mock_resp

    def test_bunny_api_error_class_exists(self):
        """BunnyAPIError must be importable from bunnyhop.base."""
        from bunnyhop.base import BunnyAPIError
        self.assertTrue(issubclass(BunnyAPIError, Exception))

    def test_bunny_api_error_has_status_code(self):
        """BunnyAPIError must expose status_code attribute."""
        from bunnyhop.base import BunnyAPIError
        err = BunnyAPIError(500, 'Internal Server Error')
        self.assertEqual(err.status_code, 500)

    def test_bunny_api_error_message(self):
        """BunnyAPIError string representation must include status code."""
        from bunnyhop.base import BunnyAPIError
        err = BunnyAPIError(503, 'Service Unavailable')
        self.assertIn('503', str(err))

    def test_500_raises_bunny_api_error(self):
        """call_api must raise BunnyAPIError for a 500 response."""
        from bunnyhop.base import BunnyAPIError
        b = self._make_bunny()
        mock_resp = self._make_response(500, text='Internal Server Error')

        with patch('bunnyhop.base.requests.request', return_value=mock_resp):
            with self.assertRaises(BunnyAPIError) as cm:
                b.call_api('/test', 'GET')

        self.assertEqual(cm.exception.status_code, 500)

    def test_503_raises_bunny_api_error(self):
        """call_api must raise BunnyAPIError for a 503 response."""
        from bunnyhop.base import BunnyAPIError
        b = self._make_bunny()
        mock_resp = self._make_response(503, text='Service Unavailable')

        with patch('bunnyhop.base.requests.request', return_value=mock_resp):
            with self.assertRaises(BunnyAPIError) as cm:
                b.call_api('/test', 'GET')

        self.assertEqual(cm.exception.status_code, 503)

    def test_400_does_not_raise(self):
        """call_api must NOT raise for a 400 response; it returns the JSON error body."""
        b = self._make_bunny()
        error_body = {'ErrorKey': 'invalid.request', 'Message': 'Bad Request'}
        mock_resp = MagicMock()
        mock_resp.status_code = 400
        mock_resp.text = 'Bad Request'
        mock_resp.json.return_value = error_body

        with patch('bunnyhop.base.requests.request', return_value=mock_resp):
            result = b.call_api('/test', 'GET')

        self.assertEqual(result, error_body,
                         "400 response should return the JSON body, not raise an exception")

    def test_404_does_not_raise(self):
        """call_api must NOT raise for a 404 response; it returns the JSON error body."""
        b = self._make_bunny()
        error_body = {'ErrorKey': 'not_found', 'Message': 'Not Found'}
        mock_resp = MagicMock()
        mock_resp.status_code = 404
        mock_resp.text = 'Not Found'
        mock_resp.json.return_value = error_body

        with patch('bunnyhop.base.requests.request', return_value=mock_resp):
            result = b.call_api('/test', 'GET')

        self.assertEqual(result, error_body,
                         "404 response should return the JSON body, not raise an exception")

    def test_200_returns_json_body(self):
        """call_api must return the JSON body for a 200 response."""
        b = self._make_bunny()
        body = {'Id': 42, 'Name': 'test-zone'}
        mock_resp = MagicMock()
        mock_resp.status_code = 200
        mock_resp.json.return_value = body

        with patch('bunnyhop.base.requests.request', return_value=mock_resp):
            result = b.call_api('/test', 'GET')

        self.assertEqual(result, body)


if __name__ == '__main__':
    unittest.main()
