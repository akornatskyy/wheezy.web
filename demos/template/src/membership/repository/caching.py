
"""
"""

from config import cache
from membership.repository import keys
from membership.repository.contract import IMembershipRepository


class MembershipRepository(object):

    def __init__(self, inner):
        self.inner = inner

    def password_questions(self, locale):
        # TODO:
        return self.inner.password_questions(locale)

    def list_password_questions(self, locale):
        # TODO:
        return self.inner.list_password_questions(locale)

    def account_types(self, locale):
        # TODO:
        return self.inner.account_types(locale)

    def list_account_types(self, locale):
        # TODO:
        return self.inner.list_account_types(locale)

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


# region: internal details

from wheezy.core.introspection import looks
assert looks(MembershipRepository).like(IMembershipRepository)
assert looks(IMembershipRepository).like(MembershipRepository)
del looks
