""" ``test_helloworld`` module.
"""

import unittest

from helloworld import main

from wheezy.http.functional import WSGIClient


class HelloworldTestCase(unittest.TestCase):
    def setUp(self):
        self.client = WSGIClient(main)

    def tearDown(self):
        del self.client
        self.client = None

    def test_welcome(self):
        """Ensure welcome page is rendered."""
        assert 200 == self.client.get("/")
        assert "Hello" in self.client.content

    def test_welcome2(self):
        """Ensure welcome2 page is rendered."""
        assert 200 == self.client.get("/welcome2")
        assert "Hello" in self.client.content

    def test_now(self):
        """Ensure now page is rendered."""
        assert 200 == self.client.get("/now")
        assert "It is" in self.client.content

    def test_now2(self):
        """Ensure welcome page is rendered."""
        assert 200 == self.client.get("/now2")
        assert "It is" in self.client.content
