
""" ``app`` module.
"""

from wheezy.http.request import HTTPRequest
from wheezy.http.response import not_found


def wraps_middleware(following, func):
    return lambda request: func(request, following)


class WSGIApplication(object):

    def __init__(self, middleware, options=None):
        options = options or {}
        middleware = filter(
                lambda m: m is not None,
                [m(options) for m in middleware])
        middleware = reduce(
                wraps_middleware,
                reversed(middleware), None)
        assert middleware
        self.middleware = middleware
        self.options = options

    def __call__(self, environ, start_response):
        request = HTTPRequest(environ, options=self.options)
        response = self.middleware(request)
        if response is None:
            response = not_found()
        return response(start_response)
