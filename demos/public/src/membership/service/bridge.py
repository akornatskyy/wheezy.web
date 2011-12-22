"""
"""

from wheezy.core.descriptors import attribute
from wheezy.core.i18n import ref_gettext
from wheezy.validation.mixin import ValidationMixin

from membership.models import Credential
from membership.validation import account_validator
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

    @attribute
    def password_questions(self):
        questions = {
                '1': self.gettext('Favorite number'),
                '2': self.gettext('City of birth'),
                '3': self.gettext('Favorite color')
        }
        return questions

    def authenticate(self, credential):
        if not self.validate(credential, credential_validator):
            return False
        if not self.repository.membership.authenticate(credential):
            self.error(self.gettext(
                "The username or password provided is incorrect."))
            return False
        return True

    def create_account(self, registration):
        if (not self.validate(registration.credential, credential_validator)
                & self.validate(registration.account, account_validator)):
            return False
        return True
