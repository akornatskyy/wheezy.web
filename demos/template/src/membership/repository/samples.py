
""" ``samples`` module.
"""

import random

from datetime import date
from wheezy.core.comp import u

from membership.models import Account
from membership.models import Credential
from membership.models import Registration


_ = lambda s: s
next_name = lambda: random.choice(('arnold', 'ben', 'erika', 'bob'))
next_date = lambda: date(random.randint(1947, 1984),
                         random.randint(1, 12),
                         random.randint(1, 28))


def next_credential():
    c = Credential()
    c.username = next_name()
    c.password = 'P@ssw0rd'
    return c


def next_account():
    a = Account()
    a.display_name = 'John Smith'
    a.email = next_name() + '@somewhere.com'
    return a


def next_registration():
    r = Registration()
    r.credential = next_credential()
    r.account = next_account()
    r.date_of_birth = next_date()
    r.questionid = random.randint(1, 3)
    r.answer = random.choice(('1', '7', '9'))
    return r


db = {
    'user': {
        'demo': u('P@ssw0rd'),
        'biz': u('P@ssw0rd')
    },
    'user_role': {
        'demo': ['user'],
        'biz': ['business']
    },
    # the order is set by key
    'password_question': {
        '1': _('Favorite number'),
        '2': _('City of birth'),
        '3': _('Favorite color')
    },
    # honor custom order
    'account_type': (
        ('user', _('User')),
        ('business', _('Business'))
    )
}
