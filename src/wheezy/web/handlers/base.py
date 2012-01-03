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
from wheezy.http.cookie import HTTPCookie
from wheezy.http.response import HTTPResponse
from wheezy.http.response import redirect
from wheezy.security.principal import Principal
from wheezy.validation.mixin import ValidationMixin
from wheezy.validation.model import try_update_model
from wheezy.web.comp import iteritems
from wheezy.web.handlers.method import MethodHandler


class BaseHandler(MethodHandler, ValidationMixin):

    @attribute
    def context(self):
        c = dict(self.options)
        c['errors'] = self.errors
        c['locale'] = self.locale
        c['principal'] = self.principal
        c['translations'] = self.translations
        return c

    # region: routing

    def path_for(self, name, **kwargs):
        route_args = dict(self.route_args)
        route_args.update(kwargs)
        return self.request.root_path + self.options['path_router'].path_for(
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
        return self.route_args['locale']

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
                model, values or self.request.form, self.errors,
                self.translations['validation'])

    # region: templates

    @attribute
    def helpers(self):
        return {
            '_': ref_gettext(self.translation),
            'absolute_url_for': self.absolute_url_for,
            'path_for': self.path_for,
            'principal': self.principal,
            'resubmission': self.resubmission_widget,
            'route_args': self.route_args,
            'xsrf': self.xsrf_widget
        }

    def render_template(self, template_name, **kwargs):
        if kwargs:
            errors = self.errors
            kwargs = dict((name, widget(value, errors))
                    for name, value in iteritems(kwargs))
        kwargs.update(self.helpers)
        return self.options['render_template'](template_name, **kwargs)

    def render_response(self, template_name, **kwargs):
        response = HTTPResponse(options=self.options)
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
                self.request.cookies[options['AUTH_COOKIE']]
            )
            if ticket:
                principal = Principal.load(ticket)
                if time_left < auth_ticket.max_age / 2:
                    # renew
                    self.setprincipal(principal)
                    return principal
            else:
                self.delprincipal()
        except KeyError:  # No auth cookie
            pass
        self.__principal = principal
        return principal

    def setprincipal(self, principal):
        options = self.options
        auth_ticket = self.ticket
        self.cookies.append(HTTPCookie(
            options['AUTH_COOKIE'],
            value=auth_ticket.encode(principal.dump()),
            path=self.request.root_path + options['AUTH_COOKIE_PATH'],
            domain=options['AUTH_COOKIE_DOMAIN'],
            secure=options['AUTH_COOKIE_SECURE'],
            httponly=True,
            options=options))
        self.__principal = principal

    def delprincipal(self):
        options = self.options
        self.cookies.append(HTTPCookie.delete(
            options['AUTH_COOKIE'],
            path=self.request.root_path + options['AUTH_COOKIE_PATH'],
            domain=options['AUTH_COOKIE_DOMAIN'],
            options=options))
        self.__principal = None

    principal = property(getprincipal, setprincipal, delprincipal)

    # region: xsrf

    def getxsrf_token(self):
        if hasattr(self, '_BaseHandler__xsrf_token'):
            return self.__xsrf_token
        options = self.options
        xsrf_name = options['XSRF_NAME']
        try:
            xsrf_token = self.request.cookies[xsrf_name]
        except KeyError:
            xsrf_token = shrink_uuid(uuid4())
            self.cookies.append(HTTPCookie(
                xsrf_name,
                value=xsrf_token,
                path=self.request.root_path,
                httponly=True,
                options=options))
        self.__xsrf_token = xsrf_token
        return xsrf_token

    def delxsrf_token(self):
        options = self.options
        self.__xsrf_token = None
        self.cookies.append(HTTPCookie.delete(
            options['XSRF_NAME'],
            path=self.request.root_path,
            options=options))

    xsrf_token = property(getxsrf_token, None, delxsrf_token)

    def validate_xsrf_token(self):
        options = self.options
        xsrf_name = options['XSRF_NAME']
        xsrf_token = last_item_adapter(self.request.form)[xsrf_name]
        if xsrf_token and xsrf_token == self.xsrf_token and parse_uuid(
                xsrf_token) != UUID_EMPTY:
            return True
        else:
            self.delxsrf_token()
            return False

    def xsrf_widget(self):
        return '<input type="hidden" name="' + self.options['XSRF_NAME'] \
                + '" value="' + self.xsrf_token + '" />'

    # region: resubmission

    def getresubmission(self):
        if hasattr(self, '_BaseHandler__resubmission'):
            return self.__resubmission
        try:
            counter = self.request.cookies[self.options['RESUBMISSION_NAME']]
            self.__resubmission = counter
        except (KeyError, TypeError):
            counter = '0'
            self.setresubmission(counter)
        return counter

    def setresubmission(self, value):
        options = self.options
        self.cookies.append(HTTPCookie(
            options['RESUBMISSION_NAME'],
            value=value,
            path=self.request.root_path,
            httponly=True,
            options=options))
        self.__resubmission = value

    def delresubmission(self):
        options = self.options
        self.__resubmission = None
        name = options['RESUBMISSION_NAME']
        self.cookies = list(filter(lambda c: c.name != name, self.cookies))
        self.cookies.append(HTTPCookie.delete(
            name,
            path=self.request.root_path,
            options=options))

    resubmission = property(getresubmission, setresubmission, delresubmission)

    def validate_resubmission(self):
        name = self.options['RESUBMISSION_NAME']
        counter = last_item_adapter(self.request.form)[name]
        if counter and counter == self.resubmission:
            counter = str(int(counter) + 1)
            self.setresubmission(counter)
            return True
        else:
            return False

    def resubmission_widget(self):
        return '<input type="hidden" name="' + \
                self.options['RESUBMISSION_NAME'] \
                + '" value="' + self.resubmission + '" />'


def redirect_handler(route_name, **route_args):
    return lambda request: RedirectRouteHandler(request,
            route_name,
            **route_args)


class RedirectRouteHandler(BaseHandler):

    def __init__(self, request, route_name, **route_args):
        self.route_name = route_name
        self.route_args = route_args
        super(RedirectRouteHandler, self).__init__(request)

    def get(self):
        return self.redirect_for(self.route_name, **self.route_args)

    def post(self):
        return self.redirect_for(self.route_name, **self.route_args)
