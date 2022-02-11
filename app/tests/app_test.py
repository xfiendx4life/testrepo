import unittest

from app import app, db
from app import Users
import tempfile
import os
from flask import session


class AppTest(unittest.TestCase):
    def setUp(self):
        self.db_fd, app.config["DATABASE"] = tempfile.mkstemp()
        app.config["TESTING"] = True
        self.client = app.test_client()
        db.create_all()

    def tearDown(self):
        os.close(self.db_fd)
        os.unlink(app.config["DATABASE"])

    def test_index(self):
        res = self.client.get("/")
        self.assertEqual(res.status_code, 200)
        self.assertIn("testvalue", res.headers.get("Set-Cookie"))

    def test_login(self):
        u = Users(name="test", password="testpass")
        db.session.add(u)
        res = self.client.post(
            "/login",
            data={"name": "test", "password": "testpass"},
            follow_redirects=True,
        )
        self.assertIn("Welcome back", str(res.data))
        with self.client:  # потому что тут нам нужен активный http-запрос
            self.client.get("/")
            self.assertEqual(session.get("name"), "test")

    # TODO обработать ошибку
    # TODO обработать logout


if __name__ == "__main__":
    unittest.main()
