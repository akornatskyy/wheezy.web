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
from wheezy.html import widget
from wheezy.http import HTTPCookie
from wheezy.http import HTTPResponse
from wheezy.http import json_response
from wheezy.http import redirect
from wheezy.http import see_other
from wheezy.security import Principal
from wheezy.validation import ValidationMixin
from wheezy.validation import try_update_model
from wheezy.web.handlers.method import MethodHandler


class BaseHandler(MethodHandler, ValidationMixin):
    """ Provides methods that integrate such features like: routing,
        i18n, model binding, template rendering, authentication,
        xsrf/resubmission protection.

        You need inherit this class and define get() and/or post() to
        be able respond to HTTP requests.
    """

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
        return self.request.root_path + self.options['path_for'](
                name, **route_args)

    def absolute_url_for(self, name, **kwargs):
        parts = self.request.urlparts
        parts = parts.join(urlparts(
            path=self.path_for(name, **kwargs)))
        return parts.geturl()

    def redirect_for(self, name, **kwargs):
        return redirect(
                self.absolute_url_for(name, **kwargs))

    def see_other_for(self, name, **kwargs):
        return see_other(
                self.absolute_url_for(name, **kwargs))

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

    @attribute
    def gettext(self):
        return ref_gettext(self.translation)

    @attribute
    def _(self):
        return ref_gettext(self.translation)

    # region: model

    @attribute
    def errors(self):
        return {}

    def try_update_model(self, model, values=None):
        return try_update_model(
                model, values or self.request.form, self.errors,
                self.translations['validation'])

    # region: widgets

    def widgets(self, **kwargs):
        errors = self.errors
        return [(name, widget(kwargs[name], errors))
                    for name in kwargs]

    # region: templates

    @attribute
    def helpers(self):
        return {
            '_': self._,
            'absolute_url_for': self.absolute_url_for,
            'errors': self.errors,
            'path_for': self.path_for,
            'principal': self.principal,
            'resubmission': self.resubmission_widget,
            'route_args': self.route_args,
            'xsrf': self.xsrf_widget
        }

    def render_template(self, template_name, widgets=None, **kwargs):
        data = self.helpers
        if kwargs:
            data.update(kwargs)
        if widgets:
            data.update(widgets)
        return self.options['render_template'](template_name, **data)

    def render_response(self, template_name, widgets=None, **kwargs):
        options = self.options
        response = HTTPResponse(options['CONTENT_TYPE'], options['ENCODING'])
        response.write(self.render_template(
            template_name,
            widgets,
            **kwargs))
        return response

    # region: json

    def json_response(self, obj):
        return json_response(obj, self.options['ENCODING'])

    # region: authentication

    @attribute
    def ticket(self):
        return self.options['ticket']

    def getprincipal(self):
        if hasattr(self, '_BaseHandler__principal'):
            return self.__principal
        principal = None
        auth_cookie = self.request.cookies.get(
                self.options['AUTH_COOKIE'], None)
        if auth_cookie is not None:
            auth_ticket = self.ticket
            ticket, time_left = auth_ticket.decode(
                    auth_cookie
            )
            if ticket:
                principal = Principal.load(ticket)
                if time_left < auth_ticket.max_age / 2:
                    # renew
                    self.setprincipal(principal)
                    return principal
            else:
                self.delprincipal()
        self.__principal = principal
        return principal

    def setprincipal(self, principal):
        options = self.options
        self.cookies.append(HTTPCookie(
            options['AUTH_COOKIE'],
            value=self.ticket.encode(principal.dump()),
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
    """ Redirects to given route name.
    """
    return lambda request: RedirectRouteHandler(request,
            route_name,
            **route_args)


class RedirectRouteHandler(BaseHandler):
    """ Redirects to given route name.
    """

    def __init__(self, request, route_name, **route_args):
        self.route_name = route_name
        self.route_args = route_args
        super(RedirectRouteHandler, self).__init__(request)

    def get(self):
        return self.redirect_for(self.route_name, **self.route_args)

    def post(self):
        return self.redirect_for(self.route_name, **self.route_args)
