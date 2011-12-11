"""
"""

from wheezy.core.config import Config
from wheezy.core.descriptors import attribute
from wheezy.html.factory import widget
from wheezy.http.response import HttpResponse
from wheezy.web.handlers.method import MethodHandler
from wheezy.validation.model import try_update_model


class BaseHandler(MethodHandler):

    def __init__(self, request):
        self.request = request
        locale = self.locale
        config = request.config
        options = dict(config.options)
        options['errors'] = self.errors = {}
        options['locale'] = locale
        options['translations'] = config.translations[locale]
        self.config = Config(options=options)
        super(BaseHandler, self).__init__(request)

    @attribute
    def locale(self):
        return 'en'

    def route_locale(self):
        route_kwargs = self.request.ROUTE
        if route_kwargs:
            return route_kwargs.get('locale', None)
        return None

    def browser_locale(self):
        raise NotImplemented()

    def render_template(self, template_name, **kwargs):
        errors = self.errors
        kwargs = dict((name, widget(value, errors))
                for name, value in kwargs.iteritems())
        kwargs['path_for'] = self.path_for
        return self.config.render_template(template_name, **kwargs)

    def render_response(self, template_name, **kwargs):
        response = HttpResponse(options=self.request.config)
        response.write(self.render_template(
            template_name,
            **kwargs))
        return response

    def try_update_model(self, model, values=None):
        return try_update_model(
                model, values or self.request.FORM, self.errors,
                self.config.translations.validation
        )

    def path_for(self, name, **kwargs):
        script_name = self.request.SCRIPT_NAME + '/'
        route_kwargs = self.request.ROUTE
        if route_kwargs:
            route_kwargs = dict(route_kwargs)
            route_kwargs.update(kwargs)
            kwargs = route_kwargs
        return script_name + self.config.router.path_for(name, **kwargs)
