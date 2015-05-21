from wheezy.routing import url
from wheezy.web.handlers.file import file_handler

from hello.web.urls import all_urls


all_urls.append(url('static/{path:any}', file_handler('src/hello/static'),
                    name='static'))
