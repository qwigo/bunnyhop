from bunnyhop import base

SCRIPT_TYPE_DNS = 0
SCRIPT_TYPE_STANDALONE = 1
SCRIPT_TYPE_MIDDLEWARE = 2


class EdgeScriptSecret(base.BaseBunny):
    Id = base.IntegerProperty()
    Name = base.CharProperty()
    Secret = base.CharProperty()

    def __str__(self):
        return self.Name or ""


class EdgeScriptVariable(base.BaseBunny):
    Id = base.IntegerProperty()
    Name = base.CharProperty()
    Required = base.BooleanProperty(default_value=False)
    DefaultValue = base.CharProperty()

    def __str__(self):
        return self.Name or ""


class EdgeScript(base.BaseBunny):
    endpoint_url = "https://api.bunny.net"

    Id = base.IntegerProperty()
    Name = base.CharProperty()
    ScriptType = base.IntegerProperty()
    Content = base.CharProperty()
    DeploymentKey = base.CharProperty()
    CurrentReleaseId = base.IntegerProperty()

    def __str__(self):
        return self.Name or ""

    def list(self):
        response = self.call_api("/compute/script", "GET")
        if not isinstance(response, list):
            return []
        return [EdgeScript(self.api_key, **item) for item in response]

    def get(self, id):
        response = self.call_api(f"/compute/script/{id}", "GET")
        try:
            if not response.get('Id', None):
                return None
        except (AttributeError, TypeError):
            return None
        code = self.call_api(f"/compute/script/{id}/code", "GET")
        if isinstance(code, bytes):
            response['Content'] = code.decode('utf-8')
        elif isinstance(code, str):
            response['Content'] = code
        return EdgeScript(self.api_key, **response)

    def create(self, Name, ScriptType=SCRIPT_TYPE_STANDALONE, Content=""):
        api_data = {"Name": Name, "ScriptType": ScriptType}
        response = self.call_api("/compute/script", "POST", json_data=api_data)
        script_id = response.get('Id', None) if isinstance(response, dict) else None
        if not script_id:
            return response
        if Content:
            self.call_api(f"/compute/script/{script_id}/code", "POST", json_data={"Code": Content})
        return EdgeScript(self.api_key, **response)

    def update(self, id, Name=None, Content=None):
        if Name is not None:
            self.call_api(f"/compute/script/{id}", "POST", json_data={"Name": Name})
        if Content is not None:
            self.call_api(f"/compute/script/{id}/code", "POST", json_data={"Code": Content})
        return "Script updated."

    def delete(self, id):
        response = self.call_api(f"/compute/script/{id}", "DELETE")
        if isinstance(response, bytes):
            return "Script deleted."
        return response

    def publish(self, id, note=""):
        response = self.call_api(f"/compute/script/{id}/publish", "POST", json_data={"Note": note})
        if isinstance(response, bytes):
            return "Script published."
        return response

    def list_secrets(self, script_id):
        response = self.call_api(f"/compute/script/{script_id}/secrets", "GET")
        if isinstance(response, dict):
            secrets = response.get('Secrets', [])
        elif isinstance(response, list):
            secrets = response
        else:
            secrets = []
        return [EdgeScriptSecret(self.api_key, **s) for s in secrets]

    def add_secret(self, script_id, name, value):
        api_data = {"Name": name, "Secret": value}
        response = self.call_api(f"/compute/script/{script_id}/secrets", "POST", json_data=api_data)
        if isinstance(response, dict) and response.get('Id'):
            return EdgeScriptSecret(self.api_key, **response)
        return response

    def update_secret(self, script_id, name, value):
        api_data = {"Id": 0, "Name": name, "Secret": value}
        response = self.call_api(f"/compute/script/{script_id}/secrets", "PUT", json_data=api_data)
        if isinstance(response, bytes):
            return "Secret updated."
        return response

    def delete_secret(self, script_id, secret_id):
        response = self.call_api(f"/compute/script/{script_id}/secrets/{secret_id}", "DELETE")
        if isinstance(response, bytes):
            return "Secret deleted."
        return response

    def add_variable(self, script_id, name, required=False, default_value=""):
        api_data = {"Name": name, "Required": required, "DefaultValue": default_value}
        return self.call_api(f"/compute/script/{script_id}/variables/add", "POST", json_data=api_data)

    def update_variable(self, script_id, variable_id, name=None, required=None, default_value=None):
        api_data = {}
        if name is not None:
            api_data["Name"] = name
        if required is not None:
            api_data["Required"] = required
        if default_value is not None:
            api_data["DefaultValue"] = default_value
        return self.call_api(f"/compute/script/{script_id}/variables/{variable_id}", "POST", json_data=api_data)

    def delete_variable(self, script_id, variable_id):
        response = self.call_api(f"/compute/script/{script_id}/variables/{variable_id}", "DELETE")
        if isinstance(response, bytes):
            return "Variable deleted."
        return response
