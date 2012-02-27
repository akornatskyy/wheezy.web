"""
"""

from wheezy.core.comp import u

from membership.repository.contract import IMembershipRepository


class MockFactory(object):

    def membership(self):
        return MembershipRepository()


class MembershipRepository(IMembershipRepository):
    credentials = {
            'demo': u('P@ssw0rd'),
            'biz': u('P@ssw0rd')
    }
    roles = {
            'demo': tuple(['user']),
            'biz': tuple(['business'])
    }

    def authenticate(self, credential):
        return credential.password == self.credentials.get(
                credential.username, None)

    def has_account(self, username):
        return username in self.credentials

    def user_roles(self, username):
        return self.roles.get(username, None)

    def create_account(self, registration):
        credential = registration.credential
        self.credentials[credential.username] = credential.password
        self.roles[credential.username] = tuple(
                [registration.account.account_type])
        return True
