"""
"""

from membership.web.views import (
    ProfileHandler,
    SignInHandler,
    SignOutHandler,
    SignUpHandler,
)

from wheezy.routing import url

membership_urls = [
    url("signin", SignInHandler, name="signin"),
    url("signout", SignOutHandler, name="signout"),
    url("signup", SignUpHandler, name="signup"),
    url("profile", ProfileHandler, name="profile"),
]
