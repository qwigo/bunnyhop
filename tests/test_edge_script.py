import collections
import collections.abc
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


SCRIPT_DATA = {
    "Id": 1,
    "Name": "my-script",
    "ScriptType": 1,
    "DeploymentKey": "deploy-key-abc",
    "CurrentReleaseId": 0,
}
SCRIPT_LIST_RESPONSE = [SCRIPT_DATA]
SCRIPT_CODE = b"export default { async fetch(req) { return new Response('hi'); } }"
SECRET_DATA = {"Id": 10, "Name": "MY_SECRET", "Secret": "s3cr3t"}
SECRETS_RESPONSE = {"Secrets": [SECRET_DATA]}
VARIABLE_DATA = {"Id": 20, "Name": "MY_VAR", "Required": False, "DefaultValue": "default"}


class TestEdgeScriptList(unittest.TestCase):
    def setUp(self):
        from bunnyhop.edge_script import EdgeScript
        self.EdgeScript = EdgeScript

    @patch("requests.request")
    def test_list_returns_list_of_edge_scripts(self, mock_request):
        from bunnyhop.edge_script import EdgeScript
        mock_request.return_value = make_mock_response(json_data=SCRIPT_LIST_RESPONSE)
        es = self.EdgeScript(API_KEY)
        result = es.list()
        self.assertIsInstance(result, list)
        self.assertEqual(len(result), 1)
        self.assertIsInstance(result[0], EdgeScript)

    @patch("requests.request")
    def test_list_uses_get_method(self, mock_request):
        mock_request.return_value = make_mock_response(json_data=SCRIPT_LIST_RESPONSE)
        es = self.EdgeScript(API_KEY)
        es.list()
        args, kwargs = mock_request.call_args
        self.assertEqual(kwargs.get("method") or args[0], "GET")

    @patch("requests.request")
    def test_list_calls_correct_endpoint(self, mock_request):
        mock_request.return_value = make_mock_response(json_data=SCRIPT_LIST_RESPONSE)
        es = self.EdgeScript(API_KEY)
        es.list()
        args, kwargs = mock_request.call_args
        url = kwargs.get("url") or args[1]
        self.assertIn("/compute/script", url)

    @patch("requests.request")
    def test_list_returns_empty_list_when_api_returns_empty_array(self, mock_request):
        mock_request.return_value = make_mock_response(json_data=[])
        es = self.EdgeScript(API_KEY)
        result = es.list()
        self.assertEqual(result, [])


class TestEdgeScriptGet(unittest.TestCase):
    def setUp(self):
        from bunnyhop.edge_script import EdgeScript
        self.EdgeScript = EdgeScript

    @patch("requests.request")
    def test_get_returns_edge_script_instance(self, mock_request):
        from bunnyhop.edge_script import EdgeScript
        meta_resp = make_mock_response(json_data=SCRIPT_DATA)
        code_resp = make_mock_response(content=SCRIPT_CODE)
        mock_request.side_effect = [meta_resp, code_resp]
        es = self.EdgeScript(API_KEY)
        result = es.get(1)
        self.assertIsInstance(result, EdgeScript)
        self.assertEqual(result.Id, 1)

    @patch("requests.request")
    def test_get_returns_none_for_missing_id(self, mock_request):
        mock_request.return_value = make_mock_response(json_data={})
        es = self.EdgeScript(API_KEY)
        result = es.get(999)
        self.assertIsNone(result)

    @patch("requests.request")
    def test_get_fetches_code_separately(self, mock_request):
        meta_resp = make_mock_response(json_data=SCRIPT_DATA)
        code_resp = make_mock_response(content=SCRIPT_CODE)
        mock_request.side_effect = [meta_resp, code_resp]
        es = self.EdgeScript(API_KEY)
        es.get(1)
        self.assertEqual(mock_request.call_count, 2)
        second_call_args, second_call_kwargs = mock_request.call_args_list[1]
        second_url = second_call_kwargs.get("url") or second_call_args[1]
        self.assertIn("/code", second_url)


