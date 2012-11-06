"""
"""

from wheezy.core.descriptors import attribute

from membership.models import Credential
from membership.models import Registration


class IMembershipService(object):  # pragma: nocover

    @attribute
    def password_questions(self):
        return {'0': 'None'}

    @attribute
    def list_password_questions(self):
        return [('0', 'None')]

    @attribute
    def account_types(self):
        return {'0': 'None'}

    @attribute
    def list_account_types(self):
        return [('0', 'None')]

    def authenticate(self, credential):
        assert isinstance(credential, Credential)
        return False

    def roles(self, username):
        return tuple([])

    def create_account(self, registration):
        assert isinstance(registration, Registration)
        return False
