"""
"""

from wheezy.core.descriptors import attribute

from membership.repository.caching import MembershipRepository
from membership.service.bridge import MembershipService


class Factory(object):

    def __init__(self, session_name, **context):
        self.context = context
        self.session = sessions[session_name]()
        self.factory = RepositoryFactory(self.session)

    def __enter__(self):
        self.session.__enter__()
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.session.__exit__(exc_value, exc_value, traceback)

    @attribute
    def membership(self):
        context = self.context
        return MembershipService(self.factory,
                                 context['errors'],
                                 context['locale'])


class RepositoryFactory(object):

    def __init__(self, session):
        self.session = session

    @attribute
    def membership(self):
        return MembershipRepository(MembershipPersistence(self.session))


# region: configuration details

from config import mode

if mode == 'mock':
    from wheezy.core.db import NullSession
    from membership.repository.mock import MembershipRepository \
        as MembershipPersistence
    sessions = {'ro': NullSession, 'rw': NullSession}
else:
    raise NotImplementedError(mode)
del mode
