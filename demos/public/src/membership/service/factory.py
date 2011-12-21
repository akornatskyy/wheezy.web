"""
"""

from wheezy.core.descriptors import attribute

from membership.repository.factory import RepositoryFactory
from membership.service.bridge import MembershipService


class Factory(object):

    def __init__(self, context):
        self.repository = RepositoryFactory(context)
        self.translations = context['translations']
        self.errors = context['errors']

    @attribute
    def membership(self):
        return MembershipService(
                self.repository.membership,
                self.errors,
                self.translations)
