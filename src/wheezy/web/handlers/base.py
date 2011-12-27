"""
"""
from uuid import uuid4

from wheezy.core.collections import last_item_adapter
from wheezy.core.descriptors import attribute
from wheezy.core.i18n import null_translations
from wheezy.core.i18n import ref_gettext
from wheezy.core.url import urlparts
from wheezy.core.uuid import UUID_EMPTY
from wheezy.core.uuid import parse_uuid
from wheezy.core.uuid import shrink_uuid
from wheezy.html.factory import widget
from wheezy.http.cookie import HttpCookie
from wheezy.http.response import HttpResponse
from wheezy.http.response import redirect
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

    # region: routing

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

    # region: i18n

    @attribute
    def locale(self):
        return self.request.route_args['locale']

    @attribute
    def translations(self):
        return self.options['translations_manager'][self.locale]

    @attribute
    def translation(self):
        return null_translations

    # region: model

    @attribute
    def errors(self):
        return {}

    def try_update_model(self, model, values=None):
        return try_update_model(
                model, values or self.request.FORM, self.errors,
                self.translations['validation'])

    # region: templates

    @attribute
    def helpers(self):
        return {
            'route_args': self.request.route_args,
            'absolute_url_for': self.absolute_url_for,
            'path_for': self.path_for,
            'principal': self.principal,
            'xsrf': self.xsrf_widget,
            'resubmission': self.resubmission_widget,
            '_': ref_gettext(self.translation)
        }

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

    # region: authentication

    @attribute
    def ticket(self):
        return self.options['ticket']

    def getprincipal(self):
        if hasattr(self, '_BaseHandler__principal'):
            return self.__principal
        principal = None
        try:
            options = self.options
            auth_ticket = self.ticket
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
        auth_ticket = self.ticket
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

    # region: xsrf

    def getxsrf_token(self):
        if hasattr(self, '_BaseHandler__xsrf_token'):
            return self.__xsrf_token
        options = self.options
        xsrf_name = options['xsrf_name']
        try:
            xsrf_token = self.request.COOKIES[xsrf_name]
        except KeyError:
            xsrf_token = shrink_uuid(uuid4())
            self.cookies.append(HttpCookie(
                xsrf_name,
                value=xsrf_token,
                max_age=self.ticket.max_age,
                path=self.request.SCRIPT_NAME + '/',
                httponly=True,
                options=options))
        return xsrf_token

    def delxsrf_token(self):
        options = self.options
        self.__xsrf_token = None
        self.cookies.append(HttpCookie.delete(
            options['xsrf_name'],
            path=self.request.SCRIPT_NAME + '/',
            options=options))

    xsrf_token = property(getxsrf_token, None, delxsrf_token)

    def validate_xsrf_token(self):
        options = self.options
        xsrf_name = options['xsrf_name']
        xsrf_token = last_item_adapter(self.request.FORM)[xsrf_name]
        if xsrf_token and xsrf_token == self.xsrf_token and parse_uuid(
                xsrf_token) != UUID_EMPTY:
            return True
        else:
            self.delxsrf_token()
            return False

    def xsrf_widget(self):
        return '<input type="hidden" name="' + self.options['xsrf_name'] \
                + '" value="' + self.xsrf_token + '" />'

    # region: resubmission

    def getresubmission(self):
        if hasattr(self, '_BaseHandler__resubmission'):
            return self.__resubmission
        try:
            counter = self.request.COOKIES[self.options['resubmission_name']]
            self.__resubmission = counter
        except (KeyError, TypeError):
            counter = '0'
            self.setresubmission(counter)
        return counter

    def setresubmission(self, value):
        options = self.options
        self.cookies.append(HttpCookie(
            options['resubmission_name'],
            value=value,
            max_age=self.ticket.max_age,
            path=self.request.SCRIPT_NAME + '/',
            httponly=True,
            options=options))
        self.__resubmission = value

    def delresubmission(self):
        options = self.options
        self.__resubmission = None
        name = options['resubmission_name']
        self.cookies = filter(lambda c: c.name != name, self.cookies)
        self.cookies.append(HttpCookie.delete(
            name,
            path=self.request.SCRIPT_NAME + '/',
            options=options))

    resubmission = property(getresubmission, setresubmission, delresubmission)

    def validate_resubmission(self):
        name = self.options['resubmission_name']
        counter = last_item_adapter(self.request.FORM)[name]
        if counter and counter == self.resubmission:
            counter = str(int(counter) + 1)
            self.setresubmission(counter)
            return True
        else:
            return False

    def resubmission_widget(self):
        return '<input type="hidden" name="' + \
                self.options['resubmission_name'] \
                + '" value="' + self.resubmission + '" />'


def redirect_handler(route_name):
    return lambda request: RedirectRouteHandler(request, route_name)


class RedirectRouteHandler(BaseHandler):

    def __init__(self, request, route_name):
        self.route_name = route_name
        super(RedirectRouteHandler, self).__init__(request)

    def get(self):
        return self.redirect_for(self.route_name)

    def post(self):
        return self.redirect_for(self.route_name)
