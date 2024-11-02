# wheezy.web

[![tests](https://github.com/akornatskyy/wheezy.web/actions/workflows/tests.yml/badge.svg)](https://github.com/akornatskyy/wheezy.web/actions/workflows/tests.yml)
[![Coverage Status](https://coveralls.io/repos/github/akornatskyy/wheezy.web/badge.svg?branch=master)](https://coveralls.io/github/akornatskyy/wheezy.web?branch=master)
[![Documentation Status](https://readthedocs.org/projects/wheezyweb/badge/?version=latest)](https://wheezyweb.readthedocs.io/en/latest/?badge=latest)
[![pypi version](https://badge.fury.io/py/wheezy.web.svg)](https://badge.fury.io/py/wheezy.web)

[wheezy.web](https://pypi.org/project/wheezy.web/) is a lightweight,
[high performance](https://mindref.blogspot.com/2012/09/python-fastest-web-framework.html),
high concurrency [WSGI](http://www.python.org/dev/peps/pep-3333) web
framework with the key features to *build modern, efficient web*:

- Requires Python 3.8+.
- MVC architectural pattern
  ([push](http://en.wikipedia.org/wiki/Web_application_framework#Push-based_vs._pull-based)-based).
- Functionality includes
  [routing](https://github.com/akornatskyy/wheezy.routing),
  [model update/validation](https://github.com/akornatskyy/wheezy.validation),
  [authentication/authorization](https://github.com/akornatskyy/wheezy.security),
  [content](https://wheezyhttp.readthedocs.io/en/latest/userguide.html#content-cache)
  [caching](https://github.com/akornatskyy/wheezy.caching) with
  [dependency](https://wheezycaching.readthedocs.io/en/latest/userguide.html#cachedependency),
  xsrf/resubmission protection, AJAX+JSON, i18n (gettext),
  middlewares, and more.
- Template engine agnostic (integration with
  [jinja2](http://jinja.pocoo.org),
  [mako](http://www.makotemplates.org),
  [tenjin](http://www.kuwata-lab.com/tenjin/) and
  [wheezy.template](https://github.com/akornatskyy/wheezy.template)) plus
  [html widgets](https://github.com/akornatskyy/wheezy.html).

It is optimized for performance, well tested and documented.

Resources:

- [source code](https://github.com/akornatskyy/wheezy.web),
  [examples](https://github.com/akornatskyy/wheezy.web/tree/master/demos)
  ([live](http://wheezy.pythonanywhere.com)) and
  [issues](https://github.com/akornatskyy/wheezy.web/issues)
  tracker are available on
  [github](https://github.com/akornatskyy/wheezy.web)
- [documentation](https://wheezyweb.readthedocs.io/en/latest/)

## Install

[wheezy.web](https://pypi.org/project/wheezy.web/) requires
[python](https://www.python.org) version 3.9+. It is independent of operating
system. You can install it from [pypi](https://pypi.org/project/wheezy.web/)
site:

```sh
pip install -U wheezy.web
```

If you run into any issue or have comments, go ahead and add on
[github](https://github.com/akornatskyy/wheezy.web).
