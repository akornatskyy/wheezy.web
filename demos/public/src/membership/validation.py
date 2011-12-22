"""
"""

from wheezy.validation.rules import compare
from wheezy.validation.rules import length
from wheezy.validation.rules import required
from wheezy.validation.validator import Validator


_ = lambda s: s

credential_validator = Validator({
    'username': [required, length(min=2, max=20)],
    'password': [required, length(min=8, max=12)]
})

account_validator = Validator({
    'email': [required, length(min=6, max=30)],
    'display_name': [required, length(max=30)]
})

password_match_validator = Validator({
    'password': [compare(equal='confirm_password')]
})
