import json
from app.crud.note import NoteDb
from tests.lib.test_context import get_test_settings
from app.context.context import get_plain_context
from tests.lib.base_testing import BaseTesting


class NotesTest(BaseTesting):

    def setUp(self):
        payload = f"grant_type=password&username=vkriznar&password=test123"
        response_data = self.client.post("/token", headers=self.LOGIN_HEADER, data=payload).json()
        self.AUTH_HEADER = self.LOGIN_HEADER.copy()
        self.AUTH_HEADER["Authorization"] = f"Bearer {response_data['access_token']}"

    def test_get_all(self):
        response = self.client.get("/users/2/folders/1/notes", headers=self.AUTH_HEADER)
        response_data = response.json()
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response_data), 3)

    def test_get_by_id(self):
        response = self.client.get("/users/2/folders/1/notes/1", headers=self.AUTH_HEADER)
        response_data = response.json()
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response_data["name"], "shared-note")
        self.assertEqual(response_data["shared"], True)
        self.assertEqual(response_data["type"], "TEXT")

    def test_get_by_name(self):
        response = self.client.get("/users/2/folders/1/notes/name/shared-note", headers=self.AUTH_HEADER)
        response_data = response.json()
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response_data["id"], 1)

    def test_create_new_note(self):
        payload = {
            "folder_id": 1,
            "name": "my-new-note",
            "shared": False,
            "type": "TEXT",
            "text_body": "my-new-note"
        }
        response = self.client.post("/users/2/folders/1/notes", headers=self.AUTH_HEADER, data=json.dumps(payload))
        response_data = response.json()
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response_data["name"], "my-new-note")

    def test_update_note(self):
        payload = {
            "name": "shared-note-updated",
            "shared": False,
            "text_body": "updated"
        }
        response = self.client.put("/users/2/folders/1/notes/1", headers=self.AUTH_HEADER, data=json.dumps(payload))
        response_data = response.json()
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response_data["name"], "shared-note-updated")
        self.assertEqual(response_data["shared"], False)
        self.assertEqual(response_data["text_body"], "updated")

    def test_delete_note(self):
        response = self.client.delete(f"/users/2/folders/1/notes/4?force=false", headers=self.AUTH_HEADER)
        self.assertEqual(response.status_code, 422)

        response = self.client.delete(f"/users/2/folders/1/notes/4?force=true", headers=self.AUTH_HEADER)
        self.assertEqual(response.status_code, 200)

        with get_plain_context(get_test_settings) as ctx:
            note_db = NoteDb(ctx)
            self.assertFalse(note_db.note_exists(1, "list-note-1"))
