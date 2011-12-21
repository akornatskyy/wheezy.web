"""
"""

from wheezy.core.descriptors import attribute
from wheezy.core.i18n import ref_gettext
from wheezy.validation.mixin import ValidationMixin

from membership.models import Credential
from membership.validation import credential_validator
from membership.service.contract import IMembershipService


class MembershipService(IMembershipService, ValidationMixin):

    def __init__(self, repository, errors, translations):
        self.repository = repository
        self.errors = errors
        self.translations = translations

    @attribute
    def gettext(self):
        return ref_gettext(self.translations['membership'])

    def authenticate(self, credential):
        if not self.validate(credential, credential_validator):
            return False
        if not self.repository.membership.authenticate(credential):
            self.error(self.gettext(
                "The username or password provided is incorrect."))
            return False
        return True
