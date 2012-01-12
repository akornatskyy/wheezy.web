
""" ``errors`` module.
"""

from traceback import print_exc

from wheezy.http.response import internal_error
from wheezy.http.response import not_found
from wheezy.web.handlers.base import RedirectRouteHandler


class HTTPErrorMiddleware(object):

    def __init__(self, error_mapping):
        assert error_mapping is not None
        self.error_mapping = error_mapping

    def __call__(self, request, following):
        assert following is not None
        try:
            response = following(request)
            if response is None:
                response = not_found()
        except (KeyboardInterrupt, SystemExit, MemoryError):
            raise
        except Exception:
            print_exc()
            response = internal_error()
        status_code = response.status_code
        if status_code >= 400:
            error_route_name = self.error_mapping[status_code]
            route_name = request.environ['route_args']['route_name']
            if error_route_name != route_name:
                response = RedirectRouteHandler(request, error_route_name)
        return response
