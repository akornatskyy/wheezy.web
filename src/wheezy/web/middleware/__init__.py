
""" ``middleware`` package.
"""

from wheezy.core.collections import defaultdict
from wheezy.core.i18n import TranslationsManager
from wheezy.http.config import bootstrap_http_defaults
from wheezy.routing import PathRouter
from wheezy.security.crypto import Ticket
from wheezy.web.middleware.errors import HTTPErrorMiddleware
from wheezy.web.middleware.routing import PathRoutingMiddleware
from wheezy.web.templates import MakoTemplate


def bootstrap_defaults(url_mapping=None):
    """ Defaults bootstrap.
    """
    def load(options):
        bootstrap_http_defaults(options)
        if 'path_router' not in options:
            options['path_router'] = path_router = PathRouter()
        else:
            path_router = options['path_router']
        if 'path_for' not in options:
            options['path_for'] = path_router.path_for
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
    """ HTTP error middleware factory.
    """
    path_for = options['path_for']
    try:
        error_mapping = options['http_errors']
        assert isinstance(error_mapping, defaultdict)
        assert path_for(error_mapping.default_factory())
        for route_name in error_mapping.values():
            assert path_for(route_name)
    except KeyError:
        error_mapping = defaultdict(str)
    return HTTPErrorMiddleware(
            error_mapping=error_mapping)


def path_routing_middleware_factory(options):
    """ PathRouting middleware factory.
    """
    path_router = options['path_router']
    return PathRoutingMiddleware(
            path_router=path_router)
