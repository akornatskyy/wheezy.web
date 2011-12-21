"""
"""

from membership.models import Credential


class IMembershipService(object):

    def authenticate(self, credential):
        assert isinstance(credential, Credential)
        return False
