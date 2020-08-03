from hello.web.urls import all_urls

from wheezy.routing import url
from wheezy.web.handlers.file import file_handler

all_urls.append(
    url("static/{path:any}", file_handler("src/hello/static"), name="static")
)
