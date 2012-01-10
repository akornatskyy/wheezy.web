
""" ``caching`` module.
"""

from wheezy.http.cache import get_or_set2


def handler_cache(profile, cache):
    def decorate(factory):
        strategy = factory
        if profile.enabled:

            def get_or_set_strategy(handler, *args, **kwargs):
                if args or kwargs:
                    response = factory(*args, **kwargs)
                else:
                    response = get_or_set2(
                            request=handler.request,
                            cache=cache,
                            cache_profile=profile,
                            factory=lambda ignore: factory(handler))
                return response

            def nocache_strategy(handler, *args, **kwargs):
                response = factory(handler, *args, **kwargs)
                if response.status_code == 200:
                    if response.cache is None:
                        response.cache = profile.cache_policy()
                return response

            if profile.request_vary:
                strategy = get_or_set_strategy
            else:
                strategy = nocache_strategy
        return strategy
    return decorate
