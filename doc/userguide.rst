
User Guide
==========

:ref:`wheezy.web` is a lightweight `WSGI`_ framework that aims take most
benefits out of standard python library and serves a sort of glue with other
libraries. It can be run from python 2.4 up to the most cutting edge python 3.
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
  integrates such features as: routing, i18n, model binding, template
  rendering, authentication, xsrf/resubmission protection.
* :py:class:`~wheezy.web.handlers.base.RedirectRouteHandler` - redirects to
  given route name.
* :py:class:`~wheezy.web.handlers.file.FileHandler` - serves static files out
  of some directory.
* :py:class:`~wheezy.web.handlers.template.TemplateHandler` - serves templates
  that don't require up front data processing.

MethodHandler
~~~~~~~~~~~~~

:ref:`wheezy.web` routes incoming web request to handler per url mapping
(it uses `wheezy.routing`_ for this purpose):

.. literalinclude:: ../demos/hello/hello.py
   :lines: 27-30

You subclass from :py:class:`~wheezy.web.handlers.method.MethodHandler` or
:py:class:`~wheezy.web.handlers.base.BaseHandler` and
define methods ``get()`` or ``post()`` that handle HTTP request methods ``GET``
or ``POST``.

.. literalinclude:: ../demos/hello/hello.py
   :lines: 13-18

This method must return an ``HTTPResponse`` object.

:py:class:`~wheezy.web.handlers.method.MethodHandler` has a number of useful
attributes:

* ``options`` - a dictionary of application configuration options.
* ``request`` - an instance of ``wheezy.http.HTTPRequest``.
* ``route_args`` - a dictionary of arguments matched in url routing.
* ``cookies`` - a list of cookies that extend ``HTTPResponse``.

Please note that this handler automatically responds with HTTP status code 405
(method not allowed) in case the requested HTTP method is not overridden in your
handler, e.g. there is incoming POST request but your handler does not
provide an implementation.

BaseHandler
~~~~~~~~~~~

:py:class:`~wheezy.web.handlers.base.BaseHandler` provides methods that
integrates such features as:

#. routing
#. AJAX
#. i18n
#. model binding
#. JSON
#. template rendering
#. authentication
#. authorization
#. xsrf/resubmission protection
#. context sharing

You need to inherit from this class and define get() and/or post() to be able
respond to HTTP requests. This class inherits from
:py:class:`~wheezy.web.handlers.method.MethodHandler`, so everything mentioned
for :py:class:`~wheezy.web.handlers.method.MethodHandler` applies to
:py:class:`~wheezy.web.handlers.base.BaseHandler` as well.

Routing
^^^^^^^

Routing feature is provided via integration with `wheezy.routing`_ package.
There are the following methods:

* ``path_for(name, **kwargs)`` - returns url path by route name. Any missing
  parameters are obtained from that current route.
* ``absolute_url_for(name, **kwargs)`` - returns absolute url for the given
  route name by combining current request with route information.
* ``redirect_for(name, **kwargs)`` - returns redirect found response (HTTP
  status code 302) by route name.
* ``see_other_for(name, **kwargs)`` - returns see other redirect response
  (HTTP status code 303) by route name.

All these methods support the following arguments:

* ``name`` - a name of the route.
* ``kwargs`` - extra arguments necessary for routing.

Please refer to `wheezy.routing`_ documentation for more information.

AJAX
^^^^

Both redirects ``redirect_for`` and ``see_other_for`` understands
AJAX requests and change HTTP status code to 207 while preserving HTTP
header ``Location``.

Browsers incorrectly handle redirect response to ajax request, so there is
used HTTP status code 207 that javascript is capable to receive and process
browser redirect. Here is an example for jQuery (see file `core.js`_)::

    $.ajax({
        // ...
        success: function(data, textStatus, jqXHR) {
            if (jqXHR.status == 207) {
                window.location.replace(
                    jqXHR.getResponseHeader('Location'));
            } else {
                // ...
            }
        }
    });

