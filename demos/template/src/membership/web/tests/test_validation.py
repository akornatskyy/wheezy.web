
""" ``test_validation`` module.
"""

import unittest

from wheezy.validation.checker import Checker


class CredentialValidatorTestCase(unittest.TestCase):

    def setUp(self):
        from membership.validation import credential_validator
        self.c = Checker(gettext=lambda t: str(t))
        self.c.use(credential_validator)

    def test_username(self):
        assert not self.c.error(username='johh')

        e = 'Required field cannot be left blank.'
        assert e == self.c.error(username='')
        e = 'Required to be a minimum of 2 characters in length.'
        assert e == self.c.error(username='x')
        e = 'Exceeds maximum length of 20.'
        assert e == self.c.error(username='x' * 21)

    def test_password(self):
        assert not self.c.error(password='P@ssw0rd')

        e = 'Required field cannot be left blank.'
        assert e == self.c.error(password='')
        e = 'Required to be a minimum of 8 characters in length.'
        assert e == self.c.error(password='x' * 7)
        e = 'Exceeds maximum length of 12.'
        assert e == self.c.error(password='x' * 13)


class AccountValidatorTestCase(unittest.TestCase):

    def setUp(self):
        from membership.validation import account_validator
        self.c = Checker(gettext=lambda t: str(t))
        self.c.use(account_validator)

    def test_email(self):
        assert not self.c.error(email='johh@somewhere.net')

        e = 'Required field cannot be left blank.'
        assert e == self.c.error(email='')
        e = 'Required to be a minimum of 6 characters in length.'
        assert e == self.c.error(email='x' * 5)
        e = 'Exceeds maximum length of 30.'
        assert e == self.c.error(email='x' * 31)
        e = 'Required to be a valid email address.'
        assert e == self.c.error(email='x@somewhere')

    def test_account_type(self):
        for account_type in ('user', 'business'):
            assert not self.c.error(account_type=account_type)

        e = 'Required field cannot be left blank.'
        assert e == self.c.error(account_type='')
        e = 'The value does not belong to the list of known items.'
        assert e == self.c.error(account_type='x')


class PasswordMatchValidatorTestCase(unittest.TestCase):

    def setUp(self):
        self.c = Checker(gettext=lambda t: str(t))
        self.c.use('membership.validation.password_match_validator')

    def test_password(self):
        assert not self.c.error(password='x', confirm_password='x')

        e = 'Passwords do not match.'
        assert e == self.c.error(password='x', confirm_password='')
