"""
"""

from wheezy.core.comp import u

from membership.repository.contract import IMembershipRepository


class MembershipRepository(IMembershipRepository):
    credentials = {
        'demo': u('P@ssw0rd'),
        'biz': u('P@ssw0rd')
    }
    roles = {
        'demo': ['user'],
        'biz': ['business']
    }

    def __init__(self, session):
        # ensure session is entered
        session.cursor()

    def authenticate(self, credential):
        return credential.password == self.credentials.get(
            credential.username, None)

    def has_account(self, username):
        return username in self.credentials

    def user_roles(self, username):
        return tuple(self.roles.get(username, None))

    def create_account(self, registration):
        credential = registration.credential
        self.credentials[credential.username] = credential.password
        self.roles[credential.username] = tuple(
            [registration.account.account_type])
        return True
