"""
"""

from membership.repository import keys
from membership.repository.contract import IMembershipRepository


class MembershipRepository(IMembershipRepository):

    def __init__(self, inner, cache):
        self.inner = inner
        self.cache = cache

    def authenticate(self, credential):
        key = keys.authenticate(credential.username)
        # TODO:
        return self.inner.authenticate(credential)

    def has_account(self, username):
        # TODO:
        return self.inner.has_account(username)

    def user_roles(self, username):
        # TODO:
        return self.inner.user_roles(username)

    def create_account(self, registration):
        # TODO:
        return self.inner.create_account(registration)