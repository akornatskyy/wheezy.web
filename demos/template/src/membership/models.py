"""
"""

from datetime import date

from wheezy.core.comp import u


def _(s):
    return s

account_types = (
    ('user', _('User')),
    ('business', _('Business'))
)


class Credential(object):
    username = u('')
    password = u('')


class Account(object):
    email = u('')
    display_name = u('')
    account_type = 'user'


class Registration(object):
    question_id = '0'
    answer = u('')
    date_of_birth = date.min

    def __init__(self):
        self.credential = Credential()
        self.account = Account()
