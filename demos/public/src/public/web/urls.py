"""
"""

from wheezy.routing import url

from public.web.views import WidgetsHandler
from public.web.views import about
from public.web.views import home
from public.web.views import now_handler


public_urls = [
    url('home', home, name='home'),
    url('about', about, name='about'),
    url('now', now_handler, name='now'),
    url('widgets-with-errors', WidgetsHandler,
        kwargs={'mode': 'errors'}, name='widgets-with-errors'),
    url('widgets', WidgetsHandler,
        kwargs={'mode': 'no-errors'}, name='widgets'),
]
