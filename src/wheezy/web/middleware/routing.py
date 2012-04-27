
""" ``routing`` module.
"""

from wheezy.core.collections import defaultattrdict


class PathRoutingMiddleware(object):
    """ path routing middleware
    """

    def __init__(self, path_router):
        assert path_router
        self.match = path_router.match

    def __call__(self, request, following):
        environ = request.environ
        handler, route_args = self.match(environ['PATH_INFO'].lstrip('/'))
        environ['route_args'] = defaultattrdict(str, route_args)
        if handler is None:
            if following is not None:
                return following(request)
            return None
        return handler(request)


def path_routing_middleware_factory(options):
    """ PathRouting middleware factory.
    """
    return PathRoutingMiddleware(options['path_router'])