If AJAX response status code is 207, browser navigates to URL specified
in HTTP response header ``Location``.

Please refer to `wheezy.http`_ documentation for more information.

Internationalization
^^^^^^^^^^^^^^^^^^^^

Internationalization feature is provided via integration with `wheezy.core`_
package (module ``i18n``). There are the following attributes:

* ``locale`` - default implementation return a value resolved from route
  arguments, particularly to name ``locale``.
* ``translations`` - returns ``TranslationsManager`` (`wheezy.core`_ feature)
  for the current locale.
* ``translation`` - returns translations for the current handler. Default
  implementation return ``NullTranslations`` object. Your application handler
  must override this attribute to provide valid ``gettext`` translations.

Here is example from `template`_ demo application::

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

Once the html form is submitted, you need a way to bind these values to some domain
model, validate, report errors, etc. This is where integration with
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

Here is an example from the `template`_ demo application (see file
`membership/web/views.py`_)::

    class SignInHandler(BaseHandler):

        def get(self, credential=None):
            if self.principal:
                return self.redirect_for('default')
            credential = credential or Credential()
            return self.render_response('membership/signin.html',
                    self.widgets(credential=credential))

        def post(self):
            credential = Credential()
            if (not self.try_update_model(credential)
                or not self.validate(credential, credential_validator)):
                return self.get(credential)
            return self.redirect_for('default')

On POST this handler updates ``credential`` with values from the html form
submitted. In case ``try_update_model`` or ``valida`` fails. we re-display
the sign-in page with errors reported.

Here is an example from the `template`_ demo application that demonstrates
how to use the general error (see file `membership/web/views.py`_)::

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

JSON
^^^^

There is integration with `wheezy.http`_ package in JSON object encoding.

* :py:meth:`~wheezy.web.handlers.BaseHandler.json_response` - returns
  ``HTTPResponse`` with JSON content.

Here is an example::

    class SignInHandler(BaseHandler):
        ...
        def post(self):
            ...
            credential = Credential()
            if (not self.try_update_model(credential)
                    ...):
                if self.request.ajax:
                    return self.json_response({'errors': self.errors})
                return self.get(credential)
            ...
            return self.see_other_for('default')

In case of error in ajax requests, the handler returns JSON object with
any errors reported, otherwise it renders response the template. This way you
are able to serve both: browsers with javascript enabled or disabled.

See file `core.js`_ for an example of how errors are processed by browser.

Templates
^^^^^^^^^

:ref:`wheezy.web` is not tied to some specific template engine, instead
it provides you a convinient contract to add one you prefer (see file
`config.py`_). Template contract is any callable of the following form::

    def render_template(self, template_name, **kwargs):
        return string

There are the following attributes and methods:

* ``helpers`` - a dictionary of context objects to be passed to
  ``render_template`` implementation (you need to override this method
  in case you need more specific context information in template).

  * ``_`` - ``gettext`` translations support.
  * ``errors`` - a dictionary with errors reported during validation. Key
    corresponds to attribute validated and value to a list of errors.
  * ``handler`` - an instance of currently executing handler.
  * ``route_args``, ``absolute_url_for``, ``path_for`` - relates to
    routing related methods.
  * ``principal`` - an instance of ``wheezy.security.Principal`` for the
    authenticated request or ``None``.
  * ``resubmission`` - resubmission HTML form widget.
  * ``xsrf`` - XSRF protection HTML form widget.

* ``render_template(template_name, widgets=None, **kwargs)`` - renders
  template with name ``template_name`` and pass it context information
  in ``**kwargs``.
* ``render_response(template_name, widgets=None, **kwargs)`` - writes
  result of ``render_template`` into ``wheezy.http.HTTPResponse`` and
  return it.

``widgets`` argument in ``render_template`` and ``render_response`` is
used to explicitly wrap HTML widgets (see `wheezy.html`_ package).
Note, if you are using template engine that comes with widgets preprocessing
you do not need to explicitly initialize this argument.

Widgets
^^^^^^^

