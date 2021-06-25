from tests.lib.base_testing import BaseTesting


class DefaultRouteTest(BaseTesting):

    def setUp(self):
        payload = f"grant_type=password&username=vkriznar&password=test123"
        response_data = self.client.post("/token", headers=self.LOGIN_HEADER, data=payload).json()
        self.AUTH_HEADER = self.LOGIN_HEADER.copy()
        self.AUTH_HEADER["Authorization"] = f"Bearer {response_data['access_token']}"

    def test_get_all_folders(self):
        response = self.client.get("/default/auth/folders", headers=self.AUTH_HEADER)
        response_data = response.json()
        self.assertEqual(len(response_data), 3)

        # Without authentication
        response = self.client.get("/default/folders")
        response_data = response.json()
        self.assertEqual(len(response_data), 3)

    def test_get_all_notes(self):
        # Overbound page number
        response = self.client.get("/default/auth/notes?notes_per_page=5&page_nr=2", headers=self.AUTH_HEADER)
        response_data = response.json()
        self.assertEqual(len(response_data), 0)

        # Low enough page number
        response = self.client.get("/default/auth/notes?notes_per_page=5&page_nr=1", headers=self.AUTH_HEADER)
        response_data = response.json()
        self.assertEqual(len(response_data), 4)
        self.assertEqual(response_data[0]["name"], "shared-note")

        # Filter by folder_id
        response = self.client.get("/default/auth/notes?notes_per_page=5&page_nr=1&folder_id=2", headers=self.AUTH_HEADER)
        response_data = response.json()
        self.assertEqual(len(response_data), 1)

        # Filter by folder_id
        response = self.client.get("/default/auth/notes?notes_per_page=5&page_nr=1&folder_id=2", headers=self.AUTH_HEADER)
        response_data = response.json()
        self.assertEqual(len(response_data), 1)

        # Filter by shared
        response = self.client.get("/default/auth/notes?notes_per_page=5&page_nr=1&shared_filter=PUBLIC", headers=self.AUTH_HEADER)
        response_data = response.json()
        self.assertEqual(len(response_data), 2)

        # Filter by text
        response = self.client.get("/default/auth/notes?notes_per_page=5&page_nr=1&node_text_filter=KEYWORD", headers=self.AUTH_HEADER)
        response_data = response.json()
        self.assertEqual(len(response_data), 2)
        self.assertEqual(response_data[0]["name"], "aaa not-shared-note-folder-2")
        self.assertEqual(response_data[1]["name"], "list-note-1")

        # Sort by sharing option
        response = self.client.get("/default/auth/notes?notes_per_page=5&page_nr=1&shared_sorting=PRIVATE", headers=self.AUTH_HEADER)
        response_data = response.json()
        self.assertEqual(len(response_data), 4)
        self.assertEqual(response_data[0]["name"], "not-shared-note")

        # Sort by heading (note name)
        response = self.client.get("/default/auth/notes?notes_per_page=5&page_nr=1&heading_sorting=ASCENDING", headers=self.AUTH_HEADER)
        response_data = response.json()
        self.assertEqual(len(response_data), 4)
        self.assertEqual(response_data[0]["name"], "aaa not-shared-note-folder-2")

        # Without authentication
        response = self.client.get("/default/notes?notes_per_page=5&page_nr=1")
        response_data = response.json()
        self.assertEqual(len(response_data), 2)
