
""" ``caching`` module.
"""

from wheezy.http.cache import get_or_set2


def handler_cache(profile, cache=None):
    def decorate(factory):
        if not profile.enabled:
            return factory

        if profile.request_vary:
            assert cache is not None

            def strategy(handler, *args, **kwargs):
                if args or kwargs:
                    response = factory(*args, **kwargs)
                else:
                    response = get_or_set2(
                            request=handler.request,
                            cache=cache,
                            cache_profile=profile,
                            factory=lambda ignore: factory(handler))
                return response
        else:
            def strategy(handler, *args, **kwargs):
                response = factory(handler, *args, **kwargs)
                if response.status_code == 200:
                    if response.cache is None:
                        response.cache = profile.cache_policy()
                return response
        return strategy
    return decorate
