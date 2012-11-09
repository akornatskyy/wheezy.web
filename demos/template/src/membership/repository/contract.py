
"""
"""

from wheezy.core.descriptors import attribute


class IMembershipRepository(object):  # pragma: nocover

    def password_questions(self, locale):
        return {}

    def list_password_questions(self, locale):
        return sorted([])

    def account_types(self, locale):
        return {}

    def list_account_types(self, locale):
        return sorted([])

    def authenticate(self, credential):
        assert isinstance(credential, Credential)
        return False

    def has_account(self, username):
        return False

    def user_roles(self, username):
        return tuple([])

    def create_account(self, registration):
        return False
