"""
"""


class IMembershipRepository(object):

    def authenticate(credential):
        assert isinstance(credential, Credential)
        return False

    def has_account(self, username):
        return False

    def create_account(self, registration):
        return False
