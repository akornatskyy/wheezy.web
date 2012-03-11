
""" ``caching`` module.
"""


def handler_cache(profile):
    """ Decorator that applies cache profile strategy to the
        wrapping handler.
    """
    def decorate(method):
        if not profile.enabled:
            return method

        if profile.request_vary:
            def cache(handler, *args, **kwargs):
                response = method(handler, *args, **kwargs)
                response.cache_profile = profile
                if response.cache_policy is None:
                    response.cache_policy = profile.cache_policy()
                return response
            return cache
        else:
            def no_cache(handler, *args, **kwargs):
                response = method(handler, *args, **kwargs)
                if response.cache_policy is None:
                    response.cache_policy = profile.cache_policy()
                return response
            return no_cache
    return decorate
