"""
"""


class IMembershipRepository(object):  # pragma: nocover

    def authenticate(credential):
        assert isinstance(credential, Credential)
        return False

    def has_account(self, username):
        return False

    def user_roles(self, username):
        return tuple([])

    def create_account(self, registration):
        return False
