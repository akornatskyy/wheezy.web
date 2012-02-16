.SILENT: clean env doctest-cover test doc release
.PHONY: clean env doctest-cover test doc release

VERSION=2.7
PYPI=http://pypi.python.org/simple

PYTHON=env/bin/python$(VERSION)
EASY_INSTALL=env/bin/easy_install-$(VERSION)
PYTEST=env/bin/py.test-$(VERSION)
NOSE=env/bin/nosetests-$(VERSION)
SPHINX=/usr/bin/python /usr/bin/sphinx-build

all: clean doctest-cover test test-demos release

debian:
	apt-get -y update
	apt-get -y dist-upgrade
	# How to Compile Python from Source
	# http://mindref.blogspot.com/2011/09/compile-python-from-source.html
	apt-get -y install libbz2-dev build-essential python \
		python-dev python-setuptools python-virtualenv \
		python-sphinx mercurial

env:
	PYTHON_EXE=/usr/local/bin/python$(VERSION); \
	if [ ! -x $$PYTHON_EXE ]; then \
		PYTHON_EXE=/usr/bin/python$(VERSION); \
	fi;\
    VIRTUALENV_USE_SETUPTOOLS=1; \
    export VIRTUALENV_USE_SETUPTOOLS; \
	virtualenv --python=$$PYTHON_EXE \
		--no-site-packages env
	if [ "$$(echo $(VERSION) | sed 's/\.//')" -ge 30 ]; then \
		echo -n 'Upgrading distribute...'; \
		$(EASY_INSTALL) -i $(PYPI) -U -O2 distribute \
			> /dev/null 2>/dev/null; \
		echo 'done.'; \
	fi
	$(EASY_INSTALL) -i $(PYPI) -O2 coverage nose pytest \
		pytest-pep8 pytest-cov wsgiref
	# The following packages available for python < 3.0
	#if [ "$$(echo $(VERSION) | sed 's/\.//')" -lt 30 ]; then \
	#	$(EASY_INSTALL) sphinx; \
	#fi
	$(PYTHON) setup.py develop -i $(PYPI)

clean:
	find src/ demos/ -type d -name __pycache__ | xargs rm -rf
	find src/ demos/ -name '*.py[co]' -delete
	rm -rf dist/ build/ MANIFEST src/*.egg-info

release:
	$(PYTHON) setup.py -q bdist_egg

test:
	$(PYTEST) -q -x --pep8 --doctest-modules \
		src/wheezy/web

doctest-cover:
	$(NOSE) --stop --with-doctest --detailed-errors \
		--with-coverage --cover-package=wheezy.web

test-cover:
	$(PYTEST) -q --cov wheezy.web \
		--cov-report term-missing \
		src/wheezy/web/tests

doc:
	$(SPHINX) -a -b html doc/ doc/_build/

test-demos:
	$(PYTEST) -q -x --pep8 demos/hello
	make clean test -sC demos/public VERSION=$(VERSION)
