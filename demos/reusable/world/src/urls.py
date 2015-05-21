from wheezy.routing import url
from wheezy.web.handlers.base import redirect_handler

from shared import file_handler
from shared import import_urls
from shared import resolve_searchpath


search_path = (
    'content/static',
    resolve_searchpath('hello', 'static')
)

all_urls = [
    url('', redirect_handler('hello:welcome')),
    url('welcome', import_urls('hello')),
    url('static/{path:any}', file_handler(search_path), name='static')
]
