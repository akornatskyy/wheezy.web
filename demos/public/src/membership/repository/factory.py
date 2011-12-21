"""
"""

from wheezy.core.descriptors import attribute

from membership.repository.caching import CachingFactory


class RepositoryFactory(object):

    def __init__(self, context):
        PersistenceFactory = context['membership']
        self.persistence_factory = PersistenceFactory(context)
        self.caching_factory = CachingFactory(context)

    @attribute
    def membership(self):
        return self.caching_factory.membership(
                self.persistence_factory.membership())
