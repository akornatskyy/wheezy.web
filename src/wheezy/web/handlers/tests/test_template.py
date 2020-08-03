""" Unit tests for ``wheezy.web.handlers.base``.
"""

import unittest

from mock import Mock


class TemplateHandlerFactoryTestCase(unittest.TestCase):
    """ Test the ``template_handler``.
    """

    def setUp(self):
        from wheezy.core.i18n import null_translations

        self.options = {
            "CONTENT_TYPE": "text/plain",
            "ENCODING": "UTF-8",
            "AUTH_COOKIE": "_a",
            "translations_manager": {"en": {None: null_translations}},
        }
        self.mock_request = Mock()
        self.mock_request.options = self.options
        self.route_args = {"locale": "en"}
        self.mock_request.environ = {"route_args": self.route_args}
        self.mock_request.method = "GET"
        self.mock_request.root_path = "my_site/"
        self.mock_request.cookies = {}

    def test_get(self):
        """ get.
        """
        from wheezy.web.handlers.template import template_handler

        mock_render_template = Mock()
        self.options["render_template"] = mock_render_template
        handler = template_handler("test.html", status_code=404)
        response = handler(self.mock_request)
        assert 404 == response.status_code