class TestEdgeScriptCreate(unittest.TestCase):
    def setUp(self):
        from bunnyhop.edge_script import EdgeScript
        self.EdgeScript = EdgeScript

    @patch("requests.request")
    def test_create_returns_edge_script_on_success(self, mock_request):
        from bunnyhop.edge_script import EdgeScript
        meta_resp = make_mock_response(json_data=SCRIPT_DATA)
        bytes_resp = make_mock_response(content=b"")
        mock_request.side_effect = [meta_resp, bytes_resp]
        es = self.EdgeScript(API_KEY)
        result = es.create(Name="my-script", Content="some code")
        self.assertIsInstance(result, EdgeScript)

    @patch("requests.request")
    def test_create_posts_to_compute_script(self, mock_request):
        meta_resp = make_mock_response(json_data=SCRIPT_DATA)
        bytes_resp = make_mock_response(content=b"")
        mock_request.side_effect = [meta_resp, bytes_resp]
        es = self.EdgeScript(API_KEY)
        es.create(Name="my-script", Content="some code")
        first_call_args, first_call_kwargs = mock_request.call_args_list[0]
        method = first_call_kwargs.get("method") or first_call_args[0]
        url = first_call_kwargs.get("url") or first_call_args[1]
        self.assertEqual(method, "POST")
        self.assertTrue(url.endswith("/compute/script"))

    @patch("requests.request")
    def test_create_sends_name_and_script_type(self, mock_request):
        meta_resp = make_mock_response(json_data=SCRIPT_DATA)
        bytes_resp = make_mock_response(content=b"")
        mock_request.side_effect = [meta_resp, bytes_resp]
        es = self.EdgeScript(API_KEY)
        es.create(Name="my-script", Content="some code")
        first_call_args, first_call_kwargs = mock_request.call_args_list[0]
        json_body = first_call_kwargs.get("json")
        self.assertIn("Name", json_body)
        self.assertIn("ScriptType", json_body)

    @patch("requests.request")
    def test_create_uploads_code_after_creation(self, mock_request):
        meta_resp = make_mock_response(json_data=SCRIPT_DATA)
        bytes_resp = make_mock_response(content=b"")
        mock_request.side_effect = [meta_resp, bytes_resp]
        es = self.EdgeScript(API_KEY)
        es.create(Name="my-script", Content="some code")
        self.assertEqual(mock_request.call_count, 2)
        second_call_args, second_call_kwargs = mock_request.call_args_list[1]
        second_url = second_call_kwargs.get("url") or second_call_args[1]
        self.assertIn("/code", second_url)

    @patch("requests.request")
    def test_create_skips_code_upload_when_content_empty(self, mock_request):
        meta_resp = make_mock_response(json_data=SCRIPT_DATA)
        mock_request.return_value = meta_resp
        es = self.EdgeScript(API_KEY)
        es.create(Name="my-script", Content="")
        self.assertEqual(mock_request.call_count, 1)


class TestEdgeScriptUpdate(unittest.TestCase):
    def setUp(self):
        from bunnyhop.edge_script import EdgeScript
        self.EdgeScript = EdgeScript

    @patch("requests.request")
    def test_update_posts_name_to_script_endpoint(self, mock_request):
        mock_request.return_value = make_mock_response(content=b"")
        es = self.EdgeScript(API_KEY)
        es.update(1, Name="new-name")
        first_call_args, first_call_kwargs = mock_request.call_args_list[0]
        method = first_call_kwargs.get("method") or first_call_args[0]
        url = first_call_kwargs.get("url") or first_call_args[1]
        self.assertEqual(method, "POST")
        self.assertIn("/compute/script/1", url)

    @patch("requests.request")
    def test_update_posts_content_to_code_endpoint(self, mock_request):
        mock_request.return_value = make_mock_response(content=b"")
        es = self.EdgeScript(API_KEY)
        es.update(1, Content="new code")
        call_args, call_kwargs = mock_request.call_args
        url = call_kwargs.get("url") or call_args[1]
        self.assertIn("/code", url)

    @patch("requests.request")
    def test_update_only_one_call_when_only_name_given(self, mock_request):
        mock_request.return_value = make_mock_response(content=b"")
        es = self.EdgeScript(API_KEY)
        es.update(1, Name="new-name")
        self.assertEqual(mock_request.call_count, 1)


