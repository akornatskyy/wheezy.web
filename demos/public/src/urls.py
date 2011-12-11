"""
"""

from datetime import timedelta
from functools import partial

from wheezy.caching.memory import MemoryCache
from wheezy.http.cache import httpcache
from wheezy.http.cacheprofile import CacheProfile
from wheezy.routing import url
from wheezy.web.handlers.file import file_handler
from wheezy.web.handlers.template import template_handler

from public.web.urls import public_urls


cache = MemoryCache()
httpcache = partial(httpcache, cache=cache)
cache_profile_static = CacheProfile('public',
        duration=timedelta(minutes=15),
        vary_headers=['IF_NONE_MATCH', 'IF_MODIFIED_SINCE'],
        enabled=True)


all_urls = [
        url('',
            template_handler('public/home.html'),
            {'locale': 'en'},
            name='default'),
        url('static/{path:any}',
            httpcache(
                file_handler(
                    root='content/static/',
                    age=timedelta(hours=1)),
                cache_profile_static),
            name='static'),
        ('{locale}/', public_urls, {'locale': 'en'})
]
