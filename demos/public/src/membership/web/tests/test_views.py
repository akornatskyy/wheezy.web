
""" ``test_views`` module.
"""

import unittest

from wheezy.http.functional import WSGIClient

from app import main
from config import options


XSRF_NAME = options['XSRF_NAME']


# region: pages

class SignInPage(object):

    def __init__(self, client):
        assert '- Sign In</title>' in client.content
        assert XSRF_NAME in client.cookies
        self.client = client
        self.form = client.form

    def signin(self, username, password):
        form = self.form
        form.username = username
        form.password = password
        return self.client.submit(form)


# region: mixins

class SignInMixin(object):

    def signin(self, username, password):
        client = self.client
        assert 200 == client.get('/en/signin')
        page = SignInPage(client)
        return page.signin(username, password)


class SignOutMixin(object):

    def signout(self):
        client = self.client
        assert 'Sign out</a>' in client.content
        client.get('/en/signout')
        assert 200 == client.follow()
        assert 'Sign out</a>' not in client.content


# region: test cases

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


class SignOutTestCase(unittest.TestCase, SignInMixin, SignOutMixin):

    def setUp(self):
        self.client = WSGIClient(main)

    def tearDown(self):
        del self.client
        self.client = None

    def test_signout_user(self):
        """ Ensure sigin is successful.
        """
        self.signin('demo', 'P@ssw0rd')
        assert 200 == self.client.follow()
        self.signout()