class TestEdgeScriptDelete(unittest.TestCase):
    def setUp(self):
        from bunnyhop.edge_script import EdgeScript
        self.EdgeScript = EdgeScript

    @patch("requests.request")
    def test_delete_uses_delete_method(self, mock_request):
        mock_request.return_value = make_mock_response(content=b"")
        es = self.EdgeScript(API_KEY)
        es.delete(1)
        call_args, call_kwargs = mock_request.call_args
        method = call_kwargs.get("method") or call_args[0]
        self.assertEqual(method, "DELETE")

    @patch("requests.request")
    def test_delete_calls_correct_endpoint(self, mock_request):
        mock_request.return_value = make_mock_response(content=b"")
        es = self.EdgeScript(API_KEY)
        es.delete(1)
        call_args, call_kwargs = mock_request.call_args
        url = call_kwargs.get("url") or call_args[1]
        self.assertIn("/compute/script/1", url)

    @patch("requests.request")
    def test_delete_returns_string_on_success(self, mock_request):
        mock_request.return_value = make_mock_response(content=b"")
        es = self.EdgeScript(API_KEY)
        result = es.delete(1)
        self.assertIsInstance(result, str)


class TestEdgeScriptPublish(unittest.TestCase):
    def setUp(self):
        from bunnyhop.edge_script import EdgeScript
        self.EdgeScript = EdgeScript

    @patch("requests.request")
    def test_publish_uses_post_method(self, mock_request):
        mock_request.return_value = make_mock_response(content=b"")
        es = self.EdgeScript(API_KEY)
        es.publish(1, note="v1.0")
        call_args, call_kwargs = mock_request.call_args
        method = call_kwargs.get("method") or call_args[0]
        self.assertEqual(method, "POST")

    @patch("requests.request")
    def test_publish_calls_publish_endpoint(self, mock_request):
        mock_request.return_value = make_mock_response(content=b"")
        es = self.EdgeScript(API_KEY)
        es.publish(1, note="v1.0")
        call_args, call_kwargs = mock_request.call_args
        url = call_kwargs.get("url") or call_args[1]
        self.assertIn("/publish", url)

    @patch("requests.request")
    def test_publish_sends_note_in_body(self, mock_request):
        mock_request.return_value = make_mock_response(content=b"")
        es = self.EdgeScript(API_KEY)
        es.publish(1, note="v1.0")
        call_args, call_kwargs = mock_request.call_args
        json_body = call_kwargs.get("json")
        self.assertIn("Note", json_body)

    @patch("requests.request")
    def test_publish_returns_string_on_success(self, mock_request):
        mock_request.return_value = make_mock_response(content=b"")
        es = self.EdgeScript(API_KEY)
        result = es.publish(1, note="v1.0")
        self.assertIsInstance(result, str)


