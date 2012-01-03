"""
"""


class MakoTemplate(object):

    def __init__(self,
            directories=None,
            module_directory='/tmp/mako_modules',
            **kwargs):
        from mako.lookup import TemplateLookup

        self.template_lookup = TemplateLookup(
                directories=directories or ['content/templates'],
                module_directory=module_directory,
                **kwargs)

    def __call__(self, template_name, **kwargs):
        template = self.template_lookup.get_template(template_name)
        return template.render(
                **kwargs
        )
