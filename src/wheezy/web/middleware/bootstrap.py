
""" ``bootstrap`` module.
"""

from warnings import warn

from wheezy.http import bootstrap_http_defaults


def bootstrap_defaults(url_mapping=None):
    """ Defaults bootstrap.
    """
    def load(options):
        bootstrap_http_defaults(options)
        if 'path_router' not in options:
            from wheezy.routing import PathRouter
            options['path_router'] = path_router = PathRouter()
        else:
            path_router = options['path_router']
        if 'path_for' not in options:
            options['path_for'] = path_router.path_for
        if url_mapping:
            path_router.add_routes(url_mapping)
        if 'render_template' not in options:
            warn('Bootstrap: render_template is not defined', stacklevel=2)
        if 'translations_manager' not in options:
            from wheezy.core.i18n import TranslationsManager
            options['translations_manager'] = TranslationsManager()
        if 'ticket' not in options:
            from wheezy.security.crypto import Ticket
            options['ticket'] = Ticket()

        options.setdefault('ENCODING', 'UTF-8')
        options.setdefault(
            'CONTENT_TYPE', 'text/html; charset=' + options['ENCODING'])
        options.setdefault('AUTH_COOKIE', '_a')
        options.setdefault('AUTH_COOKIE_DOMAIN', None)
        options.setdefault('AUTH_COOKIE_PATH', '')
        options.setdefault('AUTH_COOKIE_SECURE', False)

        options.setdefault('XSRF_NAME', '_x')
        options.setdefault('RESUBMISSION_NAME', '_c')
        return None
    return load
