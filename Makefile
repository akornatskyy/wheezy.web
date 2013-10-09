.SILENT: debian env clean release upload qa test doctest-cover nose-cover test-cover doc env-demos test-demos
.PHONY: debian env clean release upload qa test doctest-cover nose-cover test-cover doc env-demos test-demos

VERSION=2.7
PYPI=http://pypi.python.org/simple
ENV=env
DIST_DIR=dist

PYTHON=$(ENV)/bin/python$(VERSION)
EASY_INSTALL=$(ENV)/bin/easy_install-$(VERSION)
PYTEST=$(ENV)/bin/py.test-$(VERSION)
NOSE=$(ENV)/bin/nosetests-$(VERSION)
SPHINX=/usr/bin/python /usr/bin/sphinx-build


all: clean doctest-cover test env-demos test-demos release

debian:
	apt-get -y update
	apt-get -y dist-upgrade
	# How to Compile Python from Source
	# http://mindref.blogspot.com/2011/09/compile-python-from-source.html
	apt-get -y install libbz2-dev build-essential python \
		python-dev python-setuptools python-virtualenv \
		python-sphinx mercurial

env:
	PYTHON_EXE=/usr/local/bin/python$(VERSION) ; \
    if [ ! -x $$PYTHON_EXE ]; then \
		PYTHON_EXE=/opt/local/bin/python$(VERSION) ; \
    	if [ ! -x $$PYTHON_EXE ]; then \
    		PYTHON_EXE=/usr/bin/python$(VERSION) ; \
    	fi ; \
    fi ; \
    VIRTUALENV_USE_SETUPTOOLS=1; \
    export VIRTUALENV_USE_SETUPTOOLS; \
    virtualenv --python=$$PYTHON_EXE $(ENV)
	if [ "$$(echo $(VERSION) | sed 's/\.//')" -ge 30 ]; then \
		echo -n 'Upgrading distribute...'; \
		$(EASY_INSTALL) -i $(PYPI) -U -O2 distribute \
			> /dev/null 2>/dev/null; \
		echo 'done.'; \
	fi
	$(EASY_INSTALL) -i $(PYPI) -O2 coverage nose pytest \
		pytest-pep8 pytest-cov mock mako tenjin jinja2 \
		wheezy.template
	# The following packages available for python == 2.4
	if [ "$$(echo $(VERSION) | sed 's/\.//')" -eq 24 ]; then \
		$(EASY_INSTALL) -i $(PYPI) -O2 wsgiref; \
	fi
	$(PYTHON) setup.py develop -i $(PYPI)

clean:
	find src/ demos/ -type d -name __pycache__ | xargs rm -rf
	find demos/*/i18n/ -name '*.mo' -delete
	find src/ demos/ -name '*.py[co]' -delete
	rm -rf dist/ build/ MANIFEST src/*.egg-info .cache .coverage \
		build/ dist/

release:
	$(PYTHON) setup.py -q bdist_egg

upload:
	REV=$$(hg head --template '{rev}') ; \
	sed -i "s/'0.1'/'0.1.$$REV'/" src/wheezy/web/__init__.py ; \
	if [ "$$(echo $(VERSION) | sed 's/\.//')" -eq 27 ]; then \
		$(PYTHON) setup.py -q egg_info --tag-build .$$REV \
			sdist register upload; \
		$(EASY_INSTALL) -i $(PYPI) sphinx; \
		$(PYTHON) env/bin/sphinx-build -D release=0.1.$$REV \
			-a -b html doc/ doc/_build/;\
		python setup.py upload_docs; \
	fi; \
	$(PYTHON) setup.py -q egg_info --tag-build .$$REV \
		bdist_egg --dist-dir=$(DIST_DIR) \
		rotate --match=$(VERSION).egg --keep=1 --dist-dir=$(DIST_DIR) \
		upload;

qa:
	if [ "$$(echo $(VERSION) | sed 's/\.//')" -eq 27 ]; then \
		flake8 --max-complexity 10 demos doc src setup.py && \
		pep8 demos doc src setup.py ; \
	fi

test:
	$(PYTEST) -q -x --pep8 --doctest-modules \
		src/wheezy/web

doctest-cover:
	$(NOSE) --stop --with-doctest --detailed-errors \
		--with-coverage --cover-package=wheezy.web

nose-cover:
	$(NOSE) --stop --with-doctest --detailed-errors --with-coverage \
		--cover-package=wheezy.web

test-cover:
	$(PYTEST) -q --cov wheezy.web --cov wheezy.web.handlers \
		--cov wheezy.web.middleware --cov-report term-missing \
		src/wheezy/web/handlers/tests src/wheezy/web/middleware/tests \
		src/wheezy/web/tests

doc:
	$(SPHINX) -a -b html doc/ doc/_build/

env-demos:
	make env -sC demos/quickstart-empty PYPI=$(PYPI) VERSION=$(VERSION)
	make env -sC demos/quickstart-i18n PYPI=$(PYPI) VERSION=$(VERSION)
	make env -sC demos/template PYPI=$(PYPI) VERSION=$(VERSION)

test-demos:
	$(PYTEST) -q -x --pep8 demos/hello
	make clean nose-cover -sC demos/quickstart-empty VERSION=$(VERSION)
	make clean po nose-cover -sC demos/quickstart-i18n VERSION=$(VERSION)
	make clean po -sC demos/template VERSION=$(VERSION)
	make test -sC demos/template TEMPLATE_ENGINE=jinja2 VERSION=$(VERSION)
	make test -sC demos/template TEMPLATE_ENGINE=mako VERSION=$(VERSION)
	make test -sC demos/template TEMPLATE_ENGINE=tenjin VERSION=$(VERSION)
	make test -sC demos/template TEMPLATE_ENGINE=wheezy.template VERSION=$(VERSION)
	make test -sC demos/template TEMPLATE_ENGINE=wheezy.preprocessor VERSION=$(VERSION)
