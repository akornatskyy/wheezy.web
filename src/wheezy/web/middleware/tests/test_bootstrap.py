
""" Unit tests for ``wheezy.web.middleware.bootstrap``.
"""

import unittest

from mock import Mock
from mock import patch


class BootstrapWebDefaultsTestCase(unittest.TestCase):
    """ Test the ``bootstrap_defaults``.
    """

    def setUp(self):
        from wheezy.web.middleware import bootstrap
        self.patcher = patch.object(bootstrap, 'bootstrap_http_defaults')
        self.patcher.start()

    def tearDown(self):
        self.patcher.stop()

    def test_default_options(self):
        """ Ensure required keys exist.
        """
        from wheezy.web.middleware.bootstrap import bootstrap_defaults
        options = {}

        assert None == bootstrap_defaults({})(options)

        required_options = tuple(sorted(options.keys()))
        assert 12 == len(required_options)
        assert ('AUTH_COOKIE', 'AUTH_COOKIE_DOMAIN', 'AUTH_COOKIE_PATH',
                'AUTH_COOKIE_SECURE', 'CONTENT_TYPE', 'ENCODING',
                'RESUBMISSION_NAME', 'XSRF_NAME', 'path_for', 'path_router',
                'ticket', 'translations_manager') == required_options

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

        assert tuple(options.keys())
