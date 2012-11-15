
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
    def password_questions(self, locale):
        return self.inner.password_questions(locale)

    @cached
    def list_password_questions(self, locale):
        return self.inner.list_password_questions(locale)

    @cached
    def account_types(self, locale):
        return self.inner.account_types(locale)

    @cached
    def list_account_types(self, locale):
        return self.inner.list_account_types(locale)

    def authenticate(self, credential):
        # TODO:
        return self.inner.authenticate(credential)

    def has_account(self, username):
        #key = keys.has_account(username)
        #result = cache.get(key)
        #if result is None:
        #    result = self.inner.has_account(username)
        #    if result is not None:
        #        cache.set(key, result, time=3600, namespace='membership')
        #return result
        return cached_long.get_or_set(
            keys.has_account(username),
            lambda: self.inner.has_account(username))

    def user_roles(self, username):
        # TODO:
        return self.inner.user_roles(username)

    def create_account(self, registration):
        cached.delete(keys.has_account(registration.credential.username))
        return self.inner.create_account(registration)


# region: internal details

from wheezy.core.introspection import looks
from membership.repository.contract import IMembershipRepository
ignore_argspec = [
    'password_questions', 'list_password_questions',
    'account_types', 'list_account_types']
assert looks(MembershipRepository).like(
    IMembershipRepository, ignore_argspec=ignore_argspec)
assert looks(IMembershipRepository).like(
    MembershipRepository, ignore_argspec=ignore_argspec)
del looks, IMembershipRepository, ignore_argspec
