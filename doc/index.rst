.. _`wheezy.web`:

wheezy.web
==========

Introduction
------------

`wheezy.web`_ is a lightweight,
`high performance <http://mindref.blogspot.com/2012/09/python-fastest-web-framework.html>`_,
high concurrency `WSGI`_ web framework with the key features to
*build modern, efficient web*:

* Requires Python 2.4-2.7 or 3.2+.
* MVC architectural pattern (`push <http://en.wikipedia.org/wiki/Web_application_framework#Push-based_vs._pull-based>`_-based).
* Functionality includes `routing <https://github.com/akornatskyy/wheezy.routing>`_,
  `model update/validation <https://github.com/akornatskyy/wheezy.validation>`_,
  `authentication/authorization <https://github.com/akornatskyy/wheezy.security>`_,
  `content <https://wheezyhttp.readthedocs.io/en/latest/userguide.html#content-cache>`_
  `caching <https://github.com/akornatskyy/wheezy.caching>`_ with
  `dependency <https://wheezycaching.readthedocs.io/en/latest/userguide.html#cachedependency>`_,
  xsrf/resubmission protection, AJAX+JSON, i18n (gettext),
  middlewares, and more.
* Template engine agnostic (integration with
  `jinja2 <http://jinja.pocoo.org>`_,
  `mako <http://www.makotemplates.org>`_,
  `tenjin <http://www.kuwata-lab.com/tenjin/>`_ and
  `wheezy.template <https://github.com/akornatskyy/wheezy.template>`_)
  plus `html widgets <https://github.com/akornatskyy/wheezy.html>`_.

It is optimized for performance, well tested and documented.

Resources:

* `source code`_, `examples`_ and `issues`_ tracker are available
  on `github`_
* `documentation`_

Contents
--------

.. toctree::
   :maxdepth: 2

   gettingstarted
   examples
   tutorial
   userguide
   modules

.. _`github`: https://github.com/akornatskyy/wheezy.web
.. _`documentation`: http://packages.python.org/wheezy.web
.. _`examples`: https://github.com/akornatskyy/wheezy.web/tree/master/demos
.. _`issues`: https://github.com/akornatskyy/wheezy.web/issues
.. _`python`: https://www.python.org
.. _`source code`: https://github.com/akornatskyy/wheezy.web
.. _`WSGI`: http://www.python.org/dev/peps/pep-3333
