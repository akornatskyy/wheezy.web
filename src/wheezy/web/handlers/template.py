"""
"""

from wheezy.core.descriptors import attribute
from wheezy.web.handlers.base import BaseHandler


def template_handler(name):
    return lambda request: TemplateHandler(request, name).response


class TemplateHandler(BaseHandler):

    def __init__(self, request, template_name):
        self.template_name = template_name
        super(TemplateHandler, self).__init__(request)

    @attribute
    def locale(self):
        return self.route_locale() or 'en'

    def get(self):
        return self.render_response(self.template_name)
