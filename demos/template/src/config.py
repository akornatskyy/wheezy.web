"""
"""

from datetime import timedelta

from wheezy.caching import MemoryCache
from wheezy.core.collections import defaultdict
from wheezy.core.i18n import TranslationsManager
from wheezy.html.ext.mako import widget_preprocessor
from wheezy.html.ext.mako import whitespace_preprocessor
from wheezy.http import CacheProfile
from wheezy.security.crypto import Ticket
from wheezy.web.templates import MakoTemplate

from membership.repository.mock import MembershipRepository


cache = MemoryCache()
cache_factory = lambda: cache


# Custom
MembershipPersistence = MembershipRepository

options = {}

# HTTPCacheMiddleware
options.update({
        'http_cache_factory': cache_factory
})

# Cache Profiles
none_cache_profile = CacheProfile(
        'none',
        no_store=True,
        enabled=True)
static_cache_profile = CacheProfile(
        'public',
        duration=timedelta(minutes=15),
        vary_environ=['HTTP_ACCEPT_ENCODING'],
        namespace='static',
        enabled=True)
public_cache_profile = CacheProfile(
        'server',
        duration=timedelta(minutes=15),
        vary_environ=['HTTP_ACCEPT_ENCODING'],
        vary_cookies=['_a'],
        no_store=True,
        enabled=False)

# HTTPErrorMiddleware
options.update({
        'http_errors': defaultdict(lambda: 'http500', {
            # HTTP status code: route name
            400: 'http400',
            401: 'signin',
            403: 'http403',
            404: 'http404',
            405: 'default',
            500: 'http500',
        }),
})

# wheezy.security.crypto.Ticket
options.update({
        'CRYPTO_ENCRYPTION_KEY': 'r0sWsYR3dHUcrPWeTcB7',
        'CRYPTO_VALIDATION_KEY': 'kTrdyg9ZwcNyE6YKoPJU'
})

# BaseHandler
options.update({
        'translations_manager': TranslationsManager(
            directories=['i18n'],
            default_lang='en'),

        'render_template': MakoTemplate(
            directories=['content/templates'],
            filesystem_checks=False,
            cache_factory=cache_factory,
            preprocessor=[
                widget_preprocessor,
                whitespace_preprocessor,
            ]),

        'ticket': Ticket(
            max_age=1200,
            salt='WmMFjzVbSpWlCKb6cOC4',
            options=options),

        'AUTH_COOKIE': '_a',
        'AUTH_COOKIE_DOMAIN': None,
        'AUTH_COOKIE_PATH': '',
        'AUTH_COOKIE_SECURE': False,

        'XSRF_NAME': '_x',
        'RESUBMISSION_NAME': '_c'
})
