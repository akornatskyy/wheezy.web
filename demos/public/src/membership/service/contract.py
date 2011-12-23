"""
"""

from wheezy.core.descriptors import attribute

from membership.models import Credential
from membership.models import Registration


class IMembershipService(object):

    @attribute
    def password_questions(self):
        return {'0': 'None'}

    def authenticate(self, credential):
        assert isinstance(credential, Credential)
        return False

    def create_account(self, registration):
        assert isinstance(registration, Registration)
        return False
