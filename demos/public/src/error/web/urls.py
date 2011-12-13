"""
"""

from wheezy.routing import url

from error.web.views import http400
from error.web.views import http403
from error.web.views import http404
from error.web.views import http500
from error.web.views import test_bad_request
from error.web.views import test_forbidden
from error.web.views import test_internal_error
from error.web.views import test_not_found


error_urls = [
    url('400', http400, name='http400'),
    url('403', http403, name='http403'),
    url('404', http404, name='http404'),
    url('500', http500, name='http500'),
]

test_error_urls = [
    url('test-bad-request', test_bad_request, name='bad_request'),
    url('test-forbidden', test_forbidden, name='forbidden'),
    url('test-internal-error', test_internal_error, name='internal_error'),
    url('test-not-found', test_not_found, name='not_found'),
]
