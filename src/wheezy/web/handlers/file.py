"""
"""

import mimetypes
import os.path
import stat

from datetime import datetime

from wheezy.core.datetime import parse_http_datetime
from wheezy.http.cachepolicy import HttpCachePolicy
from wheezy.http.response import HttpResponse
from wheezy.web.handlers.method import MethodHandler


def file_handler(root, age=0):
    abspath = os.path.abspath(root)
    assert os.path.exists(abspath)
    assert os.path.isdir(abspath)
    return lambda request: FileHandler(
            request,
            root=abspath,
            age=age).response


class FileHandler(MethodHandler):

    def __init__(self, request, root, age=0):
        self.root = root
        self.age = age
        super(FileHandler, self).__init__(request)

    def head(self):
        return self.get(skip_body=True)

    def get(self, skip_body=False):
        route_kwargs = self.request.ROUTE
        assert route_kwargs
        path = route_kwargs.get('path', None)
        assert path
        abspath = os.path.abspath(os.path.join(self.root, path))
        if not abspath.startswith(self.root):
            return forbidden()
        if not os.path.exists(abspath):
            return not_found()
        if not os.path.isfile(abspath):
            return forbidden()

        mime_type, encoding = mimetypes.guess_type(abspath)
        response = HttpResponse(
                content_type=mime_type or 'plain/text',
                encoding=encoding,
                options=self.request.config)

        response.cache = cache_policy = HttpCachePolicy('public')

        last_modified_stamp = os.stat(abspath)[stat.ST_MTIME]
        last_modified = datetime.utcfromtimestamp(last_modified_stamp)
        cache_policy.last_modified(last_modified)

        age = route_kwargs.get('age', None)
        if age:
            cache_policy.max_age(age)
            cache_policy.expires(datetime.utcnow() + age)

        modified_since = self.request.HEADERS.IF_MODIFIED_SINCE
        if modified_since:
            modified_since = parse_http_datetime(modified_since)
            if modified_since >= last_modified:
                response.status_code = 304
                skip_body = True

        etag = '\"' + hex(last_modified_stamp)[2:] + '\"'
        cache_policy.etag(etag)
        none_match = self.request.HEADERS.IF_NONE_MATCH
        if none_match and etag in none_match:
            response.status_code = 304
            skip_body = True

        if not skip_body:
            response.headers.append(('Accept-Ranges', 'none'))
            file = open(abspath, "rb")
            try:
                response.write(file.read())
            finally:
                file.close()
        else:
            response.skip_body = True
        return response
