""" ``config`` module.
"""

import sqlite3

from wheezy.caching import MemoryCache
from wheezy.html.ext.mako import widget_preprocessor
from wheezy.web.templates import MakoTemplate


cache = MemoryCache()
cache_factory = lambda: cache


def session():
    return sqlite3.connect('guestbook.db',
        detect_types=sqlite3.PARSE_DECLTYPES)


options = {
        'render_template': MakoTemplate(
            directories=['templates'],
            filesystem_checks=False,
            preprocessor=[widget_preprocessor]
        )
}

# HTTPCacheMiddleware
options.update({
        'http_cache_factory': cache_factory
})
