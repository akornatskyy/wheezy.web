""" Unit tests for ``wheezy.web.handlers.method``.
"""

import unittest

from mock import Mock, patch


class MethodHandlerTestCase(unittest.TestCase):
    """Test the ``MethodHandler``."""

    def setUp(self):
        self.mock_request = Mock()
        self.mock_request.environ = {"route_args": {}}

    def test_call_default_response(self):
        """Ensure HTTP request method is dispatched correctly
        with default HTTP response status code 405.
        """
        from wheezy.web.handlers.method import MethodHandler

        for method in ["GET", "POST", "HEAD"]:
            self.mock_request.method = method
            response = MethodHandler(self.mock_request)
            assert 405 == response.status_code

    def test_call_unknown_http_method(self):
        """Ensure HTTP request method is dispatched correctly
        in case HTTP request method is not supported.
        """
        from wheezy.web.handlers.method import MethodHandler

        self.mock_request.method = "UNKNOWN"
        response = MethodHandler(self.mock_request)
        assert 405 == response.status_code

    def test_call(self):
        """Ensure HTTP request method is dispatched correctly."""
        from wheezy.web.handlers.method import MethodHandler

        for method in ["GET", "POST", "HEAD"]:
            patcher = patch(
                "wheezy.web.handlers.method.MethodHandler." + method.lower()
            )
            self.mock_request.method = method
            mock_method = patcher.start()
            mock_method.return_value = "response"
            response = MethodHandler(self.mock_request)
            assert "response" == response
            patcher.stop()

    def test_extend_response_with_cookies(self):
        """Ensure response cookies are extended with handler cookies."""
        from wheezy.web.handlers.method import MethodHandler

        self.mock_request.method = "GET"

        mock_response = Mock()
        cookies = ["1", "2"]

        class MockMethodHandler(MethodHandler):
            def get(self):
                self.cookies = cookies
                return mock_response

        response = MockMethodHandler(self.mock_request)

        assert mock_response == response
        mock_response.cookies.extend.assert_called_once_with(cookies)
