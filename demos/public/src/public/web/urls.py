"""
"""

from wheezy.http import response_cache
from wheezy.http.transforms import gzip_transform
from wheezy.http.transforms import response_transforms
from wheezy.routing import url

from public.web.views import WidgetsHandler
from public.web.views import about
from public.web.views import home
from public.web.views import now_handler

from config import public_cache_profile


server_cache = lambda handler: response_cache(public_cache_profile)(
        response_transforms(gzip_transform(compress_level=9))(handler))

public_urls = [
    url('home', server_cache(home), name='home'),
    url('about', server_cache(about), name='about'),
    url('now', now_handler, name='now'),
    url('widgets-with-errors', server_cache(WidgetsHandler),
        kwargs={'mode': 'errors'}, name='widgets-with-errors'),
    url('widgets', server_cache(WidgetsHandler),
        kwargs={'mode': 'no-errors'}, name='widgets'),
]
