
""" Unit tests for ``wheezy.web.authorization``.
"""

import unittest

from mock import Mock


class AuthorizeTestCase(unittest.TestCase):
    """ Test the ``authorize``.
    """

    def test_check_not_authenticated(self):
        """ Check if call is not authenticated.

            @authorize
            def get(self):
                ...
        """
        from wheezy.web.authorization import authorize
        mock_handler = Mock()
        mock_handler.principal = None
        mock_handler_method = Mock()
        handler = authorize()(mock_handler_method)
        response = handler(mock_handler)
        assert 401 == response.status_code

    def test_check_authenticated(self):
        """ Check if call is authenticated.

            @authorize
            def get(self):
                ...
        """
        from wheezy.web.authorization import authorize
        mock_handler = Mock()
        mock_handler.principal = 'UserA'
        mock_handler_method = Mock(return_value='response')
        handler = authorize()(mock_handler_method)
        assert 'response' == handler(mock_handler)
        mock_handler_method.assert_called_once_with(mock_handler)

    def test_check_authorized_but_not_authenticated(self):
        """ Check if call is authenticated

            @authorize(roles=('admin',))
            def get(self):
                ...
        """
        from wheezy.web.authorization import authorize
        mock_handler = Mock()
        mock_handler.principal = None
        mock_handler_method = Mock()
        handler = authorize(roles=('admin',))(mock_handler_method)
        response = handler(mock_handler)
        assert 401 == response.status_code

    def test_check_not_authorized(self):
        """ Check if call is not authorized.

            @authorize(roles=('admin',))
            def get(self):
                ...
        """
        from wheezy.web.authorization import authorize
        mock_principal = Mock()
        mock_principal.roles = ['user']
        mock_handler = Mock()
        mock_handler.principal = mock_principal
        mock_handler_method = Mock()
        handler = authorize(roles=('admin',))(mock_handler_method)
        response = handler(mock_handler)
        assert 401 == response.status_code

    def test_check_authorized(self):
        """ Check if call is authorized.

            @authorize(roles=('admin',))
            def get(self):
                ...
        """
        from wheezy.web.authorization import authorize
        mock_principal = Mock()
        mock_principal.roles = ['user', 'admin']
        mock_handler = Mock()
        mock_handler.principal = mock_principal
        mock_handler_method = Mock(return_value='response')
        handler = authorize(roles=('admin',))(mock_handler_method)
        assert 'response' == handler(mock_handler)

    def test_wrapped(self):
        """ Check decorator.
        """
        from wheezy.web.authorization import authorize
        mock_handler = Mock()
        mock_handler.principal = 'UserA'

        @authorize
        def get(self):
            return 'response'
        assert 'response' == get(mock_handler)
