from hello.service.bridge import HelloService

from wheezy.core.descriptors import attribute


class HelloFactoryMixin(object):
    @attribute
    def hello(self):
        context = self.context
        return HelloService(self.factory, context["errors"], context["locale"])
