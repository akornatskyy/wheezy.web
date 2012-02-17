
Examples
========

We start with a simple example. Before we proceed 
let setup `virtualenv`_ environment::

    $ virtualenv env
    $ env/bin/easy_install wheezy.web

.. _helloworld:

Hello World
-----------

`hello.py`_ shows you how to use :ref:`wheezy.web` in a pretty simple `WSGI`_
application. It no way pretend to be shortest possible and absolutely not 
magical:

.. literalinclude:: ../demos/hello/hello.py
   :lines: 1-

Handler Contract
~~~~~~~~~~~~~~~~

Let have a look through each line in this application. First of all let take
a look what is a handler:

.. literalinclude:: ../demos/hello/hello.py
   :lines: 21-24
   
This one is not changed from what you had in `wheezy.http`_ so you are good
to keep it minimal. However there is added another one (that actually 
implements the same handler contract internally):

.. literalinclude:: ../demos/hello/hello.py
   :lines: 13-18

What is ``get`` method here? It is your response to HTTP GET request. You have
post for HTTP POST, etc.

Routing
~~~~~~~

Routing is inherited from `wheezy.routing`_. Note that both handlers are 
working well together:

.. literalinclude:: ../demos/hello/hello.py
   :lines: 27-30
   
Application
~~~~~~~~~~~

``WSGIApplication`` is coming from `wheezy.http`_. Integration with 
`wheezy.routing`_ is provided as middleware factory
(:py:meth:`~wheezy.web.middleware.path_routing_middleware_factory`):

.. literalinclude:: ../demos/hello/hello.py
   :lines: 33-40

.. _public_demo:

Public
------

`Public`_ application serves template purpose for you. If you are about to start a
new project it is a good starting point.

.. _`virtualenv`: http://pypi.python.org/pypi/virtualenv
.. _`hello.py`: https://bitbucket.org/akorn/wheezy.web/src/tip/demos/hello/hello.py
.. _`public`: https://bitbucket.org/akorn/wheezy.web/src/tip/demos/public
.. _`WSGI`: http://www.python.org/dev/peps/pep-3333
.. _`wheezy.http`: http://packages.python.org/wheezy.http
.. _`wheezy.routing`: http://packages.python.org/wheezy.routing
