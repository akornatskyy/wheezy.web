"""
"""

from public.web.urls import error_urls, public_urls, static_urls
from public.web.views import WelcomeHandler
from wheezy.routing import url

locale_pattern = "{locale:(en|ru)}/"
locale_defaults = {"locale": "en"}

locale_urls = []
locale_urls += public_urls
locale_urls.append(("error/", error_urls))
locale_urls.append((".*", lambda ignore: None))
all_urls = [
    url("", WelcomeHandler, locale_defaults),
    url(
        locale_pattern.rstrip("/"),
        WelcomeHandler,
        locale_defaults,
        name="default",
    ),
    (locale_pattern, locale_urls, locale_defaults),
]
all_urls += static_urls
