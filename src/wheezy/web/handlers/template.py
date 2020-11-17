"""
"""

from wheezy.web.handlers.base import BaseHandler


def template_handler(template_name, status_code=200, translation_name=None):
    """Serves templates that does not require up front data processing."""

    def handle_request(request):
        h = object.__new__(TemplateHandler)
        h.__init__(request)
        h.template_name = template_name
        h.status_code = status_code
        h.helpers = {
            "_": h.options["translations_manager"][h.locale][
                translation_name
            ].gettext,
            "locale": h.locale,
            "path_for": h.path_for,
            "principal": h.principal,
            "route_args": h.route_args,
        }
        return h()

    return handle_request


class TemplateHandler(BaseHandler):
    """Serves templates that does not require up front data processing."""

    def get(self):
        response = self.render_response(self.template_name)
        response.status_code = self.status_code
        return response
