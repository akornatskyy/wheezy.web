"""
"""

from membership.web.urls import membership_urls
from public.web.urls import error_urls, public_urls, static_urls
from public.web.views import home

from wheezy.routing import url

locale_pattern = "{locale:(en|ru)}/"
locale_defaults = {"locale": "en"}

locale_urls = public_urls + membership_urls
locale_urls.append(("error/", error_urls))
all_urls = [
    url("", home, locale_defaults, name="default"),
    (locale_pattern, locale_urls, locale_defaults),
]
all_urls += static_urls
