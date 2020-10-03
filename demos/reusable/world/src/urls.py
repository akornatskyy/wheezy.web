from shared import file_handler, import_urls, resolve_searchpath
from wheezy.routing import url

from wheezy.web.handlers.base import redirect_handler

search_path = ("content/static", resolve_searchpath("hello", "static"))

all_urls = [
    url("", redirect_handler("hello:welcome")),
    url("welcome", import_urls("hello")),
    url("static/{path:any}", file_handler(search_path), name="static"),
]
