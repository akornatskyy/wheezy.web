.SILENT: clean env nose-cover test-cover qa test doc release upload
.PHONY: clean env nose-cover test-cover qa test doc release upload

VERSION=2.7
PYPI=http://pypi.python.org/simple
DIST_DIR=dist

PYTHON=env/bin/python$(VERSION)
EASY_INSTALL=env/bin/easy_install-$(VERSION)
PYTEST=env/bin/py.test-$(VERSION)
NOSE=env/bin/nosetests-$(VERSION)

all: clean nose-cover test env-demos test-demos release

debian:
	apt-get -y update ; \
	apt-get -y dist-upgrade ; \
	apt-get -y --no-install-recommends install libbz2-dev build-essential \
		python python-dev python-setuptools python-virtualenv \

env:
	PYTHON_EXE=/usr/local/bin/python$(VERSION) ; \
    if [ ! -x $$PYTHON_EXE ]; then \
		PYTHON_EXE=/opt/local/bin/python$(VERSION) ; \
    	if [ ! -x $$PYTHON_EXE ]; then \
    		PYTHON_EXE=/usr/bin/python$(VERSION) ; \
    	fi ; \
    fi ; \
    VIRTUALENV_USE_SETUPTOOLS=1 ; \
    export VIRTUALENV_USE_SETUPTOOLS ; \
    virtualenv --python=$$PYTHON_EXE env ; \
	if [ "$$(echo $(VERSION) | sed 's/\.//')" -ge 30 ]; then \
		/bin/echo -n 'Upgrading distribute...' ; \
		$(EASY_INSTALL) -i $(PYPI) -U -O2 distribute \
			> /dev/null 2>/dev/null ; \
		/bin/echo 'done.' ; \
	fi ; \
	$(EASY_INSTALL) -i $(PYPI) -O2 coverage nose pytest \
		pytest-pep8 pytest-cov mock mako tenjin jinja2 \
		wheezy.template ; \
	if [ "$$(echo $(VERSION) | sed 's/\.//')" -eq 24 ]; then \
		$(EASY_INSTALL) -i $(PYPI) -O2 wsgiref; \
	fi ; \
	$(PYTHON) setup.py develop -i $(PYPI)

clean:
	find src/ demos/ -type d -name __pycache__ | xargs rm -rf
	find demos/*/i18n/ -name '*.mo' -delete
	find src/ demos/ -name '*.py[co]' -delete
	rm -rf dist/ build/ doc/_build/ MANIFEST src/*.egg-info .cache .coverage

release:
	$(PYTHON) setup.py -q sdist

upload:
	REV=$$(hg head --template '{rev}') ; \
	sed -i "s/'0.1'/'0.1.$$REV'/" src/wheezy/web/__init__.py ; \
	$(PYTHON) setup.py -q egg_info --tag-build .$$REV \
		sdist register upload ; \
	$(EASY_INSTALL) -i $(PYPI) sphinx ; \
	$(PYTHON) env/bin/sphinx-build -D release=0.1.$$REV \
		-a -b html doc/ doc/_build/ ; \
	python setup.py upload_docs ; \

qa:
	env/bin/flake8 --max-complexity 10 demos/hello demos/guestbook \
			doc src setup.py && \
	env/bin/pep8 demos/hello demos/guestbook doc src setup.py

test:
	$(PYTEST) -q -x --pep8 --doctest-modules src/wheezy/web

nose-cover:
	$(NOSE) --stop --with-doctest --detailed-errors \
		--with-coverage --cover-package=wheezy.web

test-cover:
	$(PYTEST) -q --cov-report term-missing \
		--cov wheezy.web --cov wheezy.web.handlers \
		--cov wheezy.web.middleware \
		src/wheezy/web/handlers/tests src/wheezy/web/middleware/tests \
		src/wheezy/web/tests

doc:
	$(PYTHON) env/bin/sphinx-build -a -b html doc/ doc/_build/

env-demos:
	make env -sC demos/quickstart-empty PYPI=$(PYPI) VERSION=$(VERSION)
	make env -sC demos/quickstart-i18n PYPI=$(PYPI) VERSION=$(VERSION)
	make env -sC demos/template PYPI=$(PYPI) VERSION=$(VERSION)

test-demos:
	$(PYTEST) -q -x --pep8 demos/hello ; \
	make clean nose-cover -sC demos/quickstart-empty VERSION=$(VERSION) ; \
	make clean po nose-cover -sC demos/quickstart-i18n VERSION=$(VERSION) ; \
	make clean po -sC demos/template VERSION=$(VERSION) ; \
	make test -sC demos/template TEMPLATE_ENGINE=jinja2 VERSION=$(VERSION) ; \
	make test -sC demos/template TEMPLATE_ENGINE=mako VERSION=$(VERSION) ; \
	make test -sC demos/template TEMPLATE_ENGINE=tenjin VERSION=$(VERSION) ; \
	make test -sC demos/template TEMPLATE_ENGINE=wheezy.template VERSION=$(VERSION) ; \
	make test -sC demos/template TEMPLATE_ENGINE=wheezy.preprocessor VERSION=$(VERSION) ; \
	if [ "$$(echo $(VERSION) | sed 's/\.//')" -eq 27 ]; then \
		make qa -sC demos/quickstart-empty VERSION=$(VERSION) ; \
		make qa -sC demos/quickstart-i18n VERSION=$(VERSION) ; \
		make qa -sC demos/template VERSION=$(VERSION) ; \
	fi
