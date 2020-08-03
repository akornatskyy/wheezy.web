""" ``config`` module.
"""

import sqlite3

from wheezy.caching.memory import MemoryCache
from wheezy.caching.patterns import Cached
from wheezy.html.ext.template import WidgetExtension
from wheezy.html.utils import html_escape
from wheezy.template.engine import Engine
from wheezy.template.ext.core import CoreExtension
from wheezy.template.loader import FileLoader
from wheezy.web.templates import WheezyTemplate

cache = MemoryCache()
cached = Cached(cache, time=15 * 60)


def session():
    return sqlite3.connect(
        "guestbook.db", detect_types=sqlite3.PARSE_DECLTYPES
    )


options = {}

# HTTPCacheMiddleware
options.update({"http_cache": cache})


# Template Engine
searchpath = ["templates"]
engine = Engine(
    loader=FileLoader(searchpath),
    extensions=[CoreExtension(), WidgetExtension(),],
)
engine.global_vars.update({"h": html_escape, "s": lambda s: s})
options.update({"render_template": WheezyTemplate(engine)})
