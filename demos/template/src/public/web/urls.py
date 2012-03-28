"""
"""

from wheezy.http import response_cache
from wheezy.http.transforms import gzip_transform
from wheezy.http.transforms import response_transforms
from wheezy.routing import url

from config import public_cache_profile
from public.web.views import about
from public.web.views import home
from public.web.views import http400
from public.web.views import http403
from public.web.views import http404
from public.web.views import http500


server_cache = lambda handler: response_cache(public_cache_profile)(
        response_transforms(gzip_transform(compress_level=9))(handler))

public_urls = [
    url('home', server_cache(home), name='home'),
    url('about', server_cache(about), name='about'),
]

error_urls = [
    url('400', http400, name='http400'),
    url('403', http403, name='http403'),
    url('404', http404, name='http404'),
    url('500', http500, name='http500'),
]