Widgets are coming from `wheezy.html`_ package (see *WidgetExtension* for
a template engine). Here is ``SignUpHandler`` from demo::

    class SignUpHandler(BaseHandler):

        ...

        @handler_cache(profile=none_cache_profile)
        def get(self, registration=None):
            # ...
            return self.render_response(
                'membership/signup.html',
                model=self.model,
                registration=registration,
                account=registration.account,
                credential=registration.credential,
                questions=questions,
                account_types=tuple((k, self.gettext(v))
                                    for k, v in account_types))

The benefit of using widgets is a syntax sugar in html template.
They are processed by template proprocessor and generate template
engine specific code.

Mako example::

    <p>
        ${account.email.label('Email:')}
        ${account.email.textbox(autocomplete='off')}
        ${account.email.error()}
    </p>

Wheezy Template example::

    <p>
        @account.account_type.label('Account Type:')
        @account.account_type.radio(choices=account_types)
        @account.account_type.error()
    </p>

Please note that `wheezy.html`_ package provides optimization of widgets
per template engine used. That optimization is provided through use of
template specific constructs. Preprocessor for Mako / Jinja2 /
Tenjin / Wheezy.Template templates translates widgets to template engine
specific operations offering optimal performance.

Read more about available widgets in `wheezy.html`_ package.

Authentication
^^^^^^^^^^^^^^

Authentication is a process of confirming the truth of security principal.
In a web application it usually relates to creating an encrypted cookie value,
which can not easily be compromised by attacker. This is where integration
with `wheezy.security`_ happens.

The process of creating authentication cookie is as simple as assiging
instance of ``wheezy.security.Principal`` to attribute ``principal``. Let's
demonstrate this by example::

    from wheezy.security import Principal

    class SignInHandler(BaseHandler):

        def post(self):
            ...
            self.principal = Principal(
                id=credential.username,
                alias=credential.username)
            ...

Once we confirmed user has entered valid username and password we create
an instance of ``Principal`` and assign it to ``principal`` attribute. In
``setprincipal`` implementation authentication cookie is created with a
dump of ``Principal`` object and it value is protected by
``wheezy.security.crypto.Ticket`` (read more in `wheezy.security`_).

