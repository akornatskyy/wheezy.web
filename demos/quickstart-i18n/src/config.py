"""
"""

import logging
import os
import sys

try:  # pragma: nocover
    from ConfigParser import ConfigParser
    config = ConfigParser()
except ImportError:  # pragma: nocover
    from configparser import ConfigParser
    config = ConfigParser(strict=False)

from wheezy.core.collections import defaultdict
from wheezy.core.i18n import TranslationsManager
from wheezy.html.ext.template import WhitespaceExtension
from wheezy.html.ext.template import WidgetExtension
from wheezy.html.utils import format_value
from wheezy.html.utils import html_escape
from wheezy.security.crypto import Ticket
from wheezy.security.crypto.comp import aes128
from wheezy.security.crypto.comp import ripemd160
from wheezy.security.crypto.comp import sha1
from wheezy.security.crypto.comp import sha256
from wheezy.template.engine import Engine
from wheezy.template.ext.core import CoreExtension
from wheezy.template.loader import FileLoader
from wheezy.template.preprocessor import Preprocessor
from wheezy.web.templates import WheezyTemplate
from public import __version__
from tracing import ERROR_REPORT_FORMAT
from tracing import error_report_extra_provider


config.read(os.getenv('CONFIG', 'etc/development.ini'))

mode = config.get('runtime', 'cache')
if mode == 'memory':
    from wheezy.caching import MemoryCache
    cache = MemoryCache()
elif mode == 'memcached':
    from wheezy.core.pooling import EagerPool
    from wheezy.caching.pylibmc import MemcachedClient
    from wheezy.caching.pylibmc import client_factory
    pool = EagerPool(
        lambda: client_factory(config.get('memcached', 'servers').split(';')),
        size=config.getint('memcached', 'pool-size'))
    cache = MemcachedClient(pool)
else:
    raise NotImplementedError(mode)

options = {}

# HTTPCacheMiddleware
options.update({
    'http_cache': cache
})

# HTTPErrorMiddleware
mode = config.get('runtime', 'unhandled')
if mode == 'stderr':
    handler = logging.StreamHandler(sys.stderr)
elif mode == 'mail':
    from logging.handlers import SMTPHandler
    handler = SMTPHandler(
        mailhost=config.get('mail', 'host'),
        fromaddr=config.get('error_report', 'from-addr'),
        toaddrs=config.get('error_report', 'to-addrs').split(';'),
        subject=config.get('error_report', 'subject'))
else:
    raise NotImplementedError(mode)
handler.setFormatter(logging.Formatter(ERROR_REPORT_FORMAT))
handler.setLevel(logging.ERROR)
unhandled_logger = logging.getLogger('unhandled')
unhandled_logger.setLevel(logging.ERROR)
unhandled_logger.addHandler(handler)
options.update({
    'http_errors': defaultdict(lambda: 'http500', {
        # HTTP status code: route name
        400: 'http400',
        403: 'http403',
        404: 'http404',
        500: 'http500',
    }),
    'http_errors_logger': unhandled_logger,
    'http_errors_extra_provider': error_report_extra_provider
})


# Template Engine
def runtime_engine_factory(loader):
    engine = Engine(
        loader=loader,
        extensions=[
            CoreExtension(),
            WidgetExtension(),
            WhitespaceExtension(),
        ])
    engine.global_vars.update({
        'format_value': format_value,
        'h': html_escape,
    })
    return engine

searchpath = ['content/templates']
engine = Engine(
    loader=FileLoader(searchpath),
    extensions=[
        CoreExtension(token_start='#', line_join=None)
    ])
engine.global_vars.update({
    '__version__': __version__
})
engine = Preprocessor(runtime_engine_factory, engine,
                      key_factory=lambda ctx: ctx['locale'])
options.update({
    'render_template': WheezyTemplate(engine)
})

# Security
options.update({
    'ticket': Ticket(
        max_age=config.getint('crypto', 'ticket-max-age'),
        salt=config.get('crypto', 'ticket-salt'),
        cypher=aes128,
        digestmod=ripemd160 or sha256 or sha1,
        options={
            'CRYPTO_ENCRYPTION_KEY': config.get('crypto', 'encryption-key'),
            'CRYPTO_VALIDATION_KEY': config.get('crypto', 'validation-key')
        }),

    'AUTH_COOKIE': '_a',
    'AUTH_COOKIE_DOMAIN': config.get('crypto', 'auth-cookie-domain'),
    'AUTH_COOKIE_PATH': '',
    'AUTH_COOKIE_SECURE': config.getboolean('crypto', 'auth-cookie-secure'),

    'XSRF_NAME': '_x',
    'RESUBMISSION_NAME': '_c'
})

translations = TranslationsManager(
    directories=['i18n'],
    default_lang='en')
options.update({
    'translations_manager': translations
})
