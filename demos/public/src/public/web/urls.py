"""
"""

from wheezy.routing import url
from wheezy.web.handlers.template import template_handler


public_urls = [
    url('home', template_handler('public/home.html'), name='home'),
    url('about', template_handler('public/about.html'), name='about')
]
