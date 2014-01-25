"""
"""

import mimetypes
import os.path

from wheezy.http import HTTPResponse
from wheezy.http import forbidden
from wheezy.http import not_found
from wheezy.web.handlers.method import MethodHandler


HTTP_HEADER_ACCEPT_RANGE_NONE = ('Accept-Ranges', 'none')


def file_handler(root):
    """ Serves static files out of some directory.
    """
    abspath = os.path.abspath(root)
    assert os.path.exists(abspath)
    assert os.path.isdir(abspath)
    return lambda request: FileHandler(
        request,
        root=abspath)


class FileHandler(MethodHandler):
    """ Serves static files out of some directory.
    """

    def __init__(self, request, root):
        self.root = root
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
        response = HTTPResponse(mime_type or 'plain/text', encoding)
        if not skip_body:
            response.headers.append(HTTP_HEADER_ACCEPT_RANGE_NONE)
            file = open(abspath, 'rb')
            try:
                response.write_bytes(file.read())
            finally:
                file.close()
        return response
