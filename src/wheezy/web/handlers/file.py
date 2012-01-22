"""
"""

import mimetypes
import os.path
import stat

from datetime import datetime
from datetime import timedelta

from wheezy.core.datetime import parse_http_datetime
from wheezy.http import HTTPResponse
from wheezy.http import HTTPCachePolicy
from wheezy.web.handlers.method import MethodHandler


HTTP_HEADER_ACCEPT_RANGE_NONE = ('Accept-Ranges', 'none')


def file_handler(root, age=None):
    abspath = os.path.abspath(root)
    assert os.path.exists(abspath)
    assert os.path.isdir(abspath)
    return lambda request: FileHandler(
            request,
            root=abspath,
            age=age)


class FileHandler(MethodHandler):

    def __init__(self, request, root, age=None):
        assert age is None or isinstance(age, timedelta)
        self.root = root
        self.age = age
        super(FileHandler, self).__init__(request)

    def head(self):
        return self.get(skip_body=True)

    def get(self, skip_body=False):
        route_args = self.route_args
        path = route_args['path']
        assert path
        abspath = os.path.abspath(os.path.join(self.root, path))
        if not abspath.startswith(self.root):
            return forbidden()
        if not os.path.exists(abspath):
            return not_found()
        if not os.path.isfile(abspath):
            return forbidden()

        mime_type, encoding = mimetypes.guess_type(abspath)
        request = self.request
        response = HTTPResponse(
                content_type=mime_type or 'plain/text',
                encoding=encoding,
                options=request.config)

        response.cache = cache_policy = HTTPCachePolicy('public')

        last_modified_stamp = os.stat(abspath)[stat.ST_MTIME]
        last_modified = datetime.utcfromtimestamp(last_modified_stamp)
        cache_policy.last_modified(last_modified)

        age = self.age
        if age:
            cache_policy.max_age(age)
            cache_policy.expires(datetime.utcnow() + age)

        environ = request.environ
        modified_since = environ.get('HTTP_IF_MODIFIED_SINCE', None)
        if modified_since:
            modified_since = parse_http_datetime(modified_since)
            if modified_since >= last_modified:
                response.status_code = 304
                skip_body = True

        etag = '\"' + hex(last_modified_stamp)[2:] + '\"'
        cache_policy.etag(etag)
        none_match = environ.get('HTTP_IF_NONE_MATCH', None)
        if none_match and etag in none_match:
            response.status_code = 304
            skip_body = True

        if not skip_body:
            response.headers.append(HTTP_HEADER_ACCEPT_RANGE_NONE)
            file = open(abspath, 'rb')
            try:
                response.write(file.read())
            finally:
                file.close()
        else:
            response.skip_body = True
        return response
