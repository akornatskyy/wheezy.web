"""
"""

from wheezy.web.app import WSGIApplication

from config import error_mapping
from config import options
from urls import all_urls


application = WSGIApplication(
        url_mapping=all_urls,
        error_mapping=error_mapping,
        options=options)


if __name__ == '__main__':
    from wsgiref.simple_server import make_server
    try:
        print('Visit http://localhost:8080/')
        make_server('', 8080, application).serve_forever()
    except KeyboardInterrupt:
        pass
    print('\nThanks!')
