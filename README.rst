`wheezy.web`_ is a lightweight,
`high performance <http://mindref.blogspot.com/2012/09/python-fastest-web-framework.html>`_,
high concurrency `WSGI`_ web framework with the key features to
*build modern, efficient web*:

* Requires Python 2.4-2.7 or 3.2+.
* MVC architectural pattern (`push <http://en.wikipedia.org/wiki/Web_application_framework#Push-based_vs._pull-based>`_-based).
* Functionality includes `routing <http://bitbucket.org/akorn/wheezy.routing>`_,
  `model update/validation <http://bitbucket.org/akorn/wheezy.validation>`_,
  `authentication/authorization <http://bitbucket.org/akorn/wheezy.security>`_,
  `content <http://packages.python.org/wheezy.http/userguide.html#content-cache>`_
  `caching <http://bitbucket.org/akorn/wheezy.caching>`_ with
  `dependency <http://packages.python.org/wheezy.caching/userguide.html#cachedependency>`_,
  xsrf/resubmission protection, AJAX+JSON, i18n (gettext),
  middlewares, and more.
* Template engine agnostic (integration with
  `jinja2 <http://jinja.pocoo.org>`_,
  `mako <http://www.makotemplates.org>`_,
  `tenjin <http://www.kuwata-lab.com/tenjin/>`_ and
  `wheezy.template <http://bitbucket.org/akorn/wheezy.template/>`_)
  plus `html widgets <http://bitbucket.org/akorn/wheezy.html>`_.

It is optimized for performance, well tested and documented.

Resources:

* `source code`_, `examples`_ (`live`_) and `issues`_ tracker are available
  on `bitbucket`_
* `documentation`_, `readthedocs`_
* `eggs`_ on `pypi`_

Install
-------

`wheezy.web`_ requires `python`_ version 2.4 to 2.7 or 3.2+.
It is independent of operating system. You can install it from `pypi`_
site using `setuptools`_::

    $ easy_install wheezy.web

If you are using `virtualenv`_::

    $ virtualenv env
    $ env/bin/easy_install wheezy.web

If you run into any issue or have comments, go ahead and add on
`bitbucket`_.

.. _`WSGI`: http://www.python.org/dev/peps/pep-3333
.. _`bitbucket`: http://bitbucket.org/akorn/wheezy.web
.. _`documentation`: http://packages.python.org/wheezy.web
.. _`eggs`: http://pypi.python.org/pypi/wheezy.web
.. _`examples`: http://bitbucket.org/akorn/wheezy.web/src/tip/demos
.. _`issues`: http://bitbucket.org/akorn/wheezy.web/issues
.. _`live`: http://wheezy.pythonanywhere.com
.. _`pypi`: http://pypi.python.org
.. _`python`: http://www.python.org
.. _`readthedocs`: http://readthedocs.org/builds/wheezyweb
.. _`setuptools`: http://pypi.python.org/pypi/setuptools
.. _`source code`: http://bitbucket.org/akorn/wheezy.web/src
.. _`virtualenv`: http://pypi.python.org/pypi/virtualenv
.. _`wheezy.web`: http://pypi.python.org/pypi/wheezy.web
