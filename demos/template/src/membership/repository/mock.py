
"""
"""

from wheezy.core.comp import u

from membership.repository.contract import IMembershipRepository


class MembershipRepository(object):

    def __init__(self, session):
        # ensure session is entered
        session.cursor()

    def authenticate(self, credential):
        return credential.password == db['credentials'].get(
            credential.username, None)

    def has_account(self, username):
        return username in db['credentials']

    def user_roles(self, username):
        return tuple(db['roles'].get(username, None))

    def create_account(self, registration):
        credential = registration.credential
        db['credentials'][credential.username] = credential.password
        db['roles'][credential.username] = tuple(
            [registration.account.account_type])
        return True


# region: internal details

db = {
    'credentials': {
        'demo': u('P@ssw0rd'),
        'biz': u('P@ssw0rd')
    },
    'roles': {
    'demo': ['user'],
    'biz': ['business']
    }
}

from wheezy.core.introspection import looks
assert looks(MembershipRepository).like(IMembershipRepository)
assert looks(IMembershipRepository).like(MembershipRepository)
del looks
