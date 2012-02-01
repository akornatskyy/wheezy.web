
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
package (module ``i18n``). There the following attributes:

* ``locale`` - default implementation return a value resolved from route
  arguments, particularly to name ``locale``.
* ``translations`` - returns ``TranslationsManager`` (`wheezy.core`_ feature)
  for the current locale.
* ``translation`` - returns translations for the current handler. Default
  implementation return ``NullTranslations`` object. You application handler
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

See complete example in public demo application `config`_.

Model Binding
^^^^^^^^^^^^^

Once html form submitted you need a way to bind these values to some domain
model, validate, report errors, etc. This is where integartation with 
`wheezy.validation`_ package happens.












.. _`WSGI`: http://www.python.org/dev/peps/pep-3333
.. _`wheezy.core`: http://bitbucket.org/akorn/wheezy.core
.. _`wheezy.http`: http://packages.python.org/wheezy.http
.. _`wheezy.routing`: http://packages.python.org/wheezy.routing
.. _`wheezy.validation`: http://packages.python.org/wheezy.validation
.. _`i18n`: https://bitbucket.org/akorn/wheezy.web/src/tip/demos/public/i18n
.. _`config`: https://bitbucket.org/akorn/wheezy.web/src/tip/demos/public/src/config.py

