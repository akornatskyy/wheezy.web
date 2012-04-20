
""" Unit tests for ``wheezy.web.middleware.errors``.
"""

import unittest

from mock import Mock
from mock import patch


class MakoTemplateTestCase(unittest.TestCase):
    """ Test the ``MakoTemplate``.
    """

    def setUp(self):
        from mako import cache
        from mako import lookup
        self.patcher_cache = patch.object(cache, 'register_plugin')
        self.mock_register_plugin = self.patcher_cache.start()
        self.patcher_lookup = patch.object(lookup, 'TemplateLookup')
        self.mock_template_lookup_class = self.patcher_lookup.start()

    def tearDown(self):
        self.patcher_lookup.stop()
        self.patcher_cache.stop()

    def test_init_with_defaults(self):
        """ Check __init__ with all default values.
        """
        from wheezy.web.templates import MakoTemplate
        assert MakoTemplate()
        assert not self.mock_register_plugin.called
        self.mock_template_lookup_class.assert_called_once_with(
                directories=['content/templates'],
                module_directory='/tmp/mako_modules',
        )

    def test_init_with_cache_factory(self):
        """ Check __init__ with specified cache_factory
        """
        from wheezy.web.templates import MakoTemplate
        assert MakoTemplate(
                cache_factory='mock_cache_factory'
        )
        self.mock_template_lookup_class.assert_called_once_with(
                directories=['content/templates'],
                module_directory='/tmp/mako_modules',
                cache_impl='wheezy',
                cache_args={'cache_factory': 'mock_cache_factory'}
        )
        self.mock_register_plugin.assert_called_once_with(
                'wheezy', 'wheezy.web.templates', 'MakoCacheImpl')

    def test_render(self):
        """ __call__.
        """
        from wheezy.web.templates import MakoTemplate
        self.mock_template_lookup_class.return_value \
                .get_template.return_value.render.return_value = 'html'
        template = MakoTemplate()
        assert 'html' == template('signin.html', user='john')
        self.mock_template_lookup_class.return_value \
                .get_template.assert_called_once_with('signin.html')
        self.mock_template_lookup_class.return_value \
                .get_template.return_value \
                .render.assert_called_once_with(user='john')


class MakoCacheImplTestCase(unittest.TestCase):
    """ Test the ``MakoCacheImpl``.
    """

    def setUp(self):
        from wheezy.web.templates import MakoCacheImpl
        self.mock_cache_factory = Mock()
        mock_mako_cache = Mock()
        mock_mako_cache.template.cache_args = {
                'cache_factory': self.mock_cache_factory
        }
        mock_mako_cache.id = 'prefix-'
        self.cache = MakoCacheImpl(mock_mako_cache)

    def test_init(self):
        """ __init__.
        """
        assert 'prefix-' == self.cache.prefix
        assert self.mock_cache_factory == self.cache.cache_factory

    def test_not_implemented(self):
        """ set, get and invalidate raise error.
        """
        self.assertRaises(NotImplementedError,
                lambda: self.cache.set('key', 1))
        self.assertRaises(NotImplementedError,
                lambda: self.cache.get('key'))
        self.assertRaises(NotImplementedError,
                lambda: self.cache.invalidate('key'))

    def test_get_or_create_missing_in_cache(self):
        """ Requested item is missing in cache.
        """
        mock_cache = Mock()
        mock_cache.get.return_value = None
        mock_context = Mock()
        mock_context.__enter__ = Mock(return_value=mock_cache)
        mock_context.__exit__ = Mock()
        self.mock_cache_factory.return_value = mock_context
        mock_creation_function = Mock(return_value='html')
        assert 'html' == self.cache.get_or_create(
                'key',
                mock_creation_function,
                namespace='namespace',
                time='100')
        mock_cache.get.assert_called_once_with(
                'prefix-key', 'namespace')
        mock_cache.add.assert_called_once_with(
                'prefix-key', 'html', 100, 'namespace')

    def test_get_or_create_found_in_cache(self):
        """ Requested item found in cache.
        """
        mock_cache = Mock()
        mock_cache.get.return_value = 'html'
        mock_context = Mock()
        mock_context.__enter__ = Mock(return_value=mock_cache)
        mock_context.__exit__ = Mock()
        self.mock_cache_factory.return_value = mock_context
        mock_creation_function = Mock()
        assert 'html' == self.cache.get_or_create(
                'key',
                mock_creation_function,
                namespace='namespace',
                time='100')
        mock_cache.get.assert_called_once_with(
                'prefix-key', 'namespace')
        assert not mock_creation_function.called