"""
"""

from datetime import timedelta

from wheezy.http.cache import httpcache
from wheezy.http.transforms import gzip_transform
from wheezy.http.transforms import response_transforms
from wheezy.routing import url
from wheezy.web.handlers.file import file_handler
from wheezy.web.handlers.template import template_handler

from config import http_cache as cache
from config import static_cache_profile
from error.web.urls import error_urls
from error.web.urls import test_error_urls
from membership.web.urls import membership_urls
from public.web.urls import public_urls


locale_pattern = '{locale:(en|ru)}/'
locale_defaults = {'locale': 'en'}
static_files = httpcache(
        response_transforms(gzip_transform(compress_level=6))(
            file_handler(
                root='content/static/',
                age=timedelta(hours=1))),
        cache_profile=static_cache_profile,
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
