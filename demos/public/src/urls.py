"""
"""

from datetime import timedelta

from wheezy.http.cache import httpcache
from wheezy.http.cacheprofile import CacheProfile
from wheezy.routing import url
from wheezy.web.handlers.file import file_handler
from wheezy.web.handlers.template import template_handler

from config import cache
from config import middleware_vary
from error.web.urls import error_urls
from error.web.urls import test_error_urls
from membership.web.urls import membership_urls
from public.web.urls import public_urls


locale_pattern = '{locale:(en|ru)}/'
locale_defaults = {'locale': 'en'}
static_files = httpcache(
        file_handler(
            root='content/static/',
            age=timedelta(hours=1)),
        cache_profile=CacheProfile(
            'public',
            duration=timedelta(minutes=15),
            middleware_vary=middleware_vary,
            enabled=True),
        cache=cache)

all_urls = [
        url('',
            template_handler('public/home.html'),
            locale_defaults,
            name='default'),
        (locale_pattern, public_urls, locale_defaults),
        (locale_pattern, membership_urls, locale_defaults),
        (locale_pattern + 'error/', error_urls, locale_defaults),
        (locale_pattern + 'error/', test_error_urls, locale_defaults),
        url('static/{path:any}', static_files, name='static'),
        url('favicon.ico', static_files, {'path': 'img/favicon.ico'})
]
