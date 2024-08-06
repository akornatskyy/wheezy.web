"""
"""

import logging
import os
import sys
from datetime import timedelta

try:  # pragma: nocover
    from ConfigParser import ConfigParser

    config = ConfigParser()
except ImportError:  # pragma: nocover
    from configparser import ConfigParser

    config = ConfigParser(strict=False)

from public import __version__
from tracing import ERROR_REPORT_FORMAT, error_report_extra_provider
from wheezy.caching.logging import OnePassHandler
from wheezy.core.collections import defaultdict
from wheezy.html.ext.template import WhitespaceExtension, WidgetExtension
from wheezy.html.utils import format_value, html_escape
from wheezy.security.crypto import Ticket
from wheezy.security.crypto.comp import aes128, sha1, sha256, sha512
from wheezy.template.engine import Engine
from wheezy.template.ext.core import CoreExtension
from wheezy.template.loader import FileLoader, PreprocessLoader

from wheezy.web.templates import WheezyTemplate

root_dir = os.path.join(os.path.dirname(__file__), "..")
config.read(
    os.getenv(
        "CONFIG",
        os.path.join(root_dir, "etc/development.ini"),
    )
)

mode = config.get("runtime", "cache")
if mode == "memory":
    from wheezy.caching import MemoryCache

    cache = MemoryCache()
elif mode == "memcached":
    from wheezy.caching.pylibmc import MemcachedClient, client_factory
    from wheezy.core.pooling import EagerPool

    pool = EagerPool(
        lambda: client_factory(config.get("memcached", "servers").split(";")),
        size=config.getint("memcached", "pool-size"),
    )
    cache = MemcachedClient(pool)
else:
    raise NotImplementedError(mode)

options = {}

# HTTPCacheMiddleware
options.update({"http_cache": cache})

# HTTPErrorMiddleware
mode = config.get("runtime", "unhandled")
if mode == "stderr":
    handler = logging.StreamHandler(sys.stderr)
elif mode == "mail":
    from logging.handlers import SMTPHandler

    handler = SMTPHandler(
        mailhost=config.get("mail", "host"),
        fromaddr=config.get("error_report", "from-addr"),
        toaddrs=config.get("error_report", "to-addrs").split(";"),
        subject=config.get("error_report", "subject"),
    )
else:
    raise NotImplementedError(mode)
handler.setFormatter(logging.Formatter(ERROR_REPORT_FORMAT))
handler = OnePassHandler(handler, cache, timedelta(hours=12))
handler.setLevel(logging.ERROR)
unhandled_logger = logging.getLogger("unhandled")
unhandled_logger.setLevel(logging.ERROR)
unhandled_logger.addHandler(handler)
options.update(
    {
        "http_errors": defaultdict(
            lambda: "http500",
            {
                # HTTP status code: route name
                400: "http400",
                403: "http403",
                404: "http404",
                500: "http500",
            },
        ),
        "http_errors_logger": unhandled_logger,
        "http_errors_extra_provider": error_report_extra_provider,
    }
)

# Template Engine
searchpath = [os.path.join(root_dir, "content/templates")]
engine = Engine(
    loader=FileLoader(searchpath), extensions=[CoreExtension(token_start="#")]
)
engine.global_vars.update({"__version__": __version__})
engine = Engine(
    loader=PreprocessLoader(engine),
    extensions=[
        CoreExtension(),
        WidgetExtension(),
        WhitespaceExtension(),
    ],
)
engine.global_vars.update({"format_value": format_value, "h": html_escape})
options.update({"render_template": WheezyTemplate(engine)})

# Security
options.update(
    {
        "ticket": Ticket(
            max_age=config.getint("crypto", "ticket-max-age"),
            salt=config.get("crypto", "ticket-salt"),
            cypher=aes128,
            digestmod=sha512 or sha256 or sha1,
            options={
                "CRYPTO_ENCRYPTION_KEY": config.get(
                    "crypto", "encryption-key"
                ),
                "CRYPTO_VALIDATION_KEY": config.get(
                    "crypto", "validation-key"
                ),
            },
        ),
        "AUTH_COOKIE": "_a",
        "AUTH_COOKIE_DOMAIN": config.get("crypto", "auth-cookie-domain"),
        "AUTH_COOKIE_PATH": "",
        "AUTH_COOKIE_SECURE": config.getboolean(
            "crypto", "auth-cookie-secure"
        ),
        "XSRF_NAME": "_x",
        "RESUBMISSION_NAME": "_c",
    }
)
