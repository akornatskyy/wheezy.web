import warnings

from config import options
from urls import all_urls
from wheezy.http import WSGIApplication

from wheezy.web.middleware import (
    bootstrap_defaults,
    path_routing_middleware_factory,
)

warnings.simplefilter("ignore")
main = WSGIApplication(
    middleware=[
        bootstrap_defaults(url_mapping=all_urls),
        path_routing_middleware_factory,
    ],
    options=options,
)


if __name__ == "__main__":
    from wsgiref.simple_server import make_server

    try:
        print("Visit http://localhost:8080/")
        make_server("", 8080, main).serve_forever()
    except KeyboardInterrupt:
        pass
    print("\nThanks!")
