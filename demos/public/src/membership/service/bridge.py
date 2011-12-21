"""
"""

from membership.models import Credential
from membership.validation import credential_validator
from membership.service.contract import IMembershipService


class ServiceBase(object):

    def __init__(self, errors, translations):
        self.validation_translations = translations['validation']
        self.errors = errors

    def error(self, message):
        self.errors.setdefault('__ERROR__', []).append(message)

    def validate(self, model, validator):
        return validator.validate(
                model=model,
                results=self.errors,
                translations=self.validation_translations)


class MembershipService(ServiceBase, IMembershipService):

    def __init__(self, membership_repository, errors, translations):
        super(MembershipService, self).__init__(errors, translations)
        self.membership_repository = membership_repository

    def gettext(self, message):
        return message

    def authenticate(self, credential):
        if not self.validate(credential, credential_validator):
            return False
        if not self.membership_repository.authenticate(credential):
            self.error(self.gettext(
                "The username or password provided is incorrect."))
            return False
        return True
