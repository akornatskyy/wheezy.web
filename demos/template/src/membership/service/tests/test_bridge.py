
""" ``test_bridge`` module.
"""

import unittest

from mock import Mock

from membership.repository.samples import next_registration


class MembershipServiceTestCase(unittest.TestCase):

    def setUp(self):
        from wheezy.core.i18n import TranslationsManager
        from membership.service.bridge import MembershipService
        self.mock_repository = Mock()
        self.service = MembershipService(
            repository=self.mock_repository,
            errors={},
            translations=TranslationsManager()['en'],
            locale='en')


class CreateAccountTestCase(MembershipServiceTestCase):

    def test_validation_errors(self):
        """ Checks for validation errors.
        """
        from membership.models import Registration
        r = Registration()
        assert not self.service.create_account(r)
        assert 7 == len(self.service.errors)

    def test_username_is_taken(self):
        """ If username is taken return an error.
        """
        r = next_registration()
        self.mock_repository.membership.has_account.return_value = True

        assert not self.service.create_account(r)

        assert 1 == len(self.service.errors)
        assert '__ERROR__' in self.service.errors
        self.mock_repository.membership.has_account.assert_called_once_with(
            r.credential.username)

    def test_create_account_failed(self):
        """ If repository failed to create an account show a friendly
            message.
        """
        r = next_registration()
        self.mock_repository.membership.has_account.return_value = False
        self.mock_repository.membership.create_account.return_value = False

        assert not self.service.create_account(r)

        assert 1 == len(self.service.errors)
        assert '__ERROR__' in self.service.errors
        self.mock_repository.membership.has_account.assert_called_once_with(
            r.credential.username)
        self.mock_repository.membership.create_account.assert_called_once_with(
            r)

    def test_succeed(self):
        """ The account has been created successfully.
        """
        r = next_registration()
        self.mock_repository.membership.has_account.return_value = False
        self.mock_repository.membership.create_account.return_value = True

        assert self.service.create_account(r)

        assert not self.service.errors
        self.mock_repository.membership.has_account.assert_called_once_with(
            r.credential.username)
        self.mock_repository.membership.create_account.assert_called_once_with(
            r)
