
"""
"""


class IMembershipRepository(object):  # pragma: nocover

    def list_password_questions(self, locale):
        return sorted([])

    def authenticate(self, credential):
        return False

    def has_account(self, username):
        return False

    def user_roles(self, username):
        return tuple([])

    def create_account(self, registration):
        return False
