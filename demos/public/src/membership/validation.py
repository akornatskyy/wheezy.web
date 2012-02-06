"""
"""

from wheezy.validation import Validator
from wheezy.validation.rules import compare
from wheezy.validation.rules import length
from wheezy.validation.rules import required


_ = lambda s: s

credential_validator = Validator({
    'username': [required, length(min=2, max=20)],
    'password': [required, length(min=8, max=12)]
})

account_validator = Validator({
    'email': [required, length(min=6, max=30)],
    'display_name': [required, length(max=30)]
})

registration_validator = Validator({
    'answer': [required, length(min=1, max=20)],
    'date_of_birth': [required]
})

password_match_validator = Validator({
    'password': [
        compare(
            equal='confirm_password',
            message_template='Passwords do not match.')
    ]
})
