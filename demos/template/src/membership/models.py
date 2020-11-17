"""
"""

from datetime import date


def _(s):
    return s


account_types = (("user", _("User")), ("business", _("Business")))


class Credential(object):
    username = ""
    password = ""


class Account(object):
    email = ""
    display_name = ""
    account_type = "user"


class Registration(object):
    question_id = "0"
    answer = ""
    date_of_birth = date.min

    def __init__(self):
        self.credential = Credential()
        self.account = Account()
