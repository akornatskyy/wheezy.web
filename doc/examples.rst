
Examples
========

We start with a simple example. Before we proceed
let setup `virtualenv`_ environment::

    $ virtualenv env

Since :ref:`wheezy.web` is template engine agnostic, you need specify
extra requirements (per template engine of your choice)::

    $ env/bin/easy_install wheezy.web[jinja2]
    $ env/bin/easy_install wheezy.web[mako]
    $ env/bin/easy_install wheezy.web[tenjin]

Templates
---------

`Template`_ application serves template purpose for you. It includes:

* Integration with both mako and tenjin template system.
* User registration and authentication.
* Form validation.

If you are about to start a new project it is a good starting point.

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

Functional Tests
~~~~~~~~~~~~~~~~

You can easily write functional tests for your application using ``WSGIClient``
from `wheezy.http`_ (file `test_hello.py`_).

.. literalinclude:: ../demos/hello/test_hello.py
   :lines: 5-

For more advanced use cases refer to `wheezy.http`_ documentation, please.

Benchmark
~~~~~~~~~

You can add benchmark of your functional tests (file `benchmark_hello.py`_):

.. literalinclude:: ../demos/hello/benchmark_hello.py
   :lines: 5-

Let run benchmark tests with ``nose`` (to be run from ``demos/hello``
directory)::

    $ ../../env/bin/nosetests-2.7 -qs -m benchmark benchmark_hello.py

Here is output::

    hello: 2 x 20000
    baseline throughput change target
      100.0%   11518rps  +0.0% test_welcome
       91.0%   10476rps  +1.1% test_home
    ----------------------------------------------------------------------
    Ran 1 test in 3.686s


.. _`virtualenv`: http://pypi.python.org/pypi/virtualenv
.. _`hello.py`: https://bitbucket.org/akorn/wheezy.web/src/tip/demos/hello/hello.py
.. _`test_hello.py`: https://bitbucket.org/akorn/wheezy.web/src/tip/demos/hello/test_hello.py
.. _`benchmark_hello.py`: https://bitbucket.org/akorn/wheezy.web/src/tip/demos/hello/benchmark_hello.py
.. _`template`: https://bitbucket.org/akorn/wheezy.web/src/tip/demos/template
.. _`WSGI`: http://www.python.org/dev/peps/pep-3333
.. _`wheezy.http`: http://packages.python.org/wheezy.http
.. _`wheezy.routing`: http://packages.python.org/wheezy.routing

