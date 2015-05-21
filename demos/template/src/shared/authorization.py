from wheezy.core.comp import PY3

if PY3:  # pragma: nocover
    from urllib.parse import quote
else:  # pragma: nocover
    from urllib import quote


from wheezy.core.url import urlparts
from wheezy.http import HTTPCookie
from wheezy.http import ajax_redirect
from wheezy.http import redirect
from wheezy.web.handlers.base import BaseHandler


def setup_authorization_return_path():
    from wheezy.web.middleware import errors
    errors.RedirectRouteHandler = RedirectQueryStringReturnPathHandler


# region: cookie return path

class RedirectCookieReturnPathHandler(BaseHandler):

    def __init__(self, request, route_name):
        self.route_name = route_name
        super(RedirectCookieReturnPathHandler, self).__init__(request)

    def get(self):
        if self.request.ajax:
            url = self.absolute_url_for(self.route_name)
            return ajax_redirect(url)
        return self.post()

    def post(self):
        return_path = self.request.path
        qs = self.request.environ['QUERY_STRING']
        if qs:
            return_path += '?' + qs
        path = self.path_for(self.route_name)
        self.cookies.append(HTTPCookie(
            'return_path', return_path,
            path=path,
            options=self.options))
        parts = self.request.urlparts
        parts = parts.join(urlparts(path=path))
        url = parts.geturl()
        if self.request.ajax:
            return ajax_redirect(url)
        return redirect(url)


class RedirectCookieReturnPathMixin(object):

    def redirect_to_return_path(self):
        return_path = self.request.cookies.get('return_path')
        if return_path:
            self.cookies.append(HTTPCookie.delete(
                'return_path', self.request.path,
                options=self.options))
            # build absolute url
            parts = self.request.urlparts
            parts = parts.join(urlparts(path=return_path))
            url = parts.geturl()
        else:
            url = self.absolute_url_for('default')
        if self.request.ajax:
            return ajax_redirect(url)
        return redirect(url)


# region: query string return path

class RedirectQueryStringReturnPathHandler(BaseHandler):

    def __init__(self, request, route_name):
        self.route_name = route_name
        super(RedirectQueryStringReturnPathHandler, self).__init__(request)

    def get(self):
        if self.request.ajax:
            url = self.absolute_url_for(self.route_name)
            return ajax_redirect(url)
        return self.post()

    def post(self):
        url = self.absolute_url_for(self.route_name)
        return_path = self.request.path
        qs = self.request.environ['QUERY_STRING']
        if qs:
            return_path += '?' + qs
        url += '?return_path=' + quote(return_path)
        if self.request.ajax:
            return ajax_redirect(url)
        return redirect(url)


class RedirectQueryStringReturnPathMixin(object):

    def redirect_to_return_path(self):
        return_path = self.request.get_param('return_path')
        if return_path:
            # build absolute url
            parts = self.request.urlparts
            parts = parts.join(urlparts(path=return_path))
            url = parts.geturl()
        else:
            url = self.absolute_url_for('default')
        if self.request.ajax:
            return ajax_redirect(url)
        return redirect(url)
