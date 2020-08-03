"""
"""

from datetime import timedelta

from membership.rules import identity, password_rules

from wheezy.validation import Validator
from wheezy.validation.rules import (
    compare,
    email,
    length,
    one_of,
    relative_date,
    required,
)


def _(s):
    return s


credential_validator = Validator(
    {
        "username": [required, length(min=2), length(max=20)],
        "password": password_rules,
    }
)

account_validator = Validator(
    {
        "email": [required, length(min=6), length(max=30), email],
        "display_name": [required, length(max=30)],
        "account_type": [required, one_of(("user", "business"))],
    }
)

registration_validator = Validator(
    {
        "credential": credential_validator,
        "account": account_validator,
        "answer": [required, length(min=1, max=20)],
        "question_id": [required, identity(max=3)],
        "date_of_birth": [
            required,
            relative_date(
                min=timedelta(days=-80 * 365), max=timedelta(days=-7 * 365)
            ),
        ],
    }
)

password_match_validator = Validator(
    {
        "password": [
            compare(
                equal="confirm_password",
                message_template="Passwords do not match.",
            )
        ]
    }
)
