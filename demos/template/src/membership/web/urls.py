"""
"""

from wheezy.routing import url

from membership.web.views import SignInHandler
from membership.web.views import SignOutHandler
from membership.web.views import SignUpHandler
from membership.web.views import ProfileHandler


membership_urls = [
    url('signin', SignInHandler, name='signin'),
    url('signout', SignOutHandler, name='signout'),
    url('signup', SignUpHandler, name='signup'),
    url('profile', ProfileHandler, name='profile')
]
