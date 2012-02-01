"""
"""

from wheezy.http import method_not_allowed
from wheezy.http import HTTPResponse


class MethodHandler(object):
    """ Represents the most generic handler. It serves dispatcher purpose
        for HTTP request method (GET, POST, etc). Base class for all
        handlers.
    """

    def __new__(klass, *args, **kwargs):
        handler = super(MethodHandler, klass).__new__(klass)
        handler.__init__(*args, **kwargs)
        return handler()

    def __init__(self, request):
        self.options = request.config.options
        self.request = request
        self.route_args = request.environ['route_args']
        self.cookies = []

    def __call__(self):
        method = self.request.method
        if method == 'GET':
            response = self.get()
        elif method == 'POST':
            response = self.post()
        elif method == 'HEAD':
            response = self.head()
        else:
            response = method_not_allowed(self.request.config)
        if self.cookies:
            response.cookies.extend(self.cookies)
        return response

    def head(self):
        """ Responds to HTTP HEAD requests.
        """
        return method_not_allowed(self.request.config)

    def get(self):
        """ Responds to HTTP GET requests.
        """
        return method_not_allowed(self.request.config)

    def post(self):
        """ Responds to HTTP POST requests.
        """
        return method_not_allowed(self.request.config)
