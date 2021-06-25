import json
from tests.lib.base_testing import BaseTesting


class UserTest(BaseTesting):

    def setUp(self):
        payload = f"grant_type=password&username=admin&password=test123"
        response_data = self.client.post("/token", headers=self.LOGIN_HEADER, data=payload).json()
        self.AUTH_HEADER = self.LOGIN_HEADER.copy()
        self.AUTH_HEADER["Authorization"] = f"Bearer {response_data['access_token']}"

    def test_create_user(self):
        payload = {
            "name": "test-user",
            "username": "Testing User",
            "password": "test123"
        }
        response = self.client.post("/users", headers=self.AUTH_HEADER, data=json.dumps(payload))
        response_data = response.json()
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response_data["id"], 3)
        self.assertEqual(response_data["username"], payload["username"])
