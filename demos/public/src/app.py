"""
"""

from wheezy.core.collections import defaultattrdict
from wheezy.http.request import HTTPRequest

from config import dispatch
from config import options
from config import router
from urls import all_urls


router.add_routes(all_urls)


def main(environ, start_response):
    print(environ['PATH_INFO'])
    handler, route_args = router.match(environ['PATH_INFO'].lstrip('/'))
    environ['route_args'] = defaultattrdict(str, route_args)
    request = HTTPRequest(environ, options=options)
    response = dispatch(request, handler)
    return response(start_response)


if __name__ == '__main__':
    from wsgiref.simple_server import make_server
    try:
        print('Visit http://localhost:8080/')
        make_server('', 8080, main).serve_forever()
    except KeyboardInterrupt:
        pass
    print('\nThanks!')
