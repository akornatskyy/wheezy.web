from wheezy.validation.mixin import ErrorsMixin


class HelloService(ErrorsMixin):

    def __init__(self, factory, errors, locale):
        self.factory = factory
        self.errors = errors
        self.locale = locale

    def say_hi(self, someone):
        return 'Hello ' + someone + '!'
