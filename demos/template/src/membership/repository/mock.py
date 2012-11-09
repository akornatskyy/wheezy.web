
"""
"""

from operator import itemgetter

from wheezy.core.comp import u
from wheezy.core.i18n import ref_gettext

from config import translations
from membership.repository.contract import IMembershipRepository


translations = translations.domains['membership']


class MembershipRepository(object):

    def __init__(self, session):
        # ensure session is entered
        session.cursor()

    def password_questions(self, locale):
        gettext = ref_gettext(translations[locale])
        return dict([(key, gettext(value))
                     for key, value in db['password_question'].items()])

    def list_password_questions(self, locale):
        return sorted(self.password_questions(locale).items(),
                      key=itemgetter(1))

    def account_types(self, locale):
        gettext = ref_gettext(translations[locale])
        return dict([(key, gettext(value))
                     for key, value in db['account_type'].items()])

    def list_account_types(self, locale):
        return sorted(self.account_types(locale).items(),
                      key=itemgetter(1))

    def authenticate(self, credential):
        return credential.password == db['user'].get(
            credential.username, None)

    def has_account(self, username):
        return username in db['user']

    def user_roles(self, username):
        return tuple(db['role'].get(username, None))

    def create_account(self, registration):
        credential = registration.credential
        db['user'][credential.username] = credential.password
        db['role'][credential.username] = tuple(
            [registration.account.account_type])
        return True


# region: internal details

db = {
    'user': {
        'demo': u('P@ssw0rd'),
        'biz': u('P@ssw0rd')
    },
    'role': {
        'demo': ['user'],
        'biz': ['business']
    },
    'password_question': {
        '1': 'Favorite number',
        '2': 'City of birth',
        '3': 'Favorite color'
    },
    'account_type': {
        'user': 'User',
        'business': 'Business'
    }
}

from wheezy.core.introspection import looks
assert looks(MembershipRepository).like(IMembershipRepository)
assert looks(IMembershipRepository).like(MembershipRepository)
del looks
