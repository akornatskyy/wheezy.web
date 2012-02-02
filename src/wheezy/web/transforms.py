
""" ``transforms`` module
"""


def handler_transforms(*transforms):
    """ Transforms is a way to manipulate handler response
        accordingly to some algorithm.
    """
    def decorate(factory):
        if len(transforms) == 1:
            transform = transforms[0]

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
