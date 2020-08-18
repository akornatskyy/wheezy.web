""" ``test_hello`` module.
"""

import unittest

from hello import main

from wheezy.http.functional import WSGIClient


class HelloTestCase(unittest.TestCase):
    def setUp(self):
        self.client = WSGIClient(main)

    def tearDown(self):
        del self.client
        self.client = None

    def test_home(self):
        """Ensure welcome page is rendered."""
        assert 200 == self.client.get("/")
        assert "Hello World!" == self.client.content

    def test_welcome(self):
        """Ensure welcome page is rendered."""
        assert 200 == self.client.get("/welcome")
        assert "Hello World!" == self.client.content
