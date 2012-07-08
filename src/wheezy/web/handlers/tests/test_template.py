
""" Unit tests for ``wheezy.web.handlers.base``.
"""

import unittest

from mock import Mock


class TemplateHandlerTestCase(unittest.TestCase):
    """ Test the ``TemplateHandler``.
    """

    def setUp(self):
        from wheezy.web.handlers.template import TemplateHandler
        from wheezy.web.handlers.method import handler_factory
        self.options = {
            'CONTENT_TYPE': 'text/plain',
            'ENCODING': 'UTF-8',
            'AUTH_COOKIE': '_a'
        }
        self.mock_request = Mock()
        self.mock_request.options = self.options
        self.route_args = {'locale': 'en'}
        self.mock_request.environ = {
            'route_args': self.route_args
        }
        self.mock_request.root_path = 'my_site/'
        self.mock_request.cookies = {}
        self.handler = handler_factory(
            TemplateHandler,
            self.mock_request,
            template_name='test.html')

    def test_get(self):
        """ get.
        """
        mock_render_template = Mock()
        self.options['render_template'] = mock_render_template
        response = self.handler.get()
        assert 200 == response.status_code

        self.handler.status_code = 404
        response = self.handler.get()
        assert 404 == response.status_code


class TemplateHandlerFactoryTestCase(unittest.TestCase):
    """ Test the ``template_handler``.
    """

    def setUp(self):
        self.options = {
            'CONTENT_TYPE': 'text/plain',
            'ENCODING': 'UTF-8',
            'AUTH_COOKIE': '_a'
        }
        self.mock_request = Mock()
        self.mock_request.options = self.options
        self.route_args = {'locale': 'en'}
        self.mock_request.environ = {
            'route_args': self.route_args
        }
        self.mock_request.method = 'GET'
        self.mock_request.root_path = 'my_site/'
        self.mock_request.cookies = {}

    def test_get(self):
        """ get.
        """
        from wheezy.web.handlers.template import template_handler
        mock_render_template = Mock()
        self.options['render_template'] = mock_render_template
        handler = template_handler('test.html', status_code=404)
        response = handler(self.mock_request)
        assert 404 == response.status_code
