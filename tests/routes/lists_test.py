from app.crud.list import ListDb
from tests.lib.test_context import get_test_settings
from app.context.context import get_plain_context
import json
from tests.lib.base_testing import BaseTesting


class ListTest(BaseTesting):
    def setUp(self):
        payload = f"grant_type=password&username=vkriznar&password=test123"
        response_data = self.client.post("/token", headers=self.LOGIN_HEADER, data=payload).json()
        self.AUTH_HEADER = self.LOGIN_HEADER.copy()
        self.AUTH_HEADER["Authorization"] = f"Bearer {response_data['access_token']}"

    def test_create_new_list(self):
        payload = {
            "note_id": 4,
            "text_body": "my-new-list",
        }
        response = self.client.post("/users/2/folders/1/notes/4/lists", headers=self.AUTH_HEADER, data=json.dumps(payload))
        response_data = response.json()
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response_data["text_body"], "my-new-list")

    def test_update_list(self):
        payload = {
            "text_body": "updated"
        }
        response = self.client.put("/users/2/folders/1/notes/4/lists/1", headers=self.AUTH_HEADER, data=json.dumps(payload))
        response_data = response.json()
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response_data["text_body"], "updated")

    def test_delete_list(self):
        response = self.client.delete(f"/users/2/folders/1/notes/4/lists/2", headers=self.AUTH_HEADER)
        self.assertEqual(response.status_code, 200)

        with get_plain_context(get_test_settings) as ctx:
            list_db = ListDb(ctx)
            self.assertFalse(list_db.list_exists(4, "note-4-list-some-text: cow"))
