""" ``urls`` module.
"""

from views import AddHandler, ListHandler

from wheezy.routing import url
from wheezy.web.handlers import file_handler

all_urls = [
    url("", ListHandler, name="list"),
    url("add", AddHandler, name="add"),
    url("static/{path:any}", file_handler(root="static/"), name="static"),
]
