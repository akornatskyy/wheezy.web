"""
"""

from ConfigParser import ConfigParser
from datetime import timedelta

from wheezy.caching import MemoryCache
from wheezy.core.collections import defaultdict
from wheezy.core.i18n import TranslationsManager
from wheezy.html.ext.mako import widget_preprocessor
from wheezy.html.ext.mako import whitespace_preprocessor
from wheezy.http import CacheProfile
from wheezy.security.crypto import Ticket
from wheezy.security.crypto.comp import aes128
from wheezy.security.crypto.comp import ripemd160
from wheezy.security.crypto.comp import sha1
from wheezy.security.crypto.comp import sha256
from wheezy.web.templates import MakoTemplate

from membership.repository.mock import MembershipRepository


config = ConfigParser()
config.read('development.ini')

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
        enabled=config.getboolean('cache-profile', 'static-enabled'))
public_cache_profile = CacheProfile(
        'server',
        duration=timedelta(minutes=15),
        vary_environ=['HTTP_ACCEPT_ENCODING'],
        vary_cookies=['_a'],
        no_store=True,
        enabled=config.getboolean('cache-profile', 'public-enabled'))

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
        'CRYPTO_ENCRYPTION_KEY': config.get('crypto', 'encryption-key'),
        'CRYPTO_VALIDATION_KEY': config.get('crypto', 'validation-key')
})

# BaseHandler
options.update({
        'translations_manager': TranslationsManager(
            directories=['i18n'],
            default_lang='en'),

        'render_template': MakoTemplate(
            module_directory=config.get('mako', 'module-directory'),
            filesystem_checks=config.getboolean('mako', 'filesystem-checks'),
            directories=['content/templates'],
            cache_factory=cache_factory,
            preprocessor=[
                widget_preprocessor,
                whitespace_preprocessor,
            ]),

        'ticket': Ticket(
            max_age=config.getint('crypto', 'ticket-max-age'),
            salt=config.get('crypto', 'ticket-salt'),
            cypher=aes128,
            digestmod=ripemd160 or sha256 or sha1,
            options=options),

        'AUTH_COOKIE': '_a',
        'AUTH_COOKIE_DOMAIN': None,
        'AUTH_COOKIE_PATH': '',
        'AUTH_COOKIE_SECURE': False,

        'XSRF_NAME': '_x',
        'RESUBMISSION_NAME': '_c'
})
