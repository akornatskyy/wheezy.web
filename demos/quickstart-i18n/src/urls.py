"""
"""

from wheezy.routing import url

from public.web.urls import error_urls
from public.web.urls import public_urls
from public.web.urls import static_urls
from public.web.views import WelcomeHandler


all_urls = [
    url('', WelcomeHandler, name='default')
]
all_urls += public_urls
all_urls += [('error/', error_urls)]
all_urls += static_urls
