
""" ``routing`` module.
"""

from wheezy.core.collections import defaultattrdict
from wheezy.core.collections import defaultdict


class PathRoutingMiddleware(object):

    def __init__(self, path_router):
        assert path_router
        self.path_router = path_router

    def __call__(self, request, following):
        environ = request.environ
        handler, route_args = self.path_router.match(
                environ['PATH_INFO'].lstrip('/'))
        environ['route_args'] = defaultattrdict(str, route_args)
        if handler is None:
            if following is not None:
                return following(request)
            return None
        return handler(request)
