"""
"""

from wheezy.routing import url
from wheezy.web.handlers.template import template_handler

from error.web.views import test_bad_request
from error.web.views import test_forbidden
from error.web.views import test_internal_error
from error.web.views import test_not_found


error_urls = [
    url('400',
        template_handler('error/http400.html', status_code=400),
        name='http400'),
    url('403',
        template_handler('error/http403.html', status_code=403),
        name='http403'),
    url('404',
        template_handler('error/http404.html', status_code=404),
        name='http404'),
    url('500',
        template_handler('error/http500.html', status_code=500),
        name='http500'),
]

test_error_urls = [
    url('test-bad-request', test_bad_request, name='bad_request'),
    url('test-forbidden', test_forbidden, name='forbidden'),
    url('test-internal-error', test_internal_error, name='internal_error'),
    url('test-not-found', test_not_found, name='not_found'),
]
