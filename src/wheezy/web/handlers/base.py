"""
"""

from wheezy.core.descriptors import attribute
from wheezy.core.url import urlparts
from wheezy.http.response import HttpResponse
from wheezy.http.response import redirect
from wheezy.web.handlers.method import MethodHandler


class BaseHandler(MethodHandler):

    def __init__(self, request):
        self.options = request.config.options
        super(BaseHandler, self).__init__(request)

    @attribute
    def context(self):
        c = dict(self.options)
        c['locale'] = self.locale
        c['translations'] = self.translations
        c['errors'] = self.errors
        return c

    def path_for(self, name, **kwargs):
        script_name = self.request.SCRIPT_NAME + '/'
        route_args = dict(self.request.route_args)
        route_args.update(kwargs)
        return script_name + self.options['router'].path_for(
                name, **route_args)

    def absolute_url_for(self, name, **kwargs):
        parts = self.request.urlparts
        parts = parts.join(urlparts(
            path=self.path_for(name, **kwargs)))
        return parts.geturl()

    def redirect_for(self, name, **kwargs):
        return redirect(
                self.absolute_url_for(name, **kwargs),
                permanent=False,
                options=self.options)

    @attribute
    def locale(self):
        return self.request.route_args['locale']

    @attribute
    def translations(self):
        return self.options['translations_manager'][self.locale]

    @attribute
    def errors(self):
        return {}

    @attribute
    def helpers(self):
        return {
            'route_args': self.request.route_args,
            'absolute_url_for': self.absolute_url_for,
            'path_for': self.path_for,
        }

    def try_update_model(self, model, values=None):
        return try_update_model(
                model, values or self.request.FORM, self.errors,
                self.translations['validation'])

    def render_template(self, template_name, **kwargs):
        if kwargs:
            errors = self.errors
            kwargs = dict((name, widget(value, errors))
                    for name, value in kwargs.iteritems())
        kwargs.update(self.helpers)
        return self.options['render_template'](template_name, **kwargs)

    def render_response(self, template_name, **kwargs):
        response = HttpResponse(options=self.options)
        response.write(self.render_template(
            template_name,
            **kwargs))
        return response


def redirect_handler(route_name):
    return lambda request: RedirectRouteHandler(request, route_name)


class RedirectRouteHandler(BaseHandler):

    def __init__(self, request, route_name):
        self.route_name = route_name
        super(RedirectRouteHandler, self).__init__(request)

    def get(self):
        return self.redirect_for(self.route_name)
