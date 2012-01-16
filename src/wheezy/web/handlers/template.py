"""
"""

from wheezy.http.transforms import gzip_transform
from wheezy.web.handlers.base import BaseHandler
from wheezy.web.transforms import handler_transforms


def template_handler(template_name, status_code=200):
    return lambda request: TemplateHandler(
            request,
            template_name=template_name,
            status_code=status_code)


class TemplateHandler(BaseHandler):

    def __init__(self, request, template_name, status_code=200):
        self.template_name = template_name
        self.status_code = status_code
        super(TemplateHandler, self).__init__(request)

    @handler_transforms(gzip_transform)
    def get(self):
        response = self.render_response(self.template_name)
        response.status_code = self.status_code
        return response
