"""
"""
from uuid import uuid4

from wheezy.core.descriptors import attribute
from wheezy.core.i18n import null_translations
from wheezy.core.i18n import ref_gettext
from wheezy.core.url import urlparts
from wheezy.core.uuid import UUID_EMPTY
from wheezy.core.uuid import parse_uuid
from wheezy.core.uuid import shrink_uuid
from wheezy.http import HTTPCookie
from wheezy.http import HTTPResponse
from wheezy.http import ajax_redirect
from wheezy.http import json_response
from wheezy.http import redirect
from wheezy.http import permanent_redirect
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
        return {
            'errors': self.errors,
            'locale': self.locale,
            'principal': self.principal
        }

    # region: routing

    def path_for(self, name, **kwargs):
        if kwargs:
            return self.request.root_path + self.options['path_for'](
                name, **dict(self.route_args, **kwargs))
        else:
            return self.request.root_path + self.options['path_for'](
                name, **self.route_args)

    def absolute_url_for(self, name, **kwargs):
        parts = self.request.urlparts
        parts = parts.join(urlparts(path=self.path_for(name, **kwargs)))
        return parts.geturl()

    def redirect_for(self, name, **kwargs):
        if self.request.ajax:
            return ajax_redirect(self.absolute_url_for(name, **kwargs))
        return redirect(self.absolute_url_for(name, **kwargs))

    def see_other_for(self, name, **kwargs):
        if self.request.ajax:
            return ajax_redirect(self.absolute_url_for(name, **kwargs))
        return see_other(self.absolute_url_for(name, **kwargs))

    # region: i18n

    @attribute
    def locale(self):
        return self.route_args.get('locale', '')

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

    # region: templates

    @attribute
    def helpers(self):
        return {
            '_': self._,
            'absolute_url_for': self.absolute_url_for,
            'errors': self.errors,
            'locale': self.locale,
            'path_for': self.path_for,
            'principal': self.principal,
            'resubmission': self.resubmission_widget,
            'route_args': self.route_args,
            'xsrf': self.xsrf_widget
        }

    def render_template(self, template_name, **kwargs):
        return self.options['render_template'](
            template_name, dict(self.helpers, **kwargs))

    def render_response(self, template_name, **kwargs):
        options = self.options
        response = HTTPResponse(options['CONTENT_TYPE'], options['ENCODING'])
        response.write(options['render_template'](
            template_name, dict(self.helpers, **kwargs)))
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
            ticket, time_left = auth_ticket.decode(auth_cookie)
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
        cookies = self.request.cookies
        if xsrf_name in cookies:
            xsrf_token = cookies[xsrf_name]
        else:
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
        xsrf_name = self.options['XSRF_NAME']
        form = self.request.form
        if xsrf_name in form:
            xsrf_token = form[xsrf_name][-1]
            return xsrf_token == self.xsrf_token \
                and parse_uuid(xsrf_token) != UUID_EMPTY
        else:
            self.delxsrf_token()
            return False

    def xsrf_widget(self):
        return '<input type="hidden" name="' + self.options['XSRF_NAME'] + \
            '" value="' + self.xsrf_token + '" />'

    # region: resubmission

    def getresubmission(self):
        if hasattr(self, '_BaseHandler__resubmission'):
            return self.__resubmission
        resubmission_name = self.options['RESUBMISSION_NAME']
        cookies = self.request.cookies
        if resubmission_name in cookies:
            counter = cookies[resubmission_name]
            self.__resubmission = counter
        else:
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
        if self.request.ajax:
            return True
        name = self.options['RESUBMISSION_NAME']
        form = self.request.form
        if name in form:
            counter = form[name][-1]
            if counter == self.resubmission:
                try:
                    counter = str(int(counter) + 1)
                    self.setresubmission(counter)
                    return True
                except ValueError:
                    self.setresubmission('0')
        return False

    def resubmission_widget(self):
        if self.request.ajax:
            return ''
        return '<input type="hidden" name="' + \
            self.options['RESUBMISSION_NAME'] + \
            '" value="' + self.resubmission + '" />'


def redirect_handler(route_name, **route_args):
    """ Redirects to given route name (HTTP status code 302).
    """
    return lambda request: RedirectRouteHandler(
        request, route_name, **route_args)


class RedirectRouteHandler(BaseHandler):
    """ Redirects to given route name (HTTP status code 302).
    """

    def __init__(self, request, route_name, **route_args):
        self.route_name = route_name
        self.route_args = route_args
        super(RedirectRouteHandler, self).__init__(request)

    def get(self):
        return self.redirect_for(self.route_name, **self.route_args)

    def post(self):
        return self.redirect_for(self.route_name, **self.route_args)


def permanent_redirect_handler(route_name, **route_args):
    """ Performs permanent redirect (HTTP status code 301) to given route
        name.
    """
    return lambda request: PermanentRedirectRouteHandler(
        request, route_name, **route_args)


class PermanentRedirectRouteHandler(BaseHandler):
    """ Performs permanent redirect (HTTP status code 301) to given route
        name.
    """

    def __init__(self, request, route_name, **route_args):
        self.route_name = route_name
        self.route_args = route_args
        super(PermanentRedirectRouteHandler, self).__init__(request)

    def get(self):
        return permanent_redirect(
            self.absolute_url_for(self.route_name, **self.route_args))

    def post(self):
        return permanent_redirect(
            self.absolute_url_for(self.route_name, **self.route_args))
