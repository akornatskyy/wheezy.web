"""
"""

from datetime import timedelta
from functools import partial

from wheezy.caching.memory import MemoryCache
from wheezy.http.cache import httpcache
from wheezy.http.cacheprofile import CacheProfile
from wheezy.routing import url
from wheezy.web.handlers.base import redirect_handler
from wheezy.web.handlers.file import file_handler
from wheezy.web.handlers.template import template_handler

from error.web.urls import error_urls
from error.web.urls import test_error_urls
from membership.web.urls import membership_urls
from public.web.urls import public_urls


cache = MemoryCache()
httpcache = partial(httpcache, cache=cache)
cache_profile_static = CacheProfile('public',
        duration=timedelta(minutes=15),
        vary_headers=['IF_NONE_MATCH', 'IF_MODIFIED_SINCE'],
        enabled=True)

locale_pattern = '{locale:(en|ru)}/'
locale_defaults = {'locale': 'en'}

all_urls = [
        url('',
            template_handler('public/home.html'),
            locale_defaults,
            name='default'),
        (locale_pattern, public_urls, locale_defaults),
        (locale_pattern, membership_urls, locale_defaults),
        (locale_pattern + 'error/', error_urls, locale_defaults),
        (locale_pattern + 'error/', test_error_urls, locale_defaults),
        url('favicon.ico',
            redirect_handler('static', path='img/favicon.ico')),
        url('static/{path:any}',
            httpcache(
                file_handler(
                    root='content/static/',
                    age=timedelta(hours=1)),
                cache_profile_static),
            name='static')
]
