
""" ``transforms`` module
"""


def handler_transforms(transform=None, transforms=None):
    def decorate(factory):
        if transform:
            def strategy(handler, *args, **kwargs):
                return transform(
                        handler.request,
                        factory(handler, *args, **kwargs))
        else:
            def strategy(handler, *args, **kwargs):
                request = handler.request
                response = factory(handler, *args, **kwargs)
                for transform in transforms:
                    response = transform(request, response)
                return response
        return strategy
    return decorate
