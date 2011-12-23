"""
"""

from wheezy.http.comp import u

from membership.models import Credential
from membership.repository.contract import IMembershipRepository


class MockFactory(object):

    def __init__(self, context):
        pass

    def membership(self):
        return MembershipRepository()


class MembershipRepository(IMembershipRepository):
    credentials = {
            'demo': u('P@ssw0rd')
    }

    def authenticate(self, credential):
        return credential.password == self.credentials.get(
                credential.username, None)