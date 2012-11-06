"""
"""

from wheezy.caching import CacheDependency

from config import cache_factory
from membership.repository import keys
from membership.repository.contract import IMembershipRepository


class MembershipRepository(IMembershipRepository):

    def __init__(self, inner):
        self.inner = inner

    def authenticate(self, credential):
        # TODO:
        return self.inner.authenticate(credential)

    def has_account(self, username):
        key = keys.has_account(username)
        #with cache_factory() as c:
        c = cache_factory()
        try:
            c.__enter__()
            result = c.get(key)
        finally:
            c.__exit__(None, None, None)
        if result is None:
            #with cache_factory() as c:
            c = cache_factory()
            try:
                c.__enter__()
                result = self.inner.has_account(username)
                c.set(key, result, time=600, namespace='membership')
            finally:
                c.__exit__(None, None, None)
        return result

    def user_roles(self, username):
        # TODO:
        return self.inner.user_roles(username)

    def create_account(self, registration):
        key = keys.has_account(registration.credential.username)
        #with cache_factory() as c:
        c = cache_factory()
        try:
            c.__enter__()
            c.delete(key, namespace='membership')
        finally:
            c.__exit__(None, None, None)
        return self.inner.create_account(registration)
