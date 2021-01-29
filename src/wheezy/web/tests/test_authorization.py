""" Unit tests for ``wheezy.web.authorization``.
"""

import unittest
from unittest.mock import Mock

from wheezy.web.authorization import authorize, secure


class AuthorizeTestCase(unittest.TestCase):
    """Test the ``authorize``."""

    def test_check_not_authenticated(self):
        """Check if call is not authenticated.

        @authorize
        def get(self):
            ...
        """
        mock_handler = Mock()
        mock_handler.principal = None
        mock_handler_method = Mock()
        handler = authorize()(mock_handler_method)
        response = handler(mock_handler)
        assert 401 == response.status_code

    def test_check_authenticated(self):
        """Check if call is authenticated.

        @authorize
        def get(self):
            ...
        """
        mock_handler = Mock()
        mock_handler.principal = "UserA"
        mock_handler_method = Mock(return_value="response")
        handler = authorize()(mock_handler_method)
        assert "response" == handler(mock_handler)
        mock_handler_method.assert_called_once_with(mock_handler)

    def test_check_authorized_but_not_authenticated(self):
        """Check if call is authenticated

        @authorize(roles=('admin',))
        def get(self):
            ...
        """
        mock_handler = Mock()
        mock_handler.principal = None
        mock_handler_method = Mock()
        handler = authorize(roles=("admin",))(mock_handler_method)
        response = handler(mock_handler)
        assert 401 == response.status_code

    def test_check_not_authorized(self):
        """Check if call is not authorized.

        @authorize(roles=('admin',))
        def get(self):
            ...
        """
        mock_principal = Mock()
        mock_principal.roles = ["user"]
        mock_handler = Mock()
        mock_handler.principal = mock_principal
        mock_handler_method = Mock()
        handler = authorize(roles=("admin",))(mock_handler_method)
        response = handler(mock_handler)
        assert 403 == response.status_code

    def test_check_authorized(self):
        """Check if call is authorized.

        @authorize(roles=('admin',))
        def get(self):
            ...
        """
        mock_principal = Mock()
        mock_principal.roles = ["user", "admin"]
        mock_handler = Mock()
        mock_handler.principal = mock_principal
        mock_handler_method = Mock(return_value="response")
        handler = authorize(roles=("admin",))(mock_handler_method)
        assert "response" == handler(mock_handler)

    def test_wrapped(self):
        """Check decorators"""
        mock_handler = Mock()
        mock_handler.principal = "UserA"

        @authorize
        def get(self):
            return "response"

        assert "response" == get(mock_handler)


class SecureTestCase(unittest.TestCase):
    """Test the ``secure``."""

    def test_check_not_secure(self):
        """Check if request is not secure.

        @secure
        def get(self):
            ...
        """
        mock_handler = Mock()
        mock_handler.request.secure = False
        mock_handler.request.urlparts = (
            "http",
            "localhost:8080",
            "/en/signin",
            None,
            None,
        )
        mock_handler_method = Mock()
        handler = secure()(mock_handler_method)
        response = handler(mock_handler)
        assert 301 == response.status_code
        location = dict(response.headers)["Location"]
        assert "https://localhost:8080/en/signin" == location

    def test_check_secure(self):
        """Check if request is secure."""
        mock_handler = Mock()
        mock_handler.request.secure = True
        mock_handler_method = Mock(return_value="response")
        handler = secure()(mock_handler_method)
        assert "response" == handler(mock_handler)

    def test_check_not_enabled(self):
        """Check if request is secure."""
        mock_handler = Mock()
        mock_handler_method = Mock(return_value="response")
        handler = secure(enabled=False)(mock_handler_method)
        assert "response" == handler(mock_handler)

    def test_wrapped(self):
        """Check decorators"""
        mock_handler = Mock()
        mock_handler.request.secure = True

        @secure
        def get(self):
            return "response"

        assert "response" == get(mock_handler)
