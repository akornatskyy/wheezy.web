"""
"""

from wheezy.validation.rules import length
from wheezy.validation.rules import required
from wheezy.validation.validator import Validator


credential_validator = Validator({
    'username': [required, length(min=4, max=20)],
    'password': [required, length(min=6, max=12)]
})
