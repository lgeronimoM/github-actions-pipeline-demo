import json
import threading
import unittest
import urllib.error
import urllib.request
from http.server import HTTPServer

from main import Handler


class ApiTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.server = HTTPServer(("127.0.0.1", 0), Handler)
        cls.port = cls.server.server_address[1]
        threading.Thread(target=cls.server.serve_forever, daemon=True).start()

    @classmethod
    def tearDownClass(cls):
        cls.server.shutdown()
        cls.server.server_close()

    def get(self, path):
        url = f"http://127.0.0.1:{self.port}{path}"
        try:
            with urllib.request.urlopen(url) as r:
                return r.status, json.loads(r.read())
        except urllib.error.HTTPError as e:
            return e.code, json.loads(e.read())

    def test_healthz(self):
        self.assertEqual(self.get("/healthz"), (200, {"status": "ok"}))

    def test_root(self):
        code, body = self.get("/")
        self.assertEqual(code, 200)
        self.assertEqual(body["app"], "demo-api")

    def test_not_found(self):
        self.assertEqual(self.get("/nope")[0], 404)


if __name__ == "__main__":
    unittest.main()
