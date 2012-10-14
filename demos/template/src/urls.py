"""
"""

from datetime import timedelta

from wheezy.http import response_cache
from wheezy.http.transforms import gzip_transform
from wheezy.http.transforms import response_transforms
from wheezy.routing import url
from wheezy.web.handlers import file_handler

from config import static_cache_profile
from membership.web.urls import membership_urls
from public.web.urls import error_urls
from public.web.urls import public_urls
from public.web.views import home


locale_pattern = '{locale:(en|ru)}/'
locale_defaults = {'locale': 'en'}
static_files = response_cache(static_cache_profile)(
    response_transforms(gzip_transform(compress_level=6))(
        file_handler(
            root='content/static/',
            age=timedelta(hours=1))))

locale_urls = public_urls + membership_urls
locale_urls.append(('error/', error_urls))
all_urls = [
    url('', home, locale_defaults, name='default'),
    (locale_pattern, locale_urls, locale_defaults),
    url('static/{path:any}', static_files, name='static'),
    url('favicon.ico', static_files, {'path': 'img/favicon.ico'})
]
