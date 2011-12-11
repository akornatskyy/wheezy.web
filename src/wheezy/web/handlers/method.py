"""
"""

from wheezy.http.response import not_found
from wheezy.http.response import method_not_allowed
from wheezy.http.response import HttpResponse


class MethodHandler(object):

    def __init__(self, request):
        self.request = request
        if request.METHOD == 'GET':
            self.response = self.get()
        elif request.METHOD == 'POST':
            self.response = self.post()
        elif request.METHOD == 'HEAD':
            self.response = self.head()
        else:
            self.response = method_not_allowed(request.options)
        assert isinstance(self.response, HttpResponse)

    def __call__(self, start_response):
        return self.response(start_response)

    def head(self):
        return method_not_allowed(self.request.options)

    def get(self):
        return method_not_allowed(self.request.options)

    def post(self):
        return method_not_allowed(self.request.options)
