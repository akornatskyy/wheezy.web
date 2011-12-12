"""
"""

from wheezy.http.response import bad_request
from wheezy.http.response import forbidden
from wheezy.http.response import not_found


def test_bad_request(request):
    return bad_request(request.config)

def test_forbidden(request):
    return forbidden(request.config)

def test_not_found(request):
    return not_found(request.config)

def test_internal_error(request):
    raise KeyError()
