"""
"""

from traceback import print_exc
from mako import exceptions
from mako.lookup import TemplateLookup

from wheezy.core.collections import defaultdict
from wheezy.caching.memory import MemoryCache
from wheezy.core.i18n import TranslationsManager
from wheezy.http.response import internal_error
from wheezy.http.response import not_found
from wheezy.http.response import redirect
from wheezy.security.crypto.ticket import Ticket
from wheezy.routing import Router
from wheezy.web.handlers.base import RedirectRouteHandler

from membership.repository.mock import MockFactory

router = Router()

cache = MemoryCache()

translations_manager = TranslationsManager()
translations_manager.load('i18n')

template_lookup = TemplateLookup(directories=[
    'content/templates'
], module_directory='/tmp/mako_modules')


def mako_render(template_name, **kwargs):
    try:
        template = template_lookup.get_template(template_name)
        body = template.render(
                **kwargs
        )
    except:
        body = exceptions.html_error_template().render()
    return body

error_map = defaultdict(lambda: 'http500', {
        400: 'http400',
        403: 'http403',
        404: 'http404',
        500: 'http500',
})


def dispatch(request, handler):
    if handler:
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
        error_route_name = error_map[status_code]
        route_name = request.environ['route_args']['route_name']
        if error_route_name != route_name:
            response = RedirectRouteHandler(request, error_route_name)
    return response


options = {
        'cache': cache,
        'translations_manager': translations_manager,
        'router': router,
        'render_template': mako_render,
        'membership': MockFactory,

        'ticket': Ticket(
            max_age=1200,
            salt='JNbCog95cDTo1NRb7inP',
            options={
                'CRYPTO_ENCRYPTION_KEY': '4oqiKhW3qzP2EiattMt7',
                'CRYPTO_VALIDATION_KEY': 'A7GfjxIBCBA3vNqvafWf'
            }),

        'AUTH_COOKIE': '_a',
        'AUTH_COOKIE_DOMAIN': None,
        'AUTH_COOKIE_PATH': '',
        'AUTH_COOKIE_SECURE': False,

        'XSRF_NAME': '_x',
        'RESUBMISSION_NAME': '_c'
}
