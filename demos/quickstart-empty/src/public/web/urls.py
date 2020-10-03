"""
"""

from public.web.views import (
    WelcomeHandler,
    http400,
    http403,
    http404,
    http500,
    static_file,
)
from wheezy.routing import url

public_urls = [url("home", WelcomeHandler, name="home")]

error_urls = [
    url("400", http400, name="http400"),
    url("403", http403, name="http403"),
    url("404", http404, name="http404"),
    url("500", http500, name="http500"),
]

static_urls = [
    url("static/{path:any}", static_file, name="static"),
    url("favicon.ico", static_file, {"path": "img/favicon.ico"}),
    url("robots.txt", static_file, {"path": "robots.txt"}, name="robots"),
]
