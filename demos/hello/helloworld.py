"""
"""

from datetime import datetime
from datetime import timedelta

from wheezy.caching import MemoryCache
from wheezy.http import CacheProfile
from wheezy.http import HTTPResponse
from wheezy.http import WSGIApplication
from wheezy.http import httpcache
from wheezy.http import response_cache
from wheezy.routing import url
from wheezy.web.caching import handler_cache
from wheezy.web.handlers import BaseHandler
from wheezy.web.middleware import bootstrap_defaults
from wheezy.web.middleware import path_routing_middleware_factory


cache = MemoryCache()
public_cache_profile = CacheProfile(
        'public', duration=timedelta(minutes=15), enabled=True)
no_cache_profile = CacheProfile(
        'none', no_store=True, enabled=True)


class WelcomeHandler(BaseHandler):

    def get(self):
        response = HTTPResponse(options=self.request.config)
        response.write('Hello World! It is %s.'
                % datetime.now().time().strftime('%H:%M:%S'))
        return response


class Welcome2Handler(BaseHandler):

    @handler_cache(profile=public_cache_profile, cache=cache)
    def get(self):
        response = HTTPResponse(options=self.request.config)
        response.write('Hello World! It is %s.'
                % datetime.now().time().strftime('%H:%M:%S'))
        return response


def now(request):
    response = HTTPResponse(options=request.config)
    response.write('It is %s.'
                % datetime.now().time().strftime('%H:%M:%S'))
    return response


@response_cache(profile=public_cache_profile, cache=cache)
def now2(request):
    response = HTTPResponse(options=request.config)
    response.write('It is %s.'
                % datetime.now().time().strftime('%H:%M:%S'))
    return response


all_urls = [
        url('', httpcache(WelcomeHandler, public_cache_profile, cache)),
        url('welcome2', Welcome2Handler),
        url('now', httpcache(now, public_cache_profile, cache)),
        url('now2', now2)
]

main = WSGIApplication(
        middleware=[
            bootstrap_defaults(url_mapping=all_urls),
            path_routing_middleware_factory
        ]
)


if __name__ == '__main__':
    from wsgiref.simple_server import make_server
    try:
        print('Visit http://localhost:8080/')
        make_server('', 8080, main).serve_forever()
    except KeyboardInterrupt:
        pass
    print('\nThanks!')
