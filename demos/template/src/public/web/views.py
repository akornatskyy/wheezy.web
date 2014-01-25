"""
"""

from wheezy.http import response_cache
from wheezy.http.transforms import gzip_transform
from wheezy.http.transforms import response_transforms
from wheezy.web.handlers import file_handler
from wheezy.web.handlers import template_handler

from public.web.profile import public_cache_profile
from public.web.profile import static_cache_profile


wraps_handler = lambda p: lambda h: response_cache(p)(
    response_transforms(gzip_transform(compress_level=9))(h))

extra = {
    'translation_name': 'public'
}

w = wraps_handler(public_cache_profile)
home = w(template_handler('public/home.html', **extra))
about = w(template_handler('public/about.html', **extra))

# cached by nginx
http400 = template_handler('public/http400.html', status_code=400, **extra)
http403 = template_handler('public/http403.html', status_code=403, **extra)
http404 = template_handler('public/http404.html', status_code=404, **extra)
http500 = template_handler('public/http500.html', status_code=500, **extra)

w = wraps_handler(static_cache_profile)
static_file = w(file_handler(root='content/static/'))
