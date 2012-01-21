
""" ``test_views`` module.
"""

import unittest

from wheezy.http.functional import WSGIClient

from app import main


class ErrorTestCase(unittest.TestCase):

    def setUp(self):
        self.client = WSGIClient(main)

    def tearDown(self):
        del self.client
        self.client = None

    def test_bad_request(self):
        """ Ensure bad request page is rendered.
        """
        self.client.go('/en/error/test-bad-request')
        assert 400 == self.client.follow()
        assert 'Code 400' in self.client.content

    def test_forbidden(self):
        """ Ensure forbidden page is rendered.
        """
        self.client.go('/en/error/test-forbidden')
        assert 403 == self.client.follow()
        assert 'Code 403' in self.client.content

    def test_not_found(self):
        """ Ensure not found page is rendered.
        """
        self.client.go('/en/error/test-not-found')
        assert 404 == self.client.follow()
        assert 'Code 404' in self.client.content

    def test_internal_erros(self):
        """ Ensure internal error page is rendered.
        """
        self.client.go('/en/error/test-internal-error')
        assert 500 == self.client.follow()
        assert 'Code 500' in self.client.content
