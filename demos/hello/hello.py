
""" Minimal helloworld application.
"""

from wheezy.http import HTTPResponse
from wheezy.http import WSGIApplication
from wheezy.routing import url
from wheezy.web.handlers import BaseHandler
from wheezy.web.middleware import bootstrap_defaults
from wheezy.web.middleware import path_routing_middleware_factory


class WelcomeHandler(BaseHandler):

    def get(self):
        response = HTTPResponse(options=self.request.config)
        response.write('Hello World!')
        return response


def welcome(request):
    response = HTTPResponse(options=request.config)
    response.write('Hello World!')
    return response


all_urls = [
        url('', WelcomeHandler, name='default'),
        url('welcome', welcome, name='welcome')
]


main = WSGIApplication(
        middleware=[
            bootstrap_defaults(url_mapping=all_urls),
            path_routing_middleware_factory
        ]
)


if __name__ == '__main__':
    from wsgiref.simple_server import make_server
    try:
        print('Visit http://localhost:8080/')
        make_server('', 8080, main).serve_forever()
    except KeyboardInterrupt:
        pass
    print('\nThanks!')
