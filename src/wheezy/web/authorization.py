
"""
"""

from wheezy.http import unauthorized


def authorize(wrapped=None, roles=None):
    """ Checks if user accessing protected resource is
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
                    if any(role in principal_roles for role in roles):
                        return func(handler, *args, **kwargs)
                    else:
                        return unauthorized(handler.options)
                else:
                    return unauthorized(handler.options)
            return check_roles
        else:
            def check_authenticated(handler, *args, **kwargs):
                if handler.principal:
                    return func(handler, *args, **kwargs)
                else:
                    return unauthorized(handler.options)
            return check_authenticated
    if wrapped is None:
        return decorate
    else:
        return decorate(wrapped)
