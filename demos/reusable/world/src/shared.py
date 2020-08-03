import os.path

from wheezy.web.handlers.file import FileHandler


def import_urls(name):
    return __import__(name + ".web.urls", fromlist="all_urls").all_urls


def resolve_searchpath(name, scope="templates"):
    return os.path.join(__import__(name).__path__[0], scope)


def file_handler(directories):
    assert directories
    searchpath = []
    for path in directories:
        abspath = os.path.abspath(path)
        assert os.path.exists(abspath)
        assert os.path.isdir(abspath)
        searchpath.append(abspath)

    def wraps(request):
        for abspath in searchpath:
            r = FileHandler(request, root=abspath)
            if r.status_code != 404:
                break
        return r

    return wraps