class TestEdgeScriptSecrets(unittest.TestCase):
    def setUp(self):
        from bunnyhop.edge_script import EdgeScript
        self.EdgeScript = EdgeScript

    @patch("requests.request")
    def test_list_secrets_returns_list(self, mock_request):
        from bunnyhop.edge_script import EdgeScriptSecret
        mock_request.return_value = make_mock_response(json_data=SECRETS_RESPONSE)
        es = self.EdgeScript(API_KEY)
        result = es.list_secrets(1)
        self.assertIsInstance(result, list)
        self.assertEqual(len(result), 1)
        self.assertIsInstance(result[0], EdgeScriptSecret)

    @patch("requests.request")
    def test_add_secret_posts_to_secrets_endpoint(self, mock_request):
        mock_request.return_value = make_mock_response(json_data=SECRET_DATA)
        es = self.EdgeScript(API_KEY)
        es.add_secret(1, "MY_SECRET", "s3cr3t")
        call_args, call_kwargs = mock_request.call_args
        method = call_kwargs.get("method") or call_args[0]
        url = call_kwargs.get("url") or call_args[1]
        json_body = call_kwargs.get("json")
        self.assertEqual(method, "POST")
        self.assertIn("/secrets", url)
        self.assertIn("Name", json_body)
        self.assertIn("Secret", json_body)

    @patch("requests.request")
    def test_add_secret_returns_secret_instance(self, mock_request):
        from bunnyhop.edge_script import EdgeScriptSecret
        mock_request.return_value = make_mock_response(json_data=SECRET_DATA)
        es = self.EdgeScript(API_KEY)
        result = es.add_secret(1, "MY_SECRET", "s3cr3t")
        self.assertIsInstance(result, EdgeScriptSecret)

    @patch("requests.request")
    def test_update_secret_uses_put_method(self, mock_request):
        mock_request.return_value = make_mock_response(content=b"")
        es = self.EdgeScript(API_KEY)
        es.update_secret(1, "MY_SECRET", "new-value")
        call_args, call_kwargs = mock_request.call_args
        method = call_kwargs.get("method") or call_args[0]
        self.assertEqual(method, "PUT")

    @patch("requests.request")
    def test_update_secret_sends_zero_id(self, mock_request):
        mock_request.return_value = make_mock_response(content=b"")
        es = self.EdgeScript(API_KEY)
        es.update_secret(1, "MY_SECRET", "new-value")
        call_args, call_kwargs = mock_request.call_args
        json_body = call_kwargs.get("json")
        self.assertEqual(json_body["Id"], 0)

    @patch("requests.request")
    def test_delete_secret_uses_delete_method_and_correct_url(self, mock_request):
        mock_request.return_value = make_mock_response(content=b"")
        es = self.EdgeScript(API_KEY)
        es.delete_secret(1, 10)
        call_args, call_kwargs = mock_request.call_args
        method = call_kwargs.get("method") or call_args[0]
        url = call_kwargs.get("url") or call_args[1]
        self.assertEqual(method, "DELETE")
        self.assertIn("/secrets/10", url)

    @patch("requests.request")
    def test_delete_secret_returns_string(self, mock_request):
        mock_request.return_value = make_mock_response(content=b"")
        es = self.EdgeScript(API_KEY)
        result = es.delete_secret(1, 10)
        self.assertIsInstance(result, str)


class TestEdgeScriptVariables(unittest.TestCase):
    def setUp(self):
        from bunnyhop.edge_script import EdgeScript
        self.EdgeScript = EdgeScript

    @patch("requests.request")
    def test_add_variable_posts_to_add_endpoint(self, mock_request):
        mock_request.return_value = make_mock_response(json_data=VARIABLE_DATA)
        es = self.EdgeScript(API_KEY)
        es.add_variable(1, "MY_VAR", required=False, default_value="default")
        call_args, call_kwargs = mock_request.call_args
        url = call_kwargs.get("url") or call_args[1]
        json_body = call_kwargs.get("json")
        self.assertIn("/variables/add", url)
        self.assertIn("Name", json_body)
        self.assertIn("Required", json_body)
        self.assertIn("DefaultValue", json_body)

    @patch("requests.request")
    def test_update_variable_posts_to_variable_id_endpoint(self, mock_request):
        mock_request.return_value = make_mock_response(content=b"")
        es = self.EdgeScript(API_KEY)
        es.update_variable(1, 20, name="NEW_VAR")
        call_args, call_kwargs = mock_request.call_args
        url = call_kwargs.get("url") or call_args[1]
        self.assertIn("/variables/20", url)

    @patch("requests.request")
    def test_delete_variable_uses_delete_and_correct_url(self, mock_request):
        mock_request.return_value = make_mock_response(content=b"")
        es = self.EdgeScript(API_KEY)
        es.delete_variable(1, 20)
        call_args, call_kwargs = mock_request.call_args
        method = call_kwargs.get("method") or call_args[0]
        url = call_kwargs.get("url") or call_args[1]
        self.assertEqual(method, "DELETE")
        self.assertIn("/variables/20", url)

    @patch("requests.request")
    def test_delete_variable_returns_string(self, mock_request):
        mock_request.return_value = make_mock_response(content=b"")
        es = self.EdgeScript(API_KEY)
        result = es.delete_variable(1, 20)
        self.assertIsInstance(result, str)


class TestBunnyCoreEdgeScript(unittest.TestCase):
    def setUp(self):
        from bunnyhop.core import Bunny
        self.bunny = Bunny(API_KEY)

    def test_bunny_has_edge_script_attribute(self):
        self.assertTrue(hasattr(self.bunny, "EdgeScript"))

    def test_bunny_edge_script_is_edge_script_instance(self):
        from bunnyhop.edge_script import EdgeScript
        self.assertIsInstance(self.bunny.EdgeScript, EdgeScript)


if __name__ == "__main__":
    unittest.main()
