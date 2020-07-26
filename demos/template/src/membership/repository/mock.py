"""
"""

from wheezy.core.i18n import ref_gettext
from wheezy.core.introspection import looks

from config import translations

from membership.repository.contract import IMembershipRepository
from membership.repository.samples import db


translations = translations.domains['membership']


class MembershipRepository(object):

    def __init__(self, session):
        # ensure session is entered
        session.cursor()

    def list_password_questions(self, locale):
        gettext = ref_gettext(translations[locale])
        return tuple((k, gettext(v)) for k, v in db['password_question'])

    def authenticate(self, credential):
        return credential.password == db['user'].get(
            credential.username, None)

    def has_account(self, username):
        return username in db['user']

    def user_roles(self, username):
        return tuple(db['user_role'].get(username, None))

    def create_account(self, registration):
        credential = registration.credential
        db['user'][credential.username] = credential.password
        db['user_role'][credential.username] = tuple(
            [registration.account.account_type])
        return True


# region: internal details
assert looks(MembershipRepository).like(IMembershipRepository)
assert looks(IMembershipRepository).like(MembershipRepository)
del looks, IMembershipRepository