Here are authentication configuration options (see file `config.py`_)::

    options = {}

    options.update({
            'ticket': Ticket(
                max_age=config.getint('crypto', 'ticket-max-age'),
                salt=config.get('crypto', 'ticket-salt'),
                cypher=aes128,
                digestmod=ripemd160 or sha256 or sha1,
                options={
                    'CRYPTO_ENCRYPTION_KEY': config.get('crypto', 'encryption-key'),
                    'CRYPTO_VALIDATION_KEY': config.get('crypto', 'validation-key')
                }),

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
            ...

Sign out is even simpler, just delete ``principal`` attribute::

    class SignOutHandler(BaseHandler):

        def get(self):
            del self.principal
            return self.redirect_for('default')

Authorization
^^^^^^^^^^^^^

Authorization specify access rights to resources and provide access control
in particular to your application.

You are able to request authorization by decorating your handler method with
:py:meth:`~wheezy.web.authorization.authorize`::

    from wheezy.web import authorize

    class MembersOnlyHandler(BaseHandler):

        @authorize
        def get(self, registration=None):
            return response

There is also a way to demand specific role::

    class BusinessOnlyHandler(BaseHandler):

        @authorize(roles=('business',))
        def get(self, registration=None):
            return response

In case there are multiple roles specified in
:py:meth:`~wheezy.web.authorization.authorize` decorator than first match
grant access. That means user is required to be at least in one role to pass
this guard.

:py:meth:`~wheezy.web.authorization.authorize` decorator may return HTTP
response with status code 401 (Unauthorized) or 403 (Forbidden).

It is recommended to use
:py:class:`~wheezy.web.middleware.errors.HTTPErrorMiddleware` to route HTTP
status codes to signin or forbidden handlers. Read more in
:ref:`httperrormiddleware` section.

@secure
~~~~~~~

Decorator :py:class:`~wheezy.web.authorization.secure` accepts only secure
requests (those that are communication via SSL) and if incoming
request is not secure, issue permanent redirect to HTTPS location::

    class MyHandler(BaseHandler):
        @secure
        def get(self):
            ...
            return response

The behavior can be controlled via ``enabled`` (in case it is
``False`` no checks performed, defaults to ``True``).


XSRF/Resubmission
^^^^^^^^^^^^^^^^^

Cross-site request forgery (CSRF or XSRF), also known as a one-click attack
is a type of malicious exploit of a website whereby unauthorized commands are
transmitted from a user that the website trusts. Logging out of sites and
avoiding their "remember me" features can mitigate CSRF risk.

Forms that can be accidentally, or maliciously submitted multiple times can
cause undesired behavior and/or result in your application. Resubmits can
happen for many reasons, mainly through page refresh, browser back button
and incident multiple button clicks.

Regardless a source of issue you need to be aware it happening.

:ref:`wheezy.web` has built-in XSRF and resubmission protection. Configuration
options let you customize name used::

    options = {}
    options.update({
            'XSRF_NAME': '_x',
            'RESUBMISSION_NAME': '_c'
    })

You need include XSRF and/or resubmission widget into your form. Each template
has context functions ``xsrf()`` and ``resubmission()`` for this purpose::

    <form method="post">
        @xsrf()
        ...
    </form>

Validation happens in handler, here is how it implemented in
`membership/web/views.py`_::

    class SignInHandler(BaseHandler):

        def post(self):
            if not self.validate_xsrf_token():
                return self.redirect_for(self.route_args.route_name)
            ...

If XSRF token is invalid we redisplay the same page. Or we can show user an
error message, here is use case for resubmission check::

    class SignUpHandler(BaseHandler):

        def post(self):
            if not self.validate_resubmission():
                self.error('Your registration request has been queued. '
                        'Please wait while your request will be processed. '
                        'If your request fails please try again.')
                return self.get()
            ...

Since there is no simple rule of thumb when to use which protection and how
to react in case it happening, it still strongly recommended take into account
such situations during application development and provide unified application
wide behavior.

Context
^^^^^^^

:py:class:`~wheezy.web.handlers.base.BaseHandler` holds a number of useful
features that other application layers (e.g. service layer, business logic)
can benefit from.

There ``context`` attribute is available for this purpose. It is
a dictionary that extends ``options`` with the following information: errors,
locale, principal and translations.

Here is example from the `template`_ demo application (see
`membership/web/views.py`_)::

    class SignInHandler(BaseHandler):

        @attribute
        def factory(self):
            return Factory(self.context)

Context is passed to service factory.

Redirect Handler
~~~~~~~~~~~~~~~~

:py:class:`~wheezy.web.handlers.base.RedirectRouteHandler` redirects to a given
route name (HTTP status code 302). You can use
:py:meth:`~wheezy.web.handlers.base.redirect_handler` in url mapping
declaration::

    all_urls = [
        url('', redirect_handler('welcome'), name='default'),
        ...
    ]

The example above always performs a redirect match for route `default` to route
`welcome`. It asks browser to redirect it request to another page.

Permanent Redirect
~~~~~~~~~~~~~~~~~~

:py:class:`~wheezy.web.handlers.base.PermanentRedirectRouteHandler`
performs a permanent redirect (HTTP status code 301) to the given route name.
You can use
:py:meth:`~wheezy.web.handlers.base.permanent_redirect_handler` in the url
mapping declaration::

    all_urls = [
        url('', permanent_redirect_handler('welcome'), name='default'),
        ...
    ]

The example above results in a permanent redirect for route `default` to route
`welcome`.

FileHandler
~~~~~~~~~~~

:py:class:`~wheezy.web.handlers.file.FileHandler` serves static files out
of some directory. You can use
:py:meth:`~wheezy.web.handlers.file.file_handler` in url mapping
declaration::

    all_urls = [
        url('static/{path:any}', file_handler(
                root='content/static/',
                age=timedelta(hours=1)), name='static'),
        ...
    ]

:py:meth:`~wheezy.web.handlers.file.file_handler` accepts the following
arguments:

* ``root`` - a root path of directory that holds static files, e.g.
  `.css`, `.js`, `.jpg`, etc. It is recommended that this directory be
  isolated from any other part of the application.
* ``age`` - controls http browser cache policy period.

Request Headers
^^^^^^^^^^^^^^^

:py:class:`~wheezy.web.handlers.file.FileHandler` handles both GET and HEAD
browser requests, provides `Last-Modified` and `ETag` HTTP response headers,
as well as understands `If-Modified-Since` and `If-None-Match` request headers,
as sent by browser for static content.

GZip and Caching
^^^^^^^^^^^^^^^^

It is recommended to use :py:meth:`~wheezy.web.handlers.file.file_handler`
together with ``gzip_transform`` and ``response_cache`` (requries HTTP cache
middleware).

Here is example from `template`_ demo application::

    from wheezy.http import response_cache
    from wheezy.http.transforms import gzip_transform
    from wheezy.http.transforms import response_transforms
    from wheezy.web.handlers import file_handler


    static_files = response_cache(static_cache_profile)(
        response_transforms(gzip_transform(compress_level=6))(
            file_handler(
                root='content/static/',
                age=timedelta(hours=1))))

    all_urls = [
        url('static/{path:any}', static_files, name='static'),
        ...
    ]

Templates
^^^^^^^^^

Path for static files is provided by standard `wheezy.routing`_
``path_for(name, **kwargs)`` function::

    path_for('static', path='core.js')

TemplateHandler
~~~~~~~~~~~~~~~

:py:class:`~wheezy.web.handlers.template.TemplateHandler` serves templates
that do not require up front data processing. This mostly relates to some
static pages, e.g. about, help, error, etc.

You can use
:py:meth:`~wheezy.web.handlers.template.template_handler` in the url mapping
declaration::

    from wheezy.web.handlers import template_handler

    public_urls = [
        url('about', template_handler('public/about.html'), name='about'),
    ]

:py:meth:`~wheezy.web.handlers.template.template_handler` supports the
following arguments:

* ``template_name`` - template name used to render response.
* ``status_code`` - HTTP status code to set in response. Defaults to 200.

Middleware
----------

:ref:`wheezy.web` extends middleware provided by `wheezy.http`_ by adding
the following:

* bootstrap defaults
* path routing middleware
* http error middleware

Bootstrap Defaults
~~~~~~~~~~~~~~~~~~
:py:meth:`~wheezy.web.middleware.bootstrap_defaults` middleware factory does
not provide any middleware, instead it is used to check application options
and provide defaults.

The following options are checked:

* ``path_router`` - if it is not defined already an instance of
  ``wheezy.routing.PathRouter`` is created. Argument ``url_mapping`` is
  passed to ``PathRouter.add_routes`` method.
* ``render_template`` - defaults to an instance of
  ``wheezy.web.templates.MakoTemplate``.
* ``translations_manager`` - defaults to an instance of
  ``wheezy.core.i18n.TranslationsManager``.
* ``ticket`` - defaults to an instance of ``wheezy.security.crypto.Ticket``.

PathRoutingMiddleware
~~~~~~~~~~~~~~~~~~~~~

:py:class:`~wheezy.web.middleware.routing.PathRoutingMiddleware` provides
integration with `wheezy.routing`_ package. It is added to
``WSGIApplication`` via
:py:meth:`~wheezy.web.middleware.path_routing_middleware_factory`.

.. literalinclude:: ../demos/hello/hello.py
   :lines: 33-38

This factory requires `path_router` to be available in application options.

.. _httperrormiddleware:

HTTPErrorMiddleware
~~~~~~~~~~~~~~~~~~~

:py:class:`~wheezy.web.middleware.errors.HTTPErrorMiddleware` provides a
custom error page in case http status code is above 400 (HTTP status codes
from 400 and up relates to client error, 500 and up - server error). This
middleware is initialized with ``error_mapping`` dictionary, where key
corresponds to HTTP status code and value to route name. In case of a status
code match it redirects incoming request to route per ``error_mapping``.

:py:class:`~wheezy.web.middleware.errors.HTTPErrorMiddleware` can be added to
``WSGIApplication`` via
:py:meth:`~wheezy.web.middleware.http_error_middleware_factory`::

        main = WSGIApplication(
            middleware=[
                bootstrap_defaults(url_mapping=all_urls),
                http_cache_middleware_factory,
                http_error_middleware_factory,
                path_routing_middleware_factory
            ],
            options=options)

The following configuration options available::

    from wheezy.core.collections import defaultdict

    options = {}
    options['http_errors'] = defaultdict(lambda: 'http500', {
                # HTTP status code: route name
                400: 'http400',
                401: 'signin',
                403: 'http403',
                404: 'http404',
                500: 'http500',
            }),
    })

