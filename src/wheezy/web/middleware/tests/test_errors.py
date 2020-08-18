""" Unit tests for ``wheezy.web.middleware.errors``.
"""

import unittest

from mock import Mock


class HTTPErrorMiddlewareTestCase(unittest.TestCase):
    """Test the ``HTTPErrorMiddleware``."""

    def test_following_response_is_none(self):
        """The following middleware returns None as response."""
        from wheezy.web.middleware.errors import HTTPErrorMiddleware

        mock_request = Mock()
        mock_request.environ = {"route_args": {"route_name": "http404"}}
        mock_following = Mock(return_value=None)
        middleware = HTTPErrorMiddleware({404: "http404"}, None)
        response = middleware(mock_request, mock_following)
        assert 404 == response.status_code

    def test_response_status_code_is_below_400(self):
        """The following middleware returns response
        with HTTP status code less than 400.
        """
        from wheezy.web.middleware.errors import HTTPErrorMiddleware

        mock_request = Mock()
        mock_response = Mock()
        mock_response.status_code = 200
        mock_following = Mock(return_value=mock_response)
        middleware = HTTPErrorMiddleware({}, None)
        response = middleware(mock_request, mock_following)
        assert 200 == response.status_code

    def test_following_raises_error(self):
        """The following middleware raises unhandled error."""
        from wheezy.web.middleware.errors import HTTPErrorMiddleware

        mock_request = Mock()
        mock_request.environ = {"route_args": {"route_name": "http500"}}
        mock_logger = Mock()
        mock_following = Mock(side_effect=ValueError)
        middleware = HTTPErrorMiddleware({500: "http500"}, mock_logger)
        response = middleware(mock_request, mock_following)

        assert 500 == response.status_code
        assert mock_logger.error.called

    def test_following_raises_error_extra_info(self):
        """Ensure extra provider is called."""
        from wheezy.web.middleware.errors import HTTPErrorMiddleware

        mock_request = Mock()
        mock_request.environ = {"route_args": {"route_name": "http500"}}
        mock_logger = Mock()
        mock_extra_provider = Mock()
        mock_following = Mock(side_effect=ValueError)
        middleware = HTTPErrorMiddleware(
            {500: "http500"}, mock_logger, mock_extra_provider
        )
        response = middleware(mock_request, mock_following)

        assert 500 == response.status_code
        mock_extra_provider.assert_called_once_with(mock_request)
        assert mock_logger.error.called

    def test_following_error_pass_through(self):
        """The following middleware raises error that pass
        through error middleware.
        """
        from wheezy.web.middleware.errors import HTTPErrorMiddleware

        mock_request = Mock()
        mock_request.environ = {"route_args": {"route_name": "http500"}}
        for error in [KeyboardInterrupt, SystemExit, MemoryError]:
            mock_following = Mock(side_effect=error)
            middleware = HTTPErrorMiddleware({}, None)
            self.assertRaises(
                error, lambda: middleware(mock_request, mock_following)
            )

    def test_following_response_needs_redirect(self):
        """The following middleware returns error status
        that needs redirection to error page.
        """
        from wheezy.web.middleware.errors import HTTPErrorMiddleware

        mock_request = Mock()
        mock_path_for = Mock(return_value="not_found")
        mock_request.options = {"path_for": mock_path_for}
        mock_request.root_path = "my_site/"
        mock_request.method = "GET"
        mock_request.ajax = False
        mock_request.environ = {"route_args": {"route_name": "welcome"}}
        mock_following = Mock(return_value=None)
        middleware = HTTPErrorMiddleware({404: "http404"}, None)
        response = middleware(mock_request, mock_following)
        assert 302 == response.status_code


class HTTPErrorMiddlewareFactoryTestCase(unittest.TestCase):
    """Test the ``http_error_middleware_factory``."""

    def test_http_errors_undefined(self):
        """http_errors options is undefined."""
        from wheezy.web.middleware.errors import http_error_middleware_factory

        middleware = http_error_middleware_factory({})
        assert middleware

    def test_http_errors(self):
        """http_errors."""
        from wheezy.core.collections import defaultdict
        from wheezy.web.middleware.errors import http_error_middleware_factory

        mock_path_for = Mock()
        middleware = http_error_middleware_factory(
            {
                "path_for": mock_path_for,
                "http_errors": defaultdict(
                    lambda: "http500", {404: "http400"}
                ),
            }
        )
        assert middleware

    def test_logger_defined(self):
        """logger is available in options."""
        from wheezy.web.middleware.errors import http_error_middleware_factory

        middleware = http_error_middleware_factory(
            {"http_errors_logger": Mock()}
        )
        assert middleware
