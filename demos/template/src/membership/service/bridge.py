"""
"""

from wheezy.core.descriptors import attribute
from wheezy.core.i18n import ref_gettext
from wheezy.validation.mixin import ValidationMixin

from membership.models import Credential
from membership.models import Registration
from membership.validation import credential_validator
from membership.validation import registration_validator
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
        return {
            '1': self.gettext('Favorite number'),
            '2': self.gettext('City of birth'),
            '3': self.gettext('Favorite color')
        }

    @attribute
    def account_types(self):
        return {
            'user': self.gettext('User'),
            'business': self.gettext('Business')
        }

    def authenticate(self, credential):
        assert isinstance(credential, Credential)
        if not self.validate(credential, credential_validator):
            return False
        if not self.repository.membership.authenticate(credential):
            self.error(self.gettext(
                "The username or password provided is incorrect."))
            return False
        return True

    def roles(self, username):
        return self.repository.membership.user_roles(username)

    def create_account(self, registration):
        assert isinstance(registration, Registration)
        if not self.validate(registration, registration_validator):
            return False
        membership = self.repository.membership
        if membership.has_account(registration.credential.username):
            self.error(self.gettext(
                "The user with such username is already registered. "
                "Please try another."))
            return False
        if not membership.create_account(registration):
            self.error(self.gettext(
                "The system was unable to create an account for you. "
                "Please try again later."))
            return False
        return True
