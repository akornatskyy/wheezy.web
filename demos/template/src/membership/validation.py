"""
"""

from datetime import timedelta

from wheezy.validation import Validator
from wheezy.validation.rules import compare
from wheezy.validation.rules import length
from wheezy.validation.rules import one_of
from wheezy.validation.rules import range
from wheezy.validation.rules import relative_date
from wheezy.validation.rules import required


_ = lambda s: s

credential_validator = Validator({
    'username': [required, length(min=2, max=20)],
    'password': [required, length(min=8, max=12)]
})

account_validator = Validator({
    'email': [required, length(min=6, max=30)],
    'display_name': [required, length(max=30)],
    'account_type': [required, one_of(('user', 'business'))]
})

registration_validator = Validator({
    'credential': credential_validator,
    'account': account_validator,
    'answer': [required, length(min=1, max=20)],
    'questionid': [required, range(min=1, max=3)],
    'date_of_birth': [
        required,
        relative_date(
            min=timedelta(days=-80 * 365),
            max=timedelta(days=-7 * 365))
    ]
})

password_match_validator = Validator({
    'password': [
        compare(
            equal='confirm_password',
            message_template='Passwords do not match.')
    ]
})
