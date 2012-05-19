
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


class TenjinTemplateTestCase(unittest.TestCase):
    """ Test the ``TenjinTemplate``.
    """

    def setUp(self):
        import tenjin
        self.patcher_encoding = patch.object(tenjin, 'set_template_encoding')
        self.mock_encoding = self.patcher_encoding.start()
        self.patcher_cache = patch.object(tenjin, 'MemoryCacheStorage')
        self.mock_cache = self.patcher_cache.start()
        self.patcher_engine = patch.object(tenjin, 'Engine')
        self.mock_engine = self.patcher_engine.start()

    def tearDown(self):
        self.patcher_engine.stop()
        self.patcher_cache.stop()
        self.patcher_encoding.stop()

    def test_init_with_defaults(self):
        """ Check __init__ with all default values.
        """
        from wheezy.web.templates import TenjinTemplate
        template = TenjinTemplate()
        assert ['cache_as', 'capture_as', 'captured_as',
                'escape', 'to_str'] == sorted(template.helpers.keys())
        self.mock_encoding.assert_called_once_with('UTF-8')
        self.mock_cache.assert_called_once_with()
        self.mock_engine.assert_called_once_with(
                path=['content/templates'],
                postfix='.html',
                pp=None,
                cache=self.mock_cache.return_value
        )

    def test_init_with_helpers(self):
        """ Check __init__ with helpers values.
        """
        from wheezy.web.templates import TenjinTemplate
        helpers = {
                'to_str': 'to_str',
                'escape': 'escape',
                'capture_as': 'capture_as',
                'captured_as': 'captured_as',
                'cache_as': 'cache_as',
        }
        template = TenjinTemplate(helpers=helpers)
        assert helpers == template.helpers

    def test_render(self):
        """ __call__.
        """
        from wheezy.web.templates import TenjinTemplate
        mock_render = self.mock_engine.return_value.render
        mock_render.return_value = 'html'
        template = TenjinTemplate()
        assert 'html' == template('signin.html', user='john')
        mock_render.assert_called_once_with('signin.html', {
                'user': 'john'
            }, template.helpers)


class Jinja2TemplateTestCase(unittest.TestCase):
    """ Test the ``Jinja2Template``.
    """

    def test_init(self):
        """ Assert environment is not None
        """
        from wheezy.web.templates import Jinja2Template
        self.assertRaises(AssertionError, lambda: Jinja2Template(None))

    def test_render(self):
        """ __call__.
        """
        from wheezy.web.templates import Jinja2Template
        mock_env = Mock()
        mock_render = mock_env.get_template.return_value.render
        mock_render.return_value = 'html'
        template = Jinja2Template(mock_env)
        assert 'html' == template('signin.html', user='john')
        mock_env.get_template.assert_called_once_with('signin.html')
        mock_render.assert_called_once_with({
                'user': 'john'
            })
