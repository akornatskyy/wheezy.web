from hello.web.views import WelcomeHandler


def namespace(ns):
    def url(pattern, handler, kwargs=None, name=None):
        if name:
            name = ns + ':' + name
        return pattern, handler, kwargs, name
    return url


url = namespace('hello')

all_urls = [
    url('', WelcomeHandler, name='welcome')
]
