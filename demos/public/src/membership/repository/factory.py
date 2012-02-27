"""
"""

from wheezy.core.descriptors import attribute

from config import MembershipPersistenceFactory as PersistenceFactory
from membership.repository.caching import CachingFactory


class RepositoryFactory(object):

    def __init__(self):
        self.persistence_factory = PersistenceFactory()
        self.caching_factory = CachingFactory()

    @attribute
    def membership(self):
        return self.caching_factory.membership(
                self.persistence_factory.membership())
