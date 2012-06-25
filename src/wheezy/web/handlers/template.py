"""
"""

from wheezy.web.handlers.base import BaseHandler


def template_handler(template_name, status_code=200):
    """ Serves templates that does not require up front data processing.
    """
    return lambda request: TemplateHandler(
        request,
        template_name=template_name,
        status_code=status_code)


class TemplateHandler(BaseHandler):
    """ Serves templates that does not require up front data processing.
    """

    def __init__(self, request, template_name, status_code=200):
        self.template_name = template_name
        self.status_code = status_code
        super(TemplateHandler, self).__init__(request)

    def get(self):
        response = self.render_response(self.template_name)
        response.status_code = self.status_code
        return response