``defaultdict`` is used to provide default route name if there is no match in
``http_errors`` dictionary. All routes defined in ``http_errors`` must exist.
These checks occur in
:py:meth:`~wheezy.web.middleware.http_error_middleware_factory`.

Transforms
----------

Transforms are a way to manipulate handler response accordingly to some
algorithm. :ref:`wheezy.web` provides decorator
:py:meth:`~wheezy.web.transforms.handler_transforms` to adapt transforms
available in `wheezy.http`_ to web handlers sub-classed from
:py:class:`~wheezy.web.handlers.base.BaseHandler`::

    from wheezy.http.transforms import gzip_transform
    from wheezy.web.handlers import BaseHandler
    from wheezy.web.transforms import handler_transforms

    class MyHandler(BaseHandler):

        @handler_transforms(gzip_transform(compress_level=9))
        def get(self):
            return response

Please refer to `wheezy.http`_ documentation for more information.

Templates
---------

:ref:`wheezy.web` does not provide its own implementation for template rendering
instead it offers integration with the following packages:

* `Jinja2`_ Templates
* `Mako`_ Templates
* `Tenjin`_ Templates
* `Wheezy.Template`_

Contract
~~~~~~~~

Template contract is any callable of the following form::

    def render_template(self, template_name, **kwargs):
        return 'unicode string'

