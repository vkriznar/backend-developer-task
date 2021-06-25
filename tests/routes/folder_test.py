from tests.lib.test_context import get_test_settings
from app.crud.folder import FolderDb
from app.context.context import get_plain_context
import json
from tests.lib.base_testing import BaseTesting


class FolderTest(BaseTesting):

    def setUp(self):
        payload = f"grant_type=password&username=admin&password=test123"
        response_data = self.client.post("/token", headers=self.LOGIN_HEADER, data=payload).json()
        self.AUTH_HEADER = self.LOGIN_HEADER.copy()
        self.AUTH_HEADER["Authorization"] = f"Bearer {response_data['access_token']}"

    def test_get_all(self):
        response = self.client.get("/users/1/folders", headers=self.AUTH_HEADER)
        response_data = response.json()
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response_data), 2)
        self.assertEqual(response_data[0]["name"], 'admin-folder')

    def test_get_by_id(self):
        response = self.client.get("/users/2/folders/1", headers=self.AUTH_HEADER)
        response_data = response.json()
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response_data["name"], 'vkriznar-folder-1')

    def test_get_by_name(self):
        response = self.client.get("/users/2/folders/name/vkriznar-folder-1", headers=self.AUTH_HEADER)
        response_data = response.json()
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response_data["id"], 1)

    def test_create_new_folder(self):
        payload = {
            "name": "new-admin-folder"
        }
        response = self.client.post("/users/1/folders", headers=self.AUTH_HEADER, data=json.dumps(payload))
        response_data = response.json()
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response_data["id"], 4)
        self.assertEqual(response_data["name"], "new-admin-folder")

    def test_update_folder(self):
        payload = {
            "name": "updated-admin-folder"
        }
        response = self.client.put("/users/1/folders/3", headers=self.AUTH_HEADER, data=json.dumps(payload))
        response_data = response.json()
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response_data["name"], "updated-admin-folder")

    def test_delete_folder(self):
        payload = {
            "name": "to-be-deleted"
        }
        response = self.client.post("/users/1/folders", headers=self.AUTH_HEADER, data=json.dumps(payload))
        id = response.json()["id"]
        response = self.client.delete(f"/users/1/folders/{id}?force=true", headers=self.AUTH_HEADER)
        self.assertEqual(response.status_code, 200)

        with get_plain_context(get_test_settings) as ctx:
            folder_db = FolderDb(ctx)
            self.assertFalse(folder_db.folder_exists(1, "to-be-deleted"))
