"""
"""

from wheezy.core.descriptors import attribute
from wheezy.core.url import urlparts
from wheezy.html.factory import widget
from wheezy.http.cookie import HttpCookie
from wheezy.http.response import HttpResponse
from wheezy.http.response import redirect
from wheezy.security.principal import ANONYMOUS
from wheezy.security.principal import Principal
from wheezy.validation.mixin import ValidationMixin
from wheezy.validation.model import try_update_model
from wheezy.web.handlers.method import MethodHandler


class BaseHandler(MethodHandler, ValidationMixin):

    @attribute
    def context(self):
        c = dict(self.options)
        c['locale'] = self.locale
        c['translations'] = self.translations
        c['errors'] = self.errors
        c['principal'] = self.principal
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
            'principal': self.principal
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

    def getprincipal(self):
        if hasattr(self, '__principal'):
            return self.__principal
        principal = None
        try:
            options = self.options
            auth_ticket = options['auth_ticket']
            ticket, time_left = auth_ticket.decode(
                self.request.COOKIES[options['auth_cookie']]
            )
            if ticket:
                principal = Principal.load(ticket)
                if time_left < auth_ticket.max_age / 2:
                    # renew
                    self.setprincipal(principal)
                    return principal
        except KeyError:  # No auth cookie
            pass
        self.__principal = principal
        return principal

    def setprincipal(self, principal):
        assert not hasattr(self, '__principal')
        options = self.options
        auth_ticket = options['auth_ticket']
        self.cookies.append(HttpCookie(
            options['auth_cookie'],
            value=auth_ticket.encode(principal.dump()),
            max_age=auth_ticket.max_age,
            path=self.request.SCRIPT_NAME + options['auth_cookie_path'],
            domain=options['auth_cookie_domain'],
            secure=options['auth_cookie_secure'],
            httponly=True,
            options=options))
        self.__principal = principal

    def delprincipal(self):
        options = self.options
        self.cookies.append(HttpCookie.delete(
            options['auth_cookie'],
            path=self.request.SCRIPT_NAME + options['auth_cookie_path'],
            domain=options['auth_cookie_domain'],
            options=options))
        self.__principal = None

    principal = property(getprincipal, setprincipal, delprincipal)


def redirect_handler(route_name):
    return lambda request: RedirectRouteHandler(request, route_name)


class RedirectRouteHandler(BaseHandler):

    def __init__(self, request, route_name):
        self.route_name = route_name
        super(RedirectRouteHandler, self).__init__(request)

    def get(self):
        return self.redirect_for(self.route_name)
