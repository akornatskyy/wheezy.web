
""" ``test_views`` module.
"""

import unittest

from wheezy.http.functional import WSGIClient

from app import main


class PublicTestCase(unittest.TestCase):

    def setUp(self):
        self.client = WSGIClient(main)

    def tearDown(self):
        del self.client
        self.client = None

    def test_home(self):
        """ Ensure home page is rendered.
        """
        assert 200 == self.client.get('/en/home')
        assert '- Home</title>' in self.client.content

    def test_about(self):
        """ Ensure about page is rendered.
        """
        assert 200 == self.client.get('/en/about')
        assert '- About</title>' in self.client.content
