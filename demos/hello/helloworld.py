"""
"""

from wheezy.http.response import HTTPResponse
from wheezy.web.app import WSGIApplication
from wheezy.web.handlers.base import BaseHandler


class WelcomeHandler(BaseHandler):

    def get(self):
        response = HTTPResponse(options=self.request.config)
        response.write('Hello World!')
        return response


def hello(request):
    response = HTTPResponse(options=request.config)
    response.write('Hello World!')
    return response


application = WSGIApplication(
        url_mapping=[
            ('', WelcomeHandler),
            ('hello', hello)
        ]
)


if __name__ == '__main__':
    from wsgiref.simple_server import make_server
    try:
        print('Visit http://localhost:8080/')
        make_server('', 8080, application).serve_forever()
    except KeyboardInterrupt:
        pass
    print('\nThanks!')
