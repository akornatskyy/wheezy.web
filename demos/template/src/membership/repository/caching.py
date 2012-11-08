
"""
"""

from wheezy.core.introspection import looks

from config import cache
from membership.repository import keys
from membership.repository.contract import IMembershipRepository


class MembershipRepository(object):

    def __init__(self, inner):
        self.inner = inner

    def authenticate(self, credential):
        # TODO:
        return self.inner.authenticate(credential)

    def has_account(self, username):
        key = keys.has_account(username)
        result = cache.get(key)
        if result is None:
            result = self.inner.has_account(username)
            if result is not None:
                cache.set(key, result, time=600, namespace='membership')
        return result

    def user_roles(self, username):
        # TODO:
        return self.inner.user_roles(username)

    def create_account(self, registration):
        key = keys.has_account(registration.credential.username)
        cache.delete(key, namespace='membership')
        return self.inner.create_account(registration)


assert looks(IMembershipRepository).like(MembershipRepository)
