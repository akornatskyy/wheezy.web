""" ``app`` module.
"""

from traceback import print_exc

from wheezy.core.collections import defaultattrdict
from wheezy.core.collections import defaultdict
from wheezy.core.i18n import TranslationsManager
from wheezy.http.request import HTTPRequest
from wheezy.http.response import internal_error
from wheezy.http.response import not_found
from wheezy.routing import Router
from wheezy.security.crypto.ticket import Ticket
from wheezy.web.handlers.base import RedirectRouteHandler
from wheezy.web.templates import MakoTemplate


class WSGIApplication(object):

    def __init__(self, url_mapping, error_mapping=None, options=None):
        options = options or {}
        path_router = Router()
        path_router.add_routes(url_mapping)
        if error_mapping:
            assert isinstance(error_mapping, defaultdict)
            assert path_router.path_for(error_mapping.default_factory())
            for route_name in error_mapping.values():
                assert path_router.path_for(route_name)
        self.error_mapping = error_mapping or defaultdict(str)
        self.path_router = options['path_router'] = path_router
        if 'render_template' not in options:
            options['render_template'] = MakoTemplate()
        if 'translations_manager' not in options:
            options['translations_manager'] = TranslationsManager(
                    directories=['i18n']
            )
        if 'ticket' not in options:
            options['ticket'] = Ticket()
        self.options = options

    def __call__(self, environ, start_response):
        handler, route_args = self.path_router.match(
                environ['PATH_INFO'].lstrip('/'))
        environ['route_args'] = route_args = defaultattrdict(str, route_args)
        request = HTTPRequest(environ, options=self.options)
        if handler is not None:
            try:
                response = handler(request)
            except (KeyboardInterrupt, SystemExit, MemoryError):
                raise
            except Exception:
                print_exc()
                response = internal_error()
        else:
            response = not_found()
        status_code = response.status_code
        if status_code >= 400:
            error_route_name = self.error_mapping[status_code]
            route_name = route_args['route_name']
            if error_route_name != route_name:
                response = RedirectRouteHandler(request, error_route_name)
        return response(start_response)
