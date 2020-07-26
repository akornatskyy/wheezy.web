"""
"""

from wheezy.caching.patterns import Cached
from wheezy.caching.patterns import key_builder

from config import cache

from membership.repository import keys


kb = key_builder(key_prefix='mbr')
cached = Cached(cache, kb, time=3600 * 24, namespace='membership')
cached_long = Cached(cache, kb, time=3600, namespace='membership')


class MembershipRepository(object):

    def __init__(self, inner):
        self.inner = inner

    @cached
    def list_password_questions(self, locale):
        return self.inner.list_password_questions(locale)

    def authenticate(self, credential):
        # TODO:
        return self.inner.authenticate(credential)

    def has_account(self, username):
        # key = keys.has_account(username)
        # result = cache.get(key)
        # if result is None:
        #    result = self.inner.has_account(username)
        #    if result is not None:
        #        cache.set(key, result, time=3600, namespace='membership')
        # return result
        return cached_long.get_or_set(
            keys.has_account(username),
            lambda: self.inner.has_account(username))

    def user_roles(self, username):
        # TODO:
        return self.inner.user_roles(username)

    def create_account(self, registration):
        cached.delete(keys.has_account(registration.credential.username))
        return self.inner.create_account(registration)
