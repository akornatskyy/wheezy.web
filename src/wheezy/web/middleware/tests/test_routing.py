
""" Unit tests for ``wheezy.web.middleware.routing``.
"""

import unittest

from mock import Mock


class PathRoutingMiddlewareTestCase(unittest.TestCase):
    """ Test the ``PathRoutingMiddleware``.
    """

    def test_handler_is_none(self):
        """ There is no matching handler for incoming request.
        """
        from wheezy.web.middleware.routing import PathRoutingMiddleware
        mock_request = Mock()
        mock_request.environ = {
            'PATH_INFO': '/en/signin'
        }
        mock_following = Mock(return_value='response')
        mock_path_router = Mock()
        mock_path_router.match.return_value = (None, {})
        middleware = PathRoutingMiddleware(mock_path_router)
        assert 'response' == middleware(mock_request, mock_following)
        assert 'route_args' in mock_request.environ
        mock_path_router.match.assert_called_once_with('en/signin')

    def test_following_is_none(self):
        """ There is no matching handler for incoming request
            and following middleware is None.
        """
        from wheezy.web.middleware.routing import PathRoutingMiddleware
        mock_request = Mock()
        mock_request.environ = {
            'PATH_INFO': '/en/signin'
        }
        mock_path_router = Mock()
        mock_path_router.match.return_value = (None, {})
        middleware = PathRoutingMiddleware(mock_path_router)
        assert middleware(mock_request, None) is None
        assert 'route_args' in mock_request.environ

    def test_match(self):
        """ There is matching handler for incoming request.
        """
        from wheezy.web.middleware.routing import PathRoutingMiddleware
        mock_request = Mock()
        mock_request.environ = {
            'PATH_INFO': '/en/signin'
        }
        mock_path_router = Mock()
        mock_handler = Mock(return_value='response')
        mock_path_router.match.return_value = (mock_handler, {'locale': 'en'})
        middleware = PathRoutingMiddleware(mock_path_router)
        assert 'response' == middleware(mock_request, None)
        mock_path_router.match.assert_called_once_with('en/signin')
        assert 'route_args' in mock_request.environ
        mock_handler.assert_called_once_with(mock_request)


class PathRoutingMiddlewareFactoryTestCase(unittest.TestCase):
    """ Test the ``path_routing_middleware_factory``.
    """

    def test_call(self):
        """ Returns an instance of PathRoutingMiddleware.
        """
        from wheezy.web.middleware.routing \
            import path_routing_middleware_factory
        mock_path_router = Mock()
        assert path_routing_middleware_factory({
            'path_router': mock_path_router
        })
