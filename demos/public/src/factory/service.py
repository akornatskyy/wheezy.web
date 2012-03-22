"""
"""

from wheezy.core.descriptors import attribute

from factory.repository import RepositoryFactory
from membership.service.bridge import MembershipService


class Factory(object):

    def __init__(self, context):
        self.repository = RepositoryFactory(self.session, self.cache)
        self.translations = context['translations']
        self.errors = context['errors']

    @property
    def session(self):
        return None

    @property
    def cache(self):
        return None

    @attribute
    def membership(self):
        return MembershipService(
                self.repository,
                self.errors,
                self.translations)
