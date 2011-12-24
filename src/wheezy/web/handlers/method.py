"""
"""

from wheezy.http.response import not_found
from wheezy.http.response import method_not_allowed
from wheezy.http.response import HttpResponse


class MethodHandler(object):

    def __new__(klass, *args, **kwargs):
        handler = super(MethodHandler, klass).__new__(klass)
        handler.__init__(*args, **kwargs)
        return handler()

    def __init__(self, request):
        self.options = request.config.options
        self.request = request
        self.cookies = []

    def __call__(self):
        method = self.request.METHOD
        if method == 'GET':
            response = self.get()
        elif method == 'POST':
            response = self.post()
        elif method == 'HEAD':
            response = self.head()
        else:
            response = method_not_allowed(self.request.config)
        assert isinstance(response, HttpResponse)
        if self.cookies:
            response.cookies.extend(self.cookies)
        return response

    def head(self):
        return method_not_allowed(self.request.config)

    def get(self):
        return method_not_allowed(self.request.config)

    def post(self):
        return method_not_allowed(self.request.config)
