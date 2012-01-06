"""
"""

from datetime import datetime
from datetime import timedelta

from wheezy.caching.memory import MemoryCache
from wheezy.http.application import WSGIApplication
from wheezy.http.cache import httpcache
from wheezy.http.cacheprofile import CacheProfile
from wheezy.http.response import HTTPResponse
from wheezy.routing import url
from wheezy.web.handlers.base import BaseHandler
from wheezy.web.middleware import bootstrap_defaults
from wheezy.web.middleware import path_routing_middleware_factory


cache = MemoryCache()
cache_profile = CacheProfile(
        'public', duration=timedelta(minutes=15), enabled=True)
no_cache_profile = CacheProfile(
        'none', no_store=True, enabled=True)


class WelcomeHandler(BaseHandler):

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


all_urls=[
        url('', httpcache(WelcomeHandler, cache_profile, cache), name='welcome'),
        url('now', httpcache(now, no_cache_profile))
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
