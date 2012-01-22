"""
"""

from wheezy.routing import url
from wheezy.web.handlers import template_handler

from public.web.views import about
from public.web.views import home


public_urls = [
    url('home', home, name='home'),
    url('about', about, name='about'),
]
