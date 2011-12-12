"""
"""

from traceback import print_exc
from mako import exceptions
from mako.lookup import TemplateLookup

from wheezy.caching.memory import MemoryCache
from wheezy.core.i18n import TranslationsManager
from wheezy.http.response import internal_error
from wheezy.http.response import not_found
from wheezy.http.response import redirect
from wheezy.routing import Router

router = Router()

cache = MemoryCache()

translations = TranslationsManager()
translations.load('i18n')

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


error_map = {
        400: 'http400',
        403: 'http403',
        404: 'http404',
        500: 'http500',
}


def handle_errors(request, handler):
    if handler:
        try:
            response = handler(request)
        except (KeyboardInterrupt, SystemExit, MemoryError):
            raise
        except Exception, e:
            print_exc()
            response = internal_error()
    else:
        response = not_found()
    status_code = response.status_code
    if status_code >= 400:
        try:
            error_route = error_map[status_code]
            route_name = request.route_args.route_name
            if error_route != route_name:
                # TODO: absolute routes
                response = redirect('/' +
                        router.path_for(error_route),
                        options=request.config)
        except KeyError:
            pass
    return response


options = {
        'cache': cache,
        'translations': translations,
        'router': router,
        'render_template': mako_render
}
