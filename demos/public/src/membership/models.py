"""
"""

from datetime import date

from wheezy.core.comp import u


class Credential(object):

    def __init__(self):
        self.username = u('')
        self.password = u('')


class Account(object):

    def __init__(self):
        self.email = u('')
        self.display_name = u('')
        self.account_type = 'user'


class Registration(object):

    def __init__(self):
        self.credential = Credential()
        self.account = Account()
        self.questionid = 0
        self.answer = u('')
        self.date_of_birth = date.min
