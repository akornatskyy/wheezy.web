"""
"""

from config import options
from urls import all_urls
from wheezy.http import WSGIApplication
from wheezy.http.middleware import http_cache_middleware_factory

from wheezy.web.middleware import (
    bootstrap_defaults,
    http_error_middleware_factory,
    path_routing_middleware_factory,
)

main = WSGIApplication(
    middleware=[
        bootstrap_defaults(url_mapping=all_urls),
        http_cache_middleware_factory,
        http_error_middleware_factory,
        path_routing_middleware_factory,
    ],
    options=options,
)


if __name__ == "__main__":
    from wsgiref.handlers import BaseHandler
    from wsgiref.simple_server import make_server

    try:
        print("Visit http://localhost:8080/")
        BaseHandler.http_version = "1.1"
        make_server("", 8080, main).serve_forever()
    except KeyboardInterrupt:
        pass
    print("\nThanks!")
