
""" ``test_views`` module.
"""

import unittest

from wheezy.http.functional import WSGIClient

from app import main
from config import options


AUTH_COOKIE = options['AUTH_COOKIE']
XSRF_NAME = options['XSRF_NAME']
RESUBMISSION_NAME = options['RESUBMISSION_NAME']


# region: pages

class SignInPage(object):

    def __init__(self, client):
        assert '- Sign In</title>' in client.content
        assert AUTH_COOKIE not in client.cookies
        assert XSRF_NAME in client.cookies
        self.client = client
        self.form = client.form

    def signin(self, username, password):
        form = self.form
        form.username = username
        form.password = password
        self.client.submit(form)
        return self.client.form.errors()


class SignUpPage(object):

    def __init__(self, client):
        assert '- Sign Up</title>' in client.content
        assert AUTH_COOKIE not in client.cookies
        assert RESUBMISSION_NAME in client.cookies
        self.client = client
        self.form = client.form

    def signup(self, **kwargs):
        form = self.form
        form.update(kwargs)
        self.client.submit(form)
        return self.client.form.errors()


# region: mixins

class SignInMixin(object):

    def signin(self, username, password):
        client = self.client
        assert 200 == client.get('/en/signin')
        page = SignInPage(client)
        return page.signin(username, password)


class SignUpMixin(object):

    def signup(self, **kwargs):
        client = self.client
        assert 200 == client.get('/en/signup')
        page = SignUpPage(client)
        return page.signup(**kwargs)


class SignOutMixin(object):

    def signout(self):
        client = self.client
        assert AUTH_COOKIE in self.client.cookies
        assert 'Sign out</a>' in client.content
        client.get('/en/signout')
        assert 200 == client.follow()
        assert AUTH_COOKIE not in self.client.cookies
        assert 'Sign out</a>' not in client.content


# region: test cases

class MembershipTestCase(unittest.TestCase):

    def setUp(self):
        self.client = WSGIClient(main)

    def tearDown(self):
        del self.client
        self.client = None

    def test_signin(self):
        """ Ensure signin page is rendered
        """
        assert 200 == self.client.go('/en/signin')
        assert '- Sign In</title>' in self.client.content

    def test_signup(self):
        """
        """
        assert 200 == self.client.go('/en/signup')
        assert '- Sign Up</title>' in self.client.content

    def test_signout(self):
        """
        """
        assert 302 == self.client.go('/en/signout')


class SignInTestCase(unittest.TestCase, SignInMixin):

    def setUp(self):
        self.client = WSGIClient(main)

    def tearDown(self):
        del self.client
        self.client = None

    def test_validation_error(self):
        """ Ensure sigin page displays field validation errors.
        """
        errors = self.signin('', '')
        assert 2 == len(errors)
        assert AUTH_COOKIE not in self.client.cookies
        assert 'class="error"' in self.client.content

    def test_unknown_user(self):
        """ Ensure sigin page displays general error message.
        """
        errors = self.signin('test', 'password')
        assert not errors
        assert AUTH_COOKIE not in self.client.cookies
        assert 'class="error-message"' in self.client.content

    def test_valid_user(self):
        """ Ensure sigin is successful.
        """
        self.signin('demo', 'P@ssw0rd')
        assert 200 == self.client.follow()
        assert AUTH_COOKIE in self.client.cookies
        assert XSRF_NAME not in self.client.cookies
        assert 'Welcome <b>demo' in self.client.content

    def test_if_authenticated_redirect(self):
        """ If user is already authenticated redirect
            to default page.
        """
        self.signin('demo', 'P@ssw0rd')
        assert 200 == self.client.follow()
        self.client.get('/en/signin')
        assert 200 == self.client.follow()

    def test_xrsf_token_invalid(self):
        client = self.client
        assert 200 == client.get('/en/signin')
        page = SignInPage(client)
        client.cookies.clear()
        page.signin('', '')
        assert 200 == client.follow()
        SignInPage(client)


class SignOutTestCase(unittest.TestCase, SignInMixin, SignOutMixin):

    def setUp(self):
        self.client = WSGIClient(main)

    def tearDown(self):
        del self.client
        self.client = None

    def test_signout_user(self):
        """ Ensure sigout is successful.
        """
        self.signin('demo', 'P@ssw0rd')
        assert 200 == self.client.follow()
        self.signout()


class SignUpTestCase(unittest.TestCase, SignInMixin, SignUpMixin):

    def setUp(self):
        self.client = WSGIClient(main)

    def tearDown(self):
        del self.client
        self.client = None

    def test_validation_error(self):
        """ Ensure signup page displays field validation errors.
        """
        errors = self.signup()
        assert 6 == len(errors)
        assert AUTH_COOKIE not in self.client.cookies
        assert 'class="error"' in self.client.content

    def test_already_registered(self):
        """ Ensure signup page displays general error message.
        """
        errors = self.signup(
            username='demo',
            display_name='Demo',
            email='demo@somewhere.com',
            date_of_birth='1984/11/14',
            password='P@ssw0rd',
            confirm_password='P@ssw0rd',
            answer='7')
        assert not errors
        assert AUTH_COOKIE not in self.client.cookies
        assert 'class="error-message"' in self.client.content

    def test_registration_succeed(self):
        """ Ensure if all supplied information is valid than
            user is registered and logged in.
        """
        errors = self.signup(
            username='john',
            display_name='John Smith',
            email='john@somewhere.com',
            date_of_birth='1987/2/7',
            password='P@ssw0rd',
            confirm_password='P@ssw0rd',
            answer='7')
        assert not errors
        assert 200 == self.client.follow()
        assert AUTH_COOKIE in self.client.cookies
        assert RESUBMISSION_NAME not in self.client.cookies
        assert 'Welcome <b>John Smith' in self.client.content

    def test_if_authenticated_redirect(self):
        """ If user is already authenticated redirect
            to default page.
        """
        self.signin('demo', 'P@ssw0rd')
        assert 200 == self.client.follow()
        self.client.get('/en/signup')
        assert 200 == self.client.follow()

    def test_resubmission_token_invalid(self):
        client = self.client
        assert 200 == client.get('/en/signup')
        page = SignUpPage(client)
        client.cookies[RESUBMISSION_NAME] = '100'
        page.signup()
        SignUpPage(client)
