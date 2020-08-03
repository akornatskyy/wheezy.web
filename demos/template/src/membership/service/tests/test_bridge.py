""" ``test_bridge`` module.
"""

import unittest

from membership.repository.samples import next_registration
from mock import Mock


class MembershipServiceTestCase(unittest.TestCase):
    def setUp(self):
        from membership.service.bridge import MembershipService

        self.mock_factory = Mock()
        self.service = MembershipService(
            factory=self.mock_factory, errors={}, locale="en"
        )


class CreateAccountTestCase(MembershipServiceTestCase):
    def test_username_is_taken(self):
        """ If username is taken return an error.
        """
        r = next_registration(question_id="1")
        f = self.mock_factory
        f.membership.list_password_questions.return_value = (("1", ""),)
        f.membership.has_account.return_value = True

        assert not self.service.create_account(r)

        assert 1 == len(self.service.errors)
        assert "username" in self.service.errors
        f.membership.has_account.assert_called_once_with(r.credential.username)

    def test_create_account_failed(self):
        """ If repository failed to create an account show a friendly
            message.
        """
        r = next_registration(question_id="1")
        f = self.mock_factory
        f.membership.list_password_questions.return_value = (("1", ""),)
        f.membership.has_account.return_value = True
        f.membership.create_account.return_value = False

        assert not self.service.create_account(r)

        assert 1 == len(self.service.errors)
        assert "username" in self.service.errors
        f.membership.has_account.assert_called_once_with(r.credential.username)

    def test_succeed(self):
        """ The account has been created successfully.
        """
        r = next_registration(question_id="1")
        f = self.mock_factory
        f.membership.list_password_questions.return_value = (("1", ""),)
        f.membership.has_account.return_value = False
        f.membership.create_account.return_value = True

        assert self.service.create_account(r)

        assert not self.service.errors
        f.membership.has_account.assert_called_once_with(r.credential.username)
        f.membership.create_account.assert_called_once_with(r)
