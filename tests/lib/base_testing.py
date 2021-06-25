from tests.lib.test_context import cleanup_db, create_test_client
import unittest


class BaseTesting(unittest.TestCase):

    LOGIN_HEADER = {
        "Content-Type": "application/x-www-form-urlencoded",
        "Accept": "application/json, text/plain, */*",
    }

    @classmethod
    def setUpClass(cls):
        print("Setting up test client")
        cleanup_db()
        cls.client = create_test_client()

    @classmethod
    def tearDownClass(cls):
        print("Cleaning up test client")
        cleanup_db()
