"""
"""

from wheezy.core.comp import u
from wheezy.core.introspection import looks

from membership.repository.contract import IMembershipRepository


class MembershipRepository(object):

    def __init__(self, session):
        # ensure session is entered
        session.cursor()

    def authenticate(self, credential):
        return credential.password == credentials.get(
            credential.username, None)

    def has_account(self, username):
        return username in credentials

    def user_roles(self, username):
        return tuple(roles.get(username, None))

    def create_account(self, registration):
        credential = registration.credential
        credentials[credential.username] = credential.password
        roles[credential.username] = tuple(
            [registration.account.account_type])
        return True


# region: internal details

credentials = {
    'demo': u('P@ssw0rd'),
    'biz': u('P@ssw0rd')
}
roles = {
    'demo': ['user'],
    'biz': ['business']
}

assert looks(IMembershipRepository).like(MembershipRepository)
