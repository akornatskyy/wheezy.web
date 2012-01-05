
""" ``errors`` module.
"""

from wheezy.core.collections import defaultdict
from wheezy.http.response import not_found
from wheezy.web.handlers.base import RedirectRouteHandler


class HTTPErrorMiddleware(object):

    def __init__(self, options):
        path_router = options['path_router']
        try:
            error_mapping = options['http_errors']
            assert isinstance(error_mapping, defaultdict)
            assert path_router.path_for(error_mapping.default_factory())
            for route_name in error_mapping.values():
                assert path_router.path_for(route_name)
        except KeyError:
            error_mapping = defaultdict(str)
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
