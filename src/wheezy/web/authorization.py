
"""
"""

from wheezy.core.url import UrlParts
from wheezy.http import permanent_redirect
from wheezy.http import unauthorized


def authorize(wrapped=None, roles=None):
    """ Checks if user is accessing protected resource is
        authenticated and optionally in one of allowed ``roles``.

        ``roles`` - a list of authorized roles.

        Check if call is authenticated::

            class MyHandler(BaseHandler):
                @authorize
                def get(self):
                    return response

        Check if principal in role::

            class MyHandler(BaseHandler):
                @authorize(roles=('operator', 'manager'))
                def get(self):
                    return response
    """
    def decorate(func):
        if roles:
            def check_roles(handler, *args, **kwargs):
                principal = handler.principal
                if principal:
                    principal_roles = principal.roles
                    for role in roles:
                        if role in principal_roles:
                            break
                    else:
                        return unauthorized()
                    return func(handler, *args, **kwargs)
                else:
                    return unauthorized()
            return check_roles
        else:
            def check_authenticated(handler, *args, **kwargs):
                if handler.principal:
                    return func(handler, *args, **kwargs)
                else:
                    return unauthorized()
            return check_authenticated
    if wrapped is None:
        return decorate
    else:
        return decorate(wrapped)


def secure(wrapped=None, enabled=True):
    """ Checks if user is accessing protected resource via SSL and if
        not, issue permanent redirect to HTTPS location.

        ``enabled`` - whenever to do any checks (defaults to ``True``).

        Example::

            class MyHandler(BaseHandler):
                @secure
                def get(self):
                    ...
                    return response

        Using ``enabled``::

            class MyHandler(BaseHandler):
                @secure(enabled=False)
                def get(self):
                    ...
                    return response
    """
    def decorate(method):
        if not enabled:
            return method

        def check(handler, *args, **kwargs):
            if not handler.request.secure:
                parts = handler.request.urlparts
                parts = UrlParts(('https',  # scheme
                                  parts[1],  # netloc
                                  parts[2],  # path
                                  parts[3],  # query
                                  None,  # fragment
                                  ))
                return permanent_redirect(parts.geturl())
            return method(handler, *args, **kwargs)
        return check
    if wrapped is None:
        return decorate
    else:
        return decorate(wrapped)
