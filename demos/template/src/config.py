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
from wheezy.security.crypto import Ticket
from wheezy.security.crypto.comp import aes128
from wheezy.security.crypto.comp import ripemd160
from wheezy.security.crypto.comp import sha1
from wheezy.security.crypto.comp import sha256

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
        401: 'signin',
        403: 'http403',
        404: 'http404',
        405: 'default',
        500: 'http500',
    }),
    'http_errors_logger': unhandled_logger,
    'http_errors_extra_provider': error_report_extra_provider
})

template_engine = os.getenv('TEMPLATE_ENGINE', 'wheezy.preprocessor')
if template_engine == 'mako':
    from wheezy.html.ext.mako import inline_preprocessor
    from wheezy.html.ext.mako import whitespace_preprocessor
    from wheezy.html.ext.mako import widget_preprocessor
    from wheezy.web.templates import MakoTemplate

    directories = ['content/templates-mako']
    render_template = MakoTemplate(
        module_directory=config.get('mako', 'module-directory'),
        filesystem_checks=config.getboolean('mako', 'filesystem-checks'),
        directories=directories,
        cache=cache,
        preprocessor=[
            inline_preprocessor(directories, config.getboolean(
                'mako', 'inline-preprocessor-fallback')),
            widget_preprocessor,
            whitespace_preprocessor,
        ])
elif template_engine == 'tenjin':
    from wheezy.html.ext.tenjin import inline_preprocessor
    from wheezy.html.ext.tenjin import whitespace_preprocessor
    from wheezy.html.ext.tenjin import widget_preprocessor
    from wheezy.html.utils import format_value
    from wheezy.web.templates import TenjinTemplate

    path = ['content/templates-tenjin']
    render_template = TenjinTemplate(
        path=path,
        pp=[
            inline_preprocessor(path, config.getboolean(
                'tenjin', 'inline-preprocessor-fallback')),
            widget_preprocessor,
            whitespace_preprocessor,
        ],
        helpers={
            'format_value': format_value
        })
elif template_engine == 'jinja2':
    from jinja2 import Environment
    from jinja2 import FileSystemLoader
    from wheezy.html.ext.jinja2 import InlineExtension
    from wheezy.html.ext.jinja2 import WidgetExtension
    from wheezy.html.ext.jinja2 import WhitespaceExtension
    from wheezy.html.utils import format_value
    from wheezy.web.templates import Jinja2Template
    from public import __version__
    searchpath = ['content/templates-jinja2']
    env = Environment(
        loader=FileSystemLoader(searchpath),
        auto_reload=config.getboolean('jinja2', 'auto-reload'),
        extensions=[
            InlineExtension(searchpath, config.getboolean(
                'jinja2', 'inline-preprocessor-fallback')),
            WidgetExtension,
            WhitespaceExtension
        ])
    env.globals.update({
        'format_value': format_value,
        '__version__': __version__
    })
    render_template = Jinja2Template(env)
elif template_engine == 'wheezy.template':
    from wheezy.html.ext.template import InlineExtension
    from wheezy.html.ext.template import WhitespaceExtension
    from wheezy.html.ext.template import WidgetExtension
    from wheezy.html.utils import format_value
    from wheezy.html.utils import html_escape
    from wheezy.template.engine import Engine
    from wheezy.template.ext.core import CoreExtension
    from wheezy.template.loader import autoreload
    from wheezy.template.loader import FileLoader
    from wheezy.web.templates import WheezyTemplate
    from public import __version__
    searchpath = ['content/templates-wheezy']
    engine = autoreload(Engine(
        loader=FileLoader(searchpath),
        extensions=[
            InlineExtension(searchpath, fallback=config.getboolean(
                'wheezy.template', 'inline-preprocessor-fallback')),
            CoreExtension(),
            WidgetExtension(),
            WhitespaceExtension(),
        ]), enabled=config.getboolean('wheezy.template', 'auto-reload'))
    engine.global_vars.update({
        'format_value': format_value,
        'h': html_escape,
        '__version__': __version__
    })
    render_template = WheezyTemplate(engine)
elif template_engine == 'wheezy.preprocessor':
    from wheezy.html.ext.template import WhitespaceExtension
    from wheezy.html.ext.template import WidgetExtension
    from wheezy.html.utils import format_value
    from wheezy.html.utils import html_escape
    from wheezy.template.engine import Engine
    from wheezy.template.ext.core import CoreExtension
    from wheezy.template.loader import autoreload
    from wheezy.template.loader import FileLoader
    from wheezy.template.preprocessor import Preprocessor
    from wheezy.web.templates import WheezyTemplate
    from public import __version__

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

    searchpath = ['content/templates-preprocessor']
    engine = Engine(
        loader=FileLoader(searchpath),
        extensions=[
            CoreExtension('#', line_join=None)
        ])
    engine.global_vars.update({
        '__version__': __version__
    })
    engine = Preprocessor(runtime_engine_factory, engine,
                          key_factory=lambda ctx: ctx['locale'])
    engine = autoreload(engine, enabled=config.getboolean(
        'wheezy.template', 'auto-reload'))
    render_template = WheezyTemplate(engine)

# BaseHandler
translations = TranslationsManager(
    directories=['i18n'],
    default_lang='en')
options.update({
    'translations_manager': translations,
    'render_template': render_template,

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
