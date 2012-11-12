
"""
"""


from wheezy.core.collections import map_values
from wheezy.core.collections import sorted_items
from wheezy.core.i18n import ref_gettext

from config import translations
from membership.repository.samples import db


translations = translations.domains['membership']


class MembershipRepository(object):

    def __init__(self, session):
        # ensure session is entered
        session.cursor()

    def password_questions(self, locale):
        return map_values(ref_gettext(translations[locale]),
                          db['password_question'])

    def list_password_questions(self, locale):
        return tuple(sorted_items(self.password_questions(locale)))

    def account_types(self, locale):
        return map_values(ref_gettext(translations[locale]),
                          db['account_type'])

    def list_account_types(self, locale):
        return tuple(sorted_items(self.account_types(locale)))

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

from wheezy.core.introspection import looks
from membership.repository.contract import IMembershipRepository
assert looks(MembershipRepository).like(IMembershipRepository)
assert looks(IMembershipRepository).like(MembershipRepository)
del looks, IMembershipRepository
