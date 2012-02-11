"""
"""

from wheezy.routing import url

from membership.web.views import BusinessOnlyHandler
from membership.web.views import MembersOnlyHandler
from membership.web.views import SignInHandler
from membership.web.views import SignOutHandler
from membership.web.views import SignUpHandler


membership_urls = [
    url('signin', SignInHandler, name='signin'),
    url('signout', SignOutHandler, name='signout'),
    url('signup', SignUpHandler, name='signup'),
    url('members-only', MembersOnlyHandler, name='members_only'),
    url('business-only', BusinessOnlyHandler, name='business_only')
]
