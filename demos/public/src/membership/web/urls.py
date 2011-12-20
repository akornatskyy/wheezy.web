"""
"""

from wheezy.routing import url

from membership.web.views import SignInHandler
from membership.web.views import SignUpHandler


membership_urls = [
    url('signin', SignInHandler, name='signin'),
    url('signup', SignUpHandler, name='signup'),
]
