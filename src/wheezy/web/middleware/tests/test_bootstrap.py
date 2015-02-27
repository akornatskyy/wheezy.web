
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
        try:
            from warnings import catch_warnings
            self.ctx = catch_warnings(record=True)
            self.w = self.ctx.__enter__()
        except ImportError:
            self.ctx = None

    def tearDown(self):
        self.patcher.stop()
        if self.ctx:
            self.ctx.__exit__(None, None, None)

    def assert_warning(self, msg):
        if self.ctx:
            assert len(self.w) == 1
            self.assertEquals(msg, str(self.w[-1].message))

    def test_default_options(self):
        """ Ensure required keys exist.
        """
        from wheezy.web.middleware.bootstrap import bootstrap_defaults
        options = {}

        assert bootstrap_defaults({})(options) is None

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

        assert bootstrap_defaults({
            'signin': 'signin'
        })(options) is None

        assert tuple(options.keys())

    def test_warnings(self):
        """ Ensure warnings are issued.
        """
        from wheezy.web.middleware.bootstrap import bootstrap_defaults
        options = {
            'ticket': None
        }

        assert bootstrap_defaults({})(options) is None
        self.assert_warning('Bootstrap: render_template is not defined')
