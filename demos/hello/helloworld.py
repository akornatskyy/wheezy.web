"""
"""

from datetime import datetime
from datetime import timedelta

from wheezy.caching import MemoryCache
from wheezy.http import CacheProfile
from wheezy.http import HTTPResponse
from wheezy.http import WSGIApplication
from wheezy.http import response_cache
from wheezy.http.middleware import http_cache_middleware_factory
from wheezy.routing import url
from wheezy.web.caching import handler_cache
from wheezy.web.handlers import BaseHandler
from wheezy.web.middleware import bootstrap_defaults
from wheezy.web.middleware import http_error_middleware_factory
from wheezy.web.middleware import path_routing_middleware_factory


cache = MemoryCache()

public_cache_profile = CacheProfile(
    'public', duration=timedelta(minutes=15), enabled=True)
no_cache_profile = CacheProfile(
    'none', no_store=True, enabled=True)


class WelcomeHandler(BaseHandler):

    def get(self):
        response = HTTPResponse()
        response.write('Hello World! It is %s.'
                       % datetime.now().time().strftime('%H:%M:%S'))
        return response


class Welcome2Handler(BaseHandler):

    @handler_cache(public_cache_profile)
    def get(self):
        response = HTTPResponse()
        response.write('Hello World! It is %s.'
                       % datetime.now().time().strftime('%H:%M:%S'))
        return response


def now(request):
    response = HTTPResponse()
    response.write('It is %s.'
                   % datetime.now().time().strftime('%H:%M:%S'))
    return response


@response_cache(public_cache_profile)
def now2(request):
    response = HTTPResponse()
    response.write('It is %s.'
                   % datetime.now().time().strftime('%H:%M:%S'))
    return response


all_urls = [
    url('', WelcomeHandler),
    url('welcome2', Welcome2Handler),
    url('now', now),
    url('now2', now2)
]

options = {
    'http_cache': cache
}

main = WSGIApplication(
    middleware=[
        bootstrap_defaults(url_mapping=all_urls),
        http_cache_middleware_factory,
        http_error_middleware_factory,
        path_routing_middleware_factory
    ],
    options=options
)


if __name__ == '__main__':
    from wsgiref.simple_server import make_server
    try:
        print('Visit http://localhost:8080/')
        make_server('', 8080, main).serve_forever()
    except KeyboardInterrupt:
        pass
    print('\nThanks!')
