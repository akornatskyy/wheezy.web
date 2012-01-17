"""
"""

from wheezy.http.response import bad_request
from wheezy.http.response import forbidden
from wheezy.http.response import not_found
from wheezy.web.handlers.template import template_handler


http400 = template_handler('error/http400.html', status_code=400)
http403 = template_handler('error/http403.html', status_code=403)
http404 = template_handler('error/http404.html', status_code=404)
http500 = template_handler('error/http500.html', status_code=500)


def test_bad_request(request):
    return bad_request(request.config)


def test_forbidden(request):
    return forbidden(request.config)


def test_not_found(request):
    return not_found(request.config)


def test_internal_error(request):
    raise NotImplementedError('Not implemented yet')
