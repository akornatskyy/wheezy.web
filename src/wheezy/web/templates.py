"""
"""


class MakoTemplate(object):
    """ Integration with Mako templates.
    """
    __slots__ = ('template_lookup')

    def __init__(
            self, directories=None,
            module_directory='/tmp/mako_modules',
            cache_factory=None,
            **kwargs):
        from mako.lookup import TemplateLookup
        if cache_factory is None:
            self.template_lookup = TemplateLookup(
                directories=directories or ['content/templates'],
                module_directory=module_directory,
                **kwargs)
        else:
            from mako.cache import register_plugin
            register_plugin('wheezy', 'wheezy.web.templates', 'MakoCacheImpl')
            self.template_lookup = TemplateLookup(
                directories=directories or ['content/templates'],
                module_directory=module_directory,
                cache_impl='wheezy',
                cache_args={'cache_factory': cache_factory},
                **kwargs)

    def __call__(self, template_name, kwargs):
        template = self.template_lookup.get_template(template_name)
        return template.render(**kwargs)


class MakoCacheImpl(object):
    __slots__ = ('cache_factory', 'prefix')

    pass_context = False

    def __init__(self, cache):
        self.cache_factory = cache.template.cache_args['cache_factory']
        self.prefix = cache.id

    def get_or_create(self, key, creation_function, **kwargs):
        namespace = kwargs.get('namespace', None)
        context = self.cache_factory()
        cache = context.__enter__()
        try:
            value = cache.get(self.prefix + key, namespace)
            if value is None:
                value = creation_function()
                cache.add(
                    self.prefix + key,
                    value,
                    int(kwargs.get('time', 0)),
                    namespace)
            return value
        finally:
            context.__exit__(None, None, None)

    def set(self, key, value, **kw):
        raise NotImplementedError()

    def get(self, key, **kw):
        raise NotImplementedError()

    def invalidate(self, key, **kw):
        raise NotImplementedError()


class TenjinTemplate(object):
    """ Integration with Tenjin templates.
    """
    __slots__ = ('engine', 'helpers')

    def __init__(
            self, path=None, pp=None, helpers=None,
            encoding='UTF-8', postfix='.html', cache=None, **kwargs):
        import tenjin
        tenjin.set_template_encoding(encoding)
        from tenjin.helpers import capture_as, captured_as, cache_as
        try:  # pragma: nocover
            from webext import escape_html as escape
        except ImportError:  # pragma: nocover
            from tenjin.helpers import escape

        from wheezy.core.comp import str_type
        self.helpers = {
            'to_str': str_type,
            'escape': escape,
            'capture_as': capture_as,
            'captured_as': captured_as,
            'cache_as': cache_as,
            'tenjin': tenjin
        }
        if helpers:
            self.helpers.update(helpers)
        self.engine = tenjin.Engine(
            path=path or ['content/templates'],
            postfix=postfix,
            cache=cache or tenjin.MemoryCacheStorage(),
            pp=pp,
            **kwargs)

    def __call__(self, template_name, kwargs):
        return self.engine.render(template_name, kwargs, self.helpers)


class Jinja2Template(object):
    """ Integration with Jinja2 templates.
    """

    def __init__(self, env):
        assert env
        self.env = env

    def __call__(self, template_name, kwargs):
        return self.env.get_template(template_name).render(kwargs)


class WheezyTemplate(object):
    """ Integration with wheezy.template.
    """

    def __init__(self, engine):
        assert engine
        self.render = engine.render

    def __call__(self, template_name, kwargs):
        return self.render(template_name, kwargs, {}, {})
