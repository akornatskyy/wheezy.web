"""
"""

from wheezy.http.application import WSGIApplication
from wheezy.web.middleware import bootstrap_defaults
from wheezy.web.middleware import http_error
from wheezy.web.middleware import path_routing

from config import options
from urls import all_urls


main = WSGIApplication(
        middleware=[
            bootstrap_defaults(url_mapping=all_urls),
            http_error,
            path_routing
        ],
        options=options)


if __name__ == '__main__':
    from wsgiref.simple_server import make_server
    try:
        print('Visit http://localhost:8080/')
        make_server('', 8080, main).serve_forever()
    except KeyboardInterrupt:
        pass
    print('\nThanks!')
