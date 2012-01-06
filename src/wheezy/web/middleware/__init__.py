
""" ``middleware`` package.
"""

from wheezy.core.collections import defaultdict
from wheezy.core.i18n import TranslationsManager
from wheezy.routing import Router
from wheezy.security.crypto.ticket import Ticket
from wheezy.web.middleware.errors import HTTPErrorMiddleware
from wheezy.web.middleware.routing import PathRoutingMiddleware
from wheezy.web.templates import MakoTemplate


def bootstrap_defaults(url_mapping=None):
    def load(options):
        if 'path_router' not in options:
            options['path_router'] = path_router = Router()
        else:
            path_router = options['path_router']
        if url_mapping:
            path_router.add_routes(url_mapping)
        if 'render_template' not in options:
            options['render_template'] = MakoTemplate()
        if 'translations_manager' not in options:
            options['translations_manager'] = TranslationsManager()
        if 'ticket' not in options:
            options['ticket'] = Ticket()
        return None
    return load


def http_error_middleware_factory(options):
    path_router = options['path_router']
    try:
        error_mapping = options['http_errors']
        assert isinstance(error_mapping, defaultdict)
        assert path_router.path_for(error_mapping.default_factory())
        for route_name in error_mapping.values():
            assert path_router.path_for(route_name)
    except KeyError:
        error_mapping = defaultdict(str)
    return HTTPErrorMiddleware(
            error_mapping=error_mapping)


def path_routing_middleware_factory(options):
    path_router = options['path_router']
    return PathRoutingMiddleware(
            path_router=path_router)
