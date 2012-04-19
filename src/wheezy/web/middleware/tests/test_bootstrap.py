
""" Unit tests for ``wheezy.web.middleware.bootstrap``.
"""

import unittest

from mock import Mock


class BootstrapWebDefaultsTestCase(unittest.TestCase):
    """ Test the ``bootstrap_defaults``.
    """

    def test_default_options(self):
        """ Ensure required keys exist.
        """
        from wheezy.web.middleware.bootstrap import bootstrap_defaults
        options = {}

        assert None == bootstrap_defaults({})(options)

        required_options = tuple(sorted(options.keys()))
        assert 21 == len(required_options)
        assert ('AUTH_COOKIE', 'AUTH_COOKIE_DOMAIN', 'AUTH_COOKIE_PATH',
                'AUTH_COOKIE_SECURE', 'CONTENT_TYPE', 'ENCODING',
                'ENVIRON_HOST', 'ENVIRON_HTTPS', 'ENVIRON_HTTPS_VALUE',
                'ENVIRON_REMOTE_ADDR', 'HTTP_COOKIE_DOMAIN',
                'HTTP_COOKIE_HTTPONLY', 'HTTP_COOKIE_SECURE',
                'MAX_CONTENT_LENGTH', 'RESUBMISSION_NAME', 'XSRF_NAME',
                'path_for', 'path_router', 'render_template', 'ticket',
                'translations_manager') == required_options

    def test_path_router(self):
        """ Ensure required keys exist.
        """
        from wheezy.web.middleware.bootstrap import bootstrap_defaults
        mock_path_router = Mock()
        options = {
                'path_router': mock_path_router
        }

        assert None == bootstrap_defaults({
            'signin': 'signin'
        })(options)

        required_options = tuple(sorted(options.keys()))
        assert 21 == len(required_options)
