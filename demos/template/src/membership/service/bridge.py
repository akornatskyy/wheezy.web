"""
"""

from wheezy.core.descriptors import attribute
from wheezy.core.i18n import ref_gettext
from wheezy.validation.mixin import ErrorsMixin

from config import translations
from membership.models import Credential
from membership.models import Registration
from membership.models import account_types


account_types = tuple(dict(account_types).keys())
translations = translations.domains['membership']


class MembershipService(ErrorsMixin):

    def __init__(self, repository, errors, locale):
        self.repository = repository
        self.errors = errors
        self.locale = locale

    @attribute
    def gettext(self):
        return ref_gettext(translations[self.locale])

    @attribute
    def password_questions(self):
        return dict(self.list_password_questions)

    @attribute
    def list_password_questions(self):
        return self.repository.membership.list_password_questions(self.locale)

    def authenticate(self, credential):
        assert isinstance(credential, Credential)
        if not self.repository.membership.authenticate(credential):
            self.error(self.gettext(
                'The username or password provided is incorrect.'))
            return False
        return True

    def roles(self, username):
        return self.repository.membership.user_roles(username)

    def create_account(self, registration):
        assert isinstance(registration, Registration)
        if registration.account.account_type not in account_types:
            self.error(self.gettext(
                'Oops, unsuppored account type.'),
                'account_type')
            return False
        if registration.question_id not in self.password_questions:
            self.error(self.gettext(
                'Oops, unsuppored password question.'),
                'question_id')
            return False
        membership = self.repository.membership
        if membership.has_account(registration.credential.username):
            self.error(self.gettext(
                'The user with such username is already registered. '
                'Please try another.'),
                name='username')
            return False
        if not membership.create_account(registration):
            self.error(self.gettext(
                'The system was unable to create an account for you. '
                'Please try again later.'))
            return False
        return True
