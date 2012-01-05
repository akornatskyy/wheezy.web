
""" ``middleware`` package.
"""

from wheezy.routing import Router
from wheezy.core.i18n import TranslationsManager
from wheezy.security.crypto.ticket import Ticket
from wheezy.web.templates import MakoTemplate
from wheezy.web.middleware.errors import HTTPErrorMiddleware
from wheezy.web.middleware.routing import PathRoutingMiddleware


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

http_error = HTTPErrorMiddleware
path_routing = PathRoutingMiddleware
