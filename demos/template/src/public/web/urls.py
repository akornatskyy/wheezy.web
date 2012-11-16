"""
"""

from wheezy.routing import url

from public.web.views import about
from public.web.views import home
from public.web.views import http400
from public.web.views import http403
from public.web.views import http404
from public.web.views import http500
from public.web.views import static_file


public_urls = [
    url('home', home, name='home'),
    url('about', about, name='about'),
]

error_urls = [
    url('400', http400, name='http400'),
    url('403', http403, name='http403'),
    url('404', http404, name='http404'),
    url('500', http500, name='http500'),
]

static_urls = [
    url('static/{path:any}', static_file, name='static'),
    url('favicon.ico', static_file, {'path': 'img/favicon.ico'})
]