Jinja2 Templates
~~~~~~~~~~~~~~~~

Here is the configuration option to define that Jinja2 templates are rendered within
the application (see `config.py`_ for details)::

    from jinja2 import Environment
    from jinja2 import FileSystemLoader
    from wheezy.html.ext.jinja2 import WidgetExtension
    from wheezy.html.ext.jinja2 import WhitespaceExtension
    from wheezy.html.utils import format_value
    from wheezy.web.templates import Jinja2Template

    env = Environment(
        loader=FileSystemLoader('content/templates'),
        auto_reload=False,
        extensions=[
            WidgetExtension,
            WhitespaceExtension
        ])
    env.globals.update({
        'format_value': format_value,
    })
    render_template = Jinja2Template(env)

The arguments passed to ``Environment`` are specific to Jinja2 templates and
not explained here. Please refer to `Jinja2`_ documentation.

Mako Templates
~~~~~~~~~~~~~~

Here is the configuration option to define that Mako templates are rendered within
application (see `config.py`_ for details)::

    from wheezy.html.ext.mako import whitespace_preprocessor
    from wheezy.html.ext.mako import widget_preprocessor
    from wheezy.web.templates import MakoTemplate


    render_template = MakoTemplate(
            module_directory='/tmp/mako_modules',
            filesystem_checks=False,
            directories=['content/templates'],
            cache_factory=cache_factory,
            preprocessor=[
                widget_preprocessor,
                whitespace_preprocessor,
            ])

The arguments passed to ``MakoTemplate`` are specific to Mako templates and
not explained here. Please refer to `Mako`_ documentation.

Tenjin Templates
~~~~~~~~~~~~~~~~

