""" ``handlers`` package.
"""

# flake8: noqa

from wheezy.web.handlers.base import (
    BaseHandler,
    RedirectRouteHandler,
    permanent_redirect_handler,
    redirect_handler,
)
from wheezy.web.handlers.file import FileHandler, file_handler
from wheezy.web.handlers.method import MethodHandler
from wheezy.web.handlers.template import TemplateHandler, template_handler

__all__ = (
    "BaseHandler",
    "RedirectRouteHandler",
    "permanent_redirect_handler",
    "redirect_handler",
    "FileHandler",
    "file_handler",
    "MethodHandler",
    "TemplateHandler",
    "template_handler",
)
