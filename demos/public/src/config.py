"""
"""

from mako import exceptions
from mako.lookup import TemplateLookup

from wheezy.caching.memory import MemoryCache
from wheezy.routing import Router
from wheezy.core.i18n import TranslationsManager

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


options = {
        'cache': cache,
        'translations': translations,
        'router': router,
        'render_template': mako_render
}