Here is configuration option to define that Tenjin templates are rendered within
application (see `config.py`_ for details)::

    from wheezy.html.ext.tenjin import whitespace_preprocessor
    from wheezy.html.ext.tenjin import widget_preprocessor
    from wheezy.html.utils import format_value
    from wheezy.web.templates import TenjinTemplate

    render_template = TenjinTemplate(
            path=['content/templates'],
            pp=[
                widget_preprocessor,
                whitespace_preprocessor,
            ],
            helpers={
                'format_value': format_value
            })

The arguments passed to ``TenjinTemplate`` are specific to Tenjin templates
and not explained here. Please refer to `Tenjin`_ documentation.

Wheezy Template
~~~~~~~~~~~~~~~

Here is configuration option to define that Wheezy.Template templates are rendered within
application (see `config.py`_ for details)::

    from wheezy.html.ext.template import WhitespaceExtension
    from wheezy.html.ext.template import WidgetExtension
    from wheezy.html.utils import format_value
    from wheezy.html.utils import html_escape
    from wheezy.template.engine import Engine
    from wheezy.template.ext.core import CoreExtension
    from wheezy.template.loader import FileLoader
    from wheezy.web.templates import WheezyTemplate

    searchpath = ['content/templates-wheezy']
    engine = Engine(
            loader=FileLoader(searchpath),
            extensions=[
                CoreExtension(),
                WidgetExtension(),
                WhitespaceExtension()
            ])
    engine.global_vars.update({
        'format_value': format_value,
        'h': html_escape,
    })
    render_template = WheezyTemplate(engine)

The arguments passed to ``Engine`` are specific to `Wheezy.Template`_
and not explained here. Please refer to `Wheezy.Template`_ documentation.

Caching
-------

:ref:`wheezy.web` provides decorator
:py:meth:`~wheezy.web.caching.handler_cache` to adapt cache interface
available in `wheezy.http`_ to web handlers sub-classed from
:py:class:`~wheezy.web.handlers.base.BaseHandler`::

    from wheezy.http import CacheProfile
    from wheezy.web.handlers import BaseHandler
    from wheezy.web.caching import handler_cache

    none_cache_profile = CacheProfile(
            'none',
            no_store=True,
            enabled=True)

    class MyHandler(BaseHandler):

        @handler_cache(profile=none_cache_profile)
        def get(self, credential=None):
            return response

Please refer to `wheezy.http`_ documentation for more information. All features
available in `wheezy.http`_ caching are applicable.

Content caching plus cache dependency is the most advanced boost of your
application performance. Regardless of template engine this can give up to
8-10 times better performance.

.. _`config.py`: https://bitbucket.org/akorn/wheezy.web/src/tip/demos/template/src/config.py
.. _`core.js`: https://bitbucket.org/akorn/wheezy.web/src/tip/demos/template/content/static/js/core.js
.. _`i18n`: https://bitbucket.org/akorn/wheezy.web/src/tip/demos/template/i18n
.. _`jinja2`: http://jinja.pocoo.org
.. _`mako`: http://docs.makotemplates.org
.. _`membership/web/views.py`: https://bitbucket.org/akorn/wheezy.web/src/tip/demos/template/src/membership/web/views.py
.. _`template`: https://bitbucket.org/akorn/wheezy.web/src/tip/demos/template
.. _`tenjin`: http://www.kuwata-lab.com/tenjin
.. _`wheezy.core`: http://bitbucket.org/akorn/wheezy.core
.. _`wheezy.html`: http://packages.python.org/wheezy.html
.. _`wheezy.http`: http://packages.python.org/wheezy.http
.. _`wheezy.routing`: http://packages.python.org/wheezy.routing
.. _`wheezy.security`: http://packages.python.org/wheezy.security
.. _`wheezy.template`: http://pypi.python.org/pypi/wheezy.template
.. _`wheezy.validation`: http://packages.python.org/wheezy.validation
.. _`WSGI`: http://www.python.org/dev/peps/pep-3333
