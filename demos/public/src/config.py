"""
"""

from datetime import timedelta

from wheezy.caching import MemoryCache
from wheezy.core.collections import defaultdict
from wheezy.core.i18n import TranslationsManager
from wheezy.html.ext.mako import widget_preprocessor
from wheezy.http import CacheProfile
from wheezy.http import RequestVary
from wheezy.security.crypto import Ticket
from wheezy.web.templates import MakoTemplate

from membership.repository.mock import MockFactory


cache = MemoryCache()
http_cache = cache
template_cache = cache

# Custom
MembershipPersistenceFactory = MockFactory
membership_cache = cache

options = {}

# HTTPCacheMiddleware
middleware_vary = RequestVary()
options.update({
        'http_cache': http_cache,
        'http_cache_middleware_vary': middleware_vary
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
        middleware_vary=middleware_vary,
        enabled=True)

# HTTPErrorMiddleware
options.update({
        'http_errors': defaultdict(lambda: 'http500', {
            # HTTP status code: route name
            400: 'http400',
            401: 'signin',
            403: 'http403',
            404: 'http404',
            500: 'http500',
        }),
})

# wheezy.security.crypto.Ticket
options.update({
        'CRYPTO_ENCRYPTION_KEY': '4oqiKhW3qzP2EiattMt7',
        'CRYPTO_VALIDATION_KEY': 'A7GfjxIBCBA3vNqvafWf'
})

# BaseHandler
options.update({
        'translations_manager': TranslationsManager(
            directories=['i18n'],
            default_lang='en'),

        'render_template': MakoTemplate(
            directories=['content/templates'],
            filesystem_checks=False,
            template_cache=template_cache,
            preprocessor=[widget_preprocessor]
            ),

        'ticket': Ticket(
            max_age=1200,
            salt='JNbCog95cDTo1NRb7inP',
            options=options),

        'AUTH_COOKIE': '_a',
        'AUTH_COOKIE_DOMAIN': None,
        'AUTH_COOKIE_PATH': '',
        'AUTH_COOKIE_SECURE': False,

        'XSRF_NAME': '_x',
        'RESUBMISSION_NAME': '_c'
})
