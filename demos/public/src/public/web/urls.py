"""
"""

from wheezy.routing import url

from public.web.views import about
from public.web.views import home
from public.web.views import NowHandler
from public.web.views import WidgetsHandler


public_urls = [
    url('home', home, name='home'),
    url('about', about, name='about'),
    url('now', NowHandler, name='now'),
    url('widgets-with-errors', WidgetsHandler,
        kwargs={'mode': 'errors'}, name='widgets-with-errors'),
    url('widgets', WidgetsHandler,
        kwargs={'mode': 'no-errors'}, name='widgets'),
]
