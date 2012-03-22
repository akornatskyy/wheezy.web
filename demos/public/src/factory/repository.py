"""
"""

from wheezy.core.descriptors import attribute

from config import MembershipPersistence
from membership.repository.caching import MembershipRepository


class RepositoryFactory(object):

    def __init__(self, session, cache):
        self.session = session
        self.cache = cache

    @attribute
    def membership(self):
        return MembershipRepository(
                MembershipPersistence(self.session),
                self.cache)
