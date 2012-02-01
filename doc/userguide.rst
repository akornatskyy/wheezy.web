
User Guide
==========

:ref:`wheezy.web` is a lightweight `WSGI`_ framework that aims take most
benefits out of standard python library and serves a sort of glue with other
libraries. It can be run from python 2.4 up to most cutting age python 3.
The framework aims to alleviate the overhead associated with common activities
performed in Web application development.

:ref:`wheezy.web` framework follows the model–view–controller (MVC)
architectural pattern to separate the data model from the user interface. This
is considered a good practice as it modularizes code, promotes code reuse.

:ref:`wheezy.web` framework follows a push-based architecture. Handlers do
some processing, and then "push" the data to the template layer to render the
results.

Web Handlers
------------
Handler is any callable that accepts an instance of ``HTTPRequest`` and
returns ``HTTPResponse``::

    def handler(request):
        return response

:ref:`wheezy.web` comes with the following handlers:

* :py:class:`~wheezy.web.handlers.method.MethodHandler` - represents the most
  generic handler. It serves dispatcher purpose for HTTP request method (GET,
  POST, etc). Base class for all handlers.
* :py:class:`~wheezy.web.handlers.base.BaseHandler` - provides methods that
  integartes such features like: routing, i18n, model binding, template
  rendering, authentication, xsrf/resubmission protection.
* :py:class:`~wheezy.web.handlers.base.RedirectRouteHandler` - redirects to
  given route name.
* :py:class:`~wheezy.web.handlers.file.FileHandler` - serves static files out
  of some directory.
* :py:class:`~wheezy.web.handlers.template.TemplateHandler` - serves templates
  that doesn't require up front data processing.

MethodHandler
~~~~~~~~~~~~~

:ref:`wheezy.web` routes incoming web request to handler per url mapping:

.. literalinclude:: ../demos/hello/hello.py
   :lines: 27-30

You subclass from :py:class:`~wheezy.web.handlers.method.MethodHandler` or
:py:class:`~wheezy.web.handlers.base.BaseHandler` and
define methods ``get()`` or ``post()`` that handle HTTP request method ``GET``
or ``POST``.

.. literalinclude:: ../demos/hello/hello.py
   :lines: 13-18

This method must return ``HTTPResponse`` object.

:py:class:`~wheezy.web.handlers.method.MethodHandler` has a number of useful
attributes:

* ``options`` - a dictionary of application configuration options.
* ``request`` - an instance of ``wheezy.http.HTTPRequest``.
* ``route_args`` - a dictionary of arguments matched in url routing.
* ``cookies`` - a list of cookies that extend ``HTTPResponse``.

BaseHandler
~~~~~~~~~~~

:py:class:`~wheezy.web.handlers.base.BaseHandler` provides methods that
integarte such features like:

#. routing
#. i18n
#. model binding
#. template rendering
#. authentication
#. xsrf/resubmission protection.

Routing
^^^^^^^

Routing feature is provided via integartation with `wheezy.routing`_ package.
There the following methods:

* ``path_for(name, **kwargs)`` - returns url path by route name.
* ``absolute_url_for(name, **kwargs)`` - returns url by route name.
* ``redirect_for(name, **kwargs)`` - returns redirect response by route name.

All these methods support the following arguments:

* ``name`` - a name of the route.
* ``kwargs`` - extra arguments necessary for routing.

Please refer to `wheezy.routing`_ documentation for more information.

Internationalization
^^^^^^^^^^^^^^^^^^^^

Internationalization feature is provided via integartation with `wheezy.core`_
package (module ``i18n``). There are the following attributes:

* ``locale`` - default implementation return a value resolved from route
  arguments, particularly to name ``locale``.
* ``translations`` - returns ``TranslationsManager`` (`wheezy.core`_ feature)
  for the current locale.
* ``translation`` - returns translations for the current handler. Default
  implementation return ``NullTranslations`` object. Your application handler
  must override this attribute to provide valid ``gettext`` translations.

Here is example from :ref:`public_demo` demo application::

    class SignInHandler(BaseHandler):

        @attribute
        def translation(self):
            return self.translations['membership']

This code loads `membership` translations from `i18n`_ directory. In order
to function properly the following configuration options must be defined::

    from wheezy.core.i18n import TranslationsManager

    options = {}
    options['translations_manager'] = TranslationsManager(
                directories=['i18n'],
                default_lang='en')

See example in public demo application `config.py`_.

Model Binding
^^^^^^^^^^^^^

Once html form submitted, you need a way to bind these values to some domain
model, validate, report errors, etc. This is where integartation with
`wheezy.validation`_ package happens.

There are the following attributes and methods:

* ``errors`` - a dictionary where each key corresponds to attribute being
  validated and value to a list of errors reported.
* ``try_update_model(model, values=None)`` - tries update domain ``model``
  with ``values``. If ``values`` is not specified it is the same as using
  ``self.request.form``. You can pass here ``self.request.query`` or
  ``self.route_args``.
* ``ValidationMixin::validate(model, validator)`` - shortcut for domain
  ``model`` validation per ``validator``.
* ``ValidationMixin::error(message)`` - adds a general error (this error
  is added with key *__ERROR__*).

