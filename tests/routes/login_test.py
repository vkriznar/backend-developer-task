from tests.lib.base_testing import BaseTesting


class LoginTest(BaseTesting):

    def test_not_logged_in(self):
        response = self.client.get("/users/1/folders")
        self.assertEqual(response.status_code, 401)
        self.assertEqual(response.json(), {"detail": "Not authenticated"})

    def test_wrong_password(self):
        payload = "grant_type=password&username=admin&password=wrong_password"
        response = self.client.post("/token", headers=self.LOGIN_HEADER, data=payload)
        self.assertEqual(response.status_code, 401)
        self.assertEqual(response.json(), {"detail": "Incorrect username and password"})

    def test_correct_password(self):
        payload = "grant_type=password&username=admin&password=test123"
        response = self.client.post("/token", headers=self.LOGIN_HEADER, data=payload)
        self.assertEqual(response.status_code, 200)
        response_data = response.json()
        self.assertIsNotNone(response_data["access_token"])
        self.assertEqual(response_data["token_type"], "bearer")
