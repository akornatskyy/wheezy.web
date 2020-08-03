"""
"""

from public.web.urls import error_urls, public_urls, static_urls
from public.web.views import WelcomeHandler

from wheezy.routing import url

all_urls = [url("", WelcomeHandler, name="default")]
all_urls += public_urls
all_urls += [("error/", error_urls)]
all_urls += static_urls
