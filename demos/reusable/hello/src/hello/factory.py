from wheezy.core.descriptors import attribute

from hello.service.bridge import HelloService


class HelloFactoryMixin(object):

    @attribute
    def hello(self):
        context = self.context
        return HelloService(self.factory,
                            context['errors'],
                            context['locale'])
