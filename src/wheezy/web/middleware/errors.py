""" ``errors`` module.
"""

import sys
from traceback import format_exception_only

from wheezy.core.collections import defaultdict
from wheezy.http.response import internal_error, not_found
from wheezy.web.handlers.base import RedirectRouteHandler


class HTTPErrorMiddleware(object):
    """ http error middleware
    """

    def __init__(self, error_mapping, logger, extra_provider=None):
        assert error_mapping is not None
        self.error_mapping = error_mapping
        self.logger = logger
        self.extra_provider = extra_provider

    def __call__(self, request, following):
        assert following is not None
        try:
            response = following(request)
            if response is None:
                response = not_found()
        except (KeyboardInterrupt, SystemExit, MemoryError):
            raise
        except Exception:
            exc_info = sys.exc_info()
            extra = self.extra_provider and self.extra_provider(request) or {}
            self.logger.error(
                "".join(format_exception_only(*exc_info[:2])).strip("\n"),
                exc_info=exc_info,
                extra=extra,
            )
            response = internal_error()
        status_code = response.status_code
        if status_code >= 400:
            error_route_name = self.error_mapping[status_code]
            route_name = request.environ["route_args"].get("route_name")
            if error_route_name != route_name:
                response = RedirectRouteHandler(request, error_route_name)
        return response


def http_error_middleware_factory(options):
    """ HTTP error middleware factory.
    """
    import logging

    if "http_errors" in options:
        path_for = options["path_for"]
        error_mapping = options["http_errors"]
        assert isinstance(error_mapping, defaultdict)
        assert path_for(error_mapping.default_factory()) is not None
        for route_name in error_mapping.values():
            assert path_for(route_name) is not None
    else:
        error_mapping = defaultdict(str)
    if "http_errors_logger" in options:
        logger = options["http_errors_logger"]
    else:
        logger = logging.getLogger("unhandled")
        if not logger.handlers:
            logger.setLevel(logging.ERROR)
            logger.addHandler(logging.StreamHandler(sys.stderr))
    return HTTPErrorMiddleware(
        error_mapping, logger, options.get("http_errors_extra_provider", None),
    )
