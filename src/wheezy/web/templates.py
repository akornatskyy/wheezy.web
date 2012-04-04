"""
"""


class MakoTemplate(object):

    def __init__(self,
            directories=None,
            module_directory='/tmp/mako_modules',
            cache_factory=None,
            **kwargs):
        from mako.cache import register_plugin
        from mako.lookup import TemplateLookup

        register_plugin('wheezy', 'wheezy.web.templates', 'MakoCacheImpl')
        self.template_lookup = TemplateLookup(
                directories=directories or ['content/templates'],
                module_directory=module_directory,
                cache_impl='wheezy',
                cache_args={'cache_factory': cache_factory},
                **kwargs)

    def __call__(self, template_name, **kwargs):
        template = self.template_lookup.get_template(template_name)
        return template.render(
                **kwargs
        )


class MakoCacheImpl(object):

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
