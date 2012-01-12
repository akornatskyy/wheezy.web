"""
"""


class MakoTemplate(object):

    def __init__(self,
            directories=None,
            module_directory='/tmp/mako_modules',
            template_cache=None,
            **kwargs):
        from mako.cache import register_plugin
        from mako.lookup import TemplateLookup

        register_plugin('wheezy', 'wheezy.web.templates', 'MakoCacheImpl')
        self.template_lookup = TemplateLookup(
                directories=directories or ['content/templates'],
                module_directory=module_directory,
                cache_impl='wheezy',
                cache_args={'template_cache': template_cache},
                **kwargs)

    def __call__(self, template_name, **kwargs):
        template = self.template_lookup.get_template(template_name)
        return template.render(
                **kwargs
        )


class MakoCacheImpl(object):

    def __init__(self, cache):
        self.template_cache = cache.template.cache_args['template_cache']
        self.prefix = cache.template.module.__name__

    def get_and_replace(self, key, creation_function, **kwargs):
        value = self.template_cache.get(self.prefix + key)
        if value is None:
            value = creation_function()
            self.template_cache.add(
                    self.prefix + key,
                    value,
                    time=kwargs.pop('time', 0))
        return value

    def put(self, key, value, **kw):
        raise NotImplementedError()

    def get(self, key, **kw):
        raise NotImplementedError()

    def invalidate(self, key, **kw):
        raise NotImplementedError()
