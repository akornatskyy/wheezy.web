
""" ``test_views`` module.
"""

import unittest

from wheezy.http.functional import WSGIClient

from app import main
from config import options


XSRF_NAME = options['XSRF_NAME']


class SignInMixin(object):

    def signin(self, username, password):
        client = self.client
        assert 200 == client.get('/en/signin')
        assert '- Sign In</title>' in client.content
        assert XSRF_NAME in client.cookies

        form = client.form
        form.username = username
        form.password = password
        return client.submit(form)


class SignInTestCase(unittest.TestCase, SignInMixin):

    def setUp(self):
        self.client = WSGIClient(main)

    def tearDown(self):
        del self.client
        self.client = None

    def test_validation_error(self):
        """ Ensure sigin page displays field validation errors.
        """
        assert 200 == self.signin('', '')
        assert 'class="error"' in self.client.content

    def test_unknown_user(self):
        """ Ensure sigin page displays general error message.
        """
        assert 200 == self.signin('test', 'password')
        assert 'class="error-message"' in self.client.content

    def test_valid_user(self):
        """ Ensure sigin is successful.
        """
        self.signin('demo', 'P@ssw0rd')
        assert 200 == self.client.follow()
        assert 'Welcome <b>demo' in self.client.content
