
Getting Started
===============

Install
-------

:ref:`wheezy.web` requires `python`_ version 2.4 to 2.7 or 3.2+.
It is independent of operating system. You can install it from `pypi`_
site using `setuptools`_::

    $ easy_install wheezy.web

If you are using `virtualenv`_::

    $ virtualenv env
    $ env/bin/easy_install wheezy.web

Since :ref:`wheezy.web` is template engine agnostic, you need specify
extra requirements (per template engine of your choice)::

    $ env/bin/easy_install wheezy.web[jinja2]
    $ env/bin/easy_install wheezy.web[mako]
    $ env/bin/easy_install wheezy.web[tenjin]
    $ env/bin/easy_install wheezy.web[wheezy.template]

Develop
-------

You can get the `source code`_ using `mercurial`_::

    $ hg clone http://bitbucket.org/akorn/wheezy.web
    $ cd wheezy.web

Prepare `virtualenv`_ environment in *env* directory ::

    $ make env

... and run all tests::

    $ make test

You can read how to compile from source code different versions of
`python`_ in the `article`_ published on `mind reference`_ blog.

You can run certain make targets with specific python version. Here
we are going to run `doctest`_ with python3.2::

    $ make env doctest-cover VERSION=3.2

Generate documentation with `sphinx`_::

	$ make doc

If you run into any issue or have comments, go ahead and add on
`bitbucket`_.

.. _`article`: http://mindref.blogspot.com/2011/09/compile-python-from-source.html
.. _`bitbucket`: http://bitbucket.org/akorn/wheezy.web/issues
.. _`doctest`: http://docs.python.org/library/doctest.html
.. _`mercurial`: http://mercurial.selenic.com/
.. _`mind reference`: http://mindref.blogspot.com/
.. _`pypi`: http://pypi.python.org/pypi/wheezy.web
.. _`python`: http://www.python.org
.. _`setuptools`: http://pypi.python.org/pypi/setuptools
.. _`source code`: http://bitbucket.org/akorn/wheezy.web/src
.. _`sphinx`: http://sphinx.pocoo.org/
.. _`virtualenv`: http://pypi.python.org/pypi/virtualenv