Here is example from :ref:`public_demo` demo application (see file
`membership/web/views.py`_)::

    class SignInHandler(BaseHandler):

        def get(self, credential=None):
            if self.principal:
                return self.redirect_for('default')
            credential = credential or Credential()
            return self.render_response('membership/signin.html',
                    credential=credential)

        def post(self):
            credential = Credential()
            if (not self.try_update_model(credential)
                or not self.validate(credential, credential_validator)):
                return self.get(credential)
            return self.redirect_for('default')

This handler on post updates ``credential`` with values from html form
submitted. In case ``try_update_model`` or ``valida`` fails we re-display
sign in page with errors reported.

Here is example from :ref:`public_demo` demo application that demonstrates
how to use general error (see file `membership/web/views.py`_)::

    class SignUpHandler(BaseHandler):

        def post(self):
            if not self.validate_resubmission():
                self.error('Your registration request has been queued. '
                        'Please wait while your request will be processed. '
                        'If your request fails please try again.')
                return self.get()
            ...

Read more about model binding and validation in `wheezy.validation`_
package.

Templates
^^^^^^^^^

:ref:`wheezy.web` is not tied to some specific template engine, instead
it provides you with convinient contract to add one you prefer. Here is
how we add ``MakoTemplate`` renderer (see file `config.py`_)::

    from wheezy.web.templates import MakoTemplate

    options = {}
    options['render_template'] = MakoTemplate(
            directories=['content/templates'],
            filesystem_checks=False,
            template_cache=template_cache),

Template contract is any callable of the following form::

    def render_template(self, template_name, **kwargs):
        return string

There are the following attributes and methods:

* ``helpers`` - a dictionary of context objects to be passed to
  ``render_template`` implementation (you need to override this method
  in case you need more specific context information in template).

  * ``_`` - ``gettext`` translations support.
  * ``route_args``, ``absolute_url_for``, ``path_for`` - relates to
    routing related methods.
  * ``principal`` - an instance of ``wheezy.security.Principal`` for the
    authenticated request or ``None``.
  * ``resubmission`` - resubmission HTML form widget.
  * ``xsrf`` - XSRF protection HTML form widget.
  
* ``render_template(template_name, **kwargs)`` - renders template with name
  ``template_name`` and pass it context information in ``**kwargs``.
* ``render_response(template_name, **kwargs)`` - writes result of 
  ``render_template`` into ``wheezy.http.HTTPResponse`` and return it.

Authentication
^^^^^^^^^^^^^^

Authentication is a process of confirming the truth of security principal.
In web application it usually relates to creating an encrypted cookie value
so it can not be easily compromised by attacker. This is where integration 
with `wheezy.security`_ happens.

The process of creating authentication cookie is as simple as assiging 
instance of ``wheezy.security.Principal`` to attribute ``principal``. Let
demonstrate this by example::

    from wheezy.security import Principal

    class SignInHandler(BaseHandler):
    
        def post(self):
            ...
            self.principal = Principal(
                id=credential.username,
                alias=credential.username)

Once we confirmed user has entered valid username and password we create
an instance of ``Principal`` and assign it to ``principal`` attribute. In
``setprincipal`` implementation authentication cookie is created with a
dump of ``Principal`` object and it value is protected by 
``wheezy.security.crypto.Ticket`` (read more in `wheezy.security`_).

Here are authentication configuration options (see file `config.py`_)::

    # wheezy.security.crypto.Ticket
    options = {}
    options.update({
            'CRYPTO_ENCRYPTION_KEY': '4oqiKhW3qzP2EiattMt7',
            'CRYPTO_VALIDATION_KEY': 'A7GfjxIBCBA3vNqvafWf'
    })

    options.update({
            'ticket': Ticket(
                max_age=1200,
                salt='JNbCog95cDTo1NRb7inP',
                options=options),

            'AUTH_COOKIE': '_a',
            'AUTH_COOKIE_DOMAIN': None,
            'AUTH_COOKIE_PATH': '',
            'AUTH_COOKIE_SECURE': False,
    })
    
You can obtain current security ``Principal`` by requesting ``principal``
attribute. The example below redirects user to default route in case he 
or she is already authenticated::

    class SignInHandler(BaseHandler):

        def get(self, credential=None):
            if self.principal:
                return self.redirect_for('default')

Sign out is even simpler. You delete ``principal`` attribute::

    class SignOutHandler(BaseHandler):

        def get(self):
            del self.principal
            return self.redirect_for('default')










.. _`WSGI`: http://www.python.org/dev/peps/pep-3333
.. _`wheezy.core`: http://bitbucket.org/akorn/wheezy.core
.. _`wheezy.http`: http://packages.python.org/wheezy.http
.. _`wheezy.routing`: http://packages.python.org/wheezy.routing
.. _`wheezy.validation`: http://packages.python.org/wheezy.validation
.. _`wheezy.security`: http://packages.python.org/wheezy.security
.. _`i18n`: https://bitbucket.org/akorn/wheezy.web/src/tip/demos/public/i18n
.. _`config.py`: https://bitbucket.org/akorn/wheezy.web/src/tip/demos/public/src/config.py
.. _`membership/web/views.py`: https://bitbucket.org/akorn/wheezy.web/src/tip/demos/public/src/membership/web/views.py
