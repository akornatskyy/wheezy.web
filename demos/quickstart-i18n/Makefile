.SILENT: virtualenv env clean release dep install po run uwsgi gunicorn qa test nose-cover test-cover benchmark profile gropf
.PHONY: virtualenv env clean release dep install po run uwsgi gunicorn qa test nose-cover test-cover benchmark profile gropf

VERSION=2.7
PYPI=http://pypi.python.org/simple
ENV=env

PYTHON=$(ENV)/bin/python$(VERSION)
EASY_INSTALL=$(ENV)/bin/easy_install-$(VERSION)
PYTEST=$(ENV)/bin/py.test-$(VERSION)
NOSE=$(ENV)/bin/nosetests-$(VERSION)


all: clean po nose-cover release

virtualenv:
	PYTHON_EXE=/usr/local/bin/python$(VERSION) ; \
    if [ ! -x $$PYTHON_EXE ]; then \
		PYTHON_EXE=/opt/local/bin/python$(VERSION) ; \
    	if [ ! -x $$PYTHON_EXE ]; then \
    		PYTHON_EXE=/usr/bin/python$(VERSION) ; \
    	fi ; \
    fi ; \
    virtualenv --python=$$PYTHON_EXE $(ENV)

env: virtualenv
	$(EASY_INSTALL) -i $(PYPI) -O2 coverage nose pytest \
	        pytest-pep8 pytest-cov lxml
	if [ "$$(echo $(VERSION) | sed 's/\.//')" -eq 24 ]; then \
		$(EASY_INSTALL) -i $(PYPI) -O2 wsgiref ; \
	else \
		$(EASY_INSTALL) -i $(PYPI) -O2 flake8 ; \
	fi ; \
	if [ `uname` = 'FreeBSD' ]; then \
	    export LIBMEMCACHED=/usr/local ; \
	fi ; \
	$(PYTHON) setup.py develop -O2 -U -i $(PYPI)

clean:
	find src/ -type d -name __pycache__ | xargs rm -rf
	find src/ -name '*.py[co]' -delete
	find i18n/ -name '*.mo' -delete
	find src/ -name '*.cache' -delete
	rm -rf .cache .coverage src/*.egg-info/ build/ dist/

release:
	#$(PYTHON) setup.py -q egg_info sdist
	rm -rf src/*.egg-info/ ; \
	REV=$$(hg head --template '{rev}') ; \
    $(PYTHON) setup.py -q egg_info --tag-build .$$REV sdist ; \
	NAME=$$($(PYTHON) setup.py --fullname).$$REV ; \
	rm -rf dist/$$NAME ; \
	tar xzf dist/$$NAME.tar.gz -C dist/ ; \
	rm dist/$$NAME.tar.gz ; \
	sed -i '' "s/, 0)/, $$REV)/" dist/$$NAME/src/public/__init__.py ; \
	tar cf - -C dist/ $$NAME | gzip -9 - > dist/$$NAME.tar.gz ; \
	rm -rf dist/$$NAME

dep:
	if [ -f /etc/debian_version ]; then \
	    apt-get update ; \
		apt-get install --no-install-recommends -y build-essential \
			python$(VERSION) python$(VERSION)-dev python-setuptools \
			python-virtualenv gettext libgmp-dev ; \
	    apt-get clean ; \
	else \
		echo This OS is not supported yet. ; \
		exit 1 ; \
	fi

install: virtualenv
	$(PYTHON) setup.py develop -O2 -U -i $(PYPI)

po:
	get_text() { \
		for f in $$@; do \
			(find content/templates/$$f -name '*.html' ; \
		     find src/$$f -name '*.py' 2>/dev/null) \
		        | xargs grep -E "_\(['\"]" \
			    | sed -E "s/[u]?'#_\('([^']*)'\)'/_('\1')/g" \
			    | sed -E "s/[u]?'#_\(\"([^\"]*)\"\)'/_(\"\1\")/g" \
			    | sed -E "s/[u]?\"#_\('([^']*)'\)\"/_('\1')/g" \
			    | sed -E "s/[u]?\"#_\(\"([^\"]*)\"\)\"/_(\"\1\")/g" \
			    | sed -E "s/#_\('([^']*)'\)/_('\1')/g" \
			    | sed -E "s/#_\(\"([^\"]*)\"\)/_(\"\1\")/g" \
			    | xgettext --join-existing --no-location --omit-header \
				    --language=Python -o i18n/en/LC_MESSAGES/$$f.po - ; \
		done \
	} ; \
	get_text shared public
	for l in `ls -d i18n/*/ | cut -d / -f 2`; do \
		/bin/echo -n "$$l => "; \
		msgfmt -v i18n/$$l/LC_MESSAGES/public.po \
			i18n/$$l/LC_MESSAGES/shared.po \
			-o i18n/$$l/LC_MESSAGES/public.mo; \
		msgfmt -v i18n/$$l/LC_MESSAGES/validation.po \
			-o i18n/$$l/LC_MESSAGES/validation.mo; \
	done

run:
	if [ -f src/app.pyo ]; then \
		$(PYTHON) -OO src/app.pyo ; \
	else \
		$(PYTHON) src/app.py ; \
	fi

uwsgi:
	$(ENV)/bin/uwsgi --ini development.ini

gunicorn:
	export PYTHONPATH=$$PYTHONPATH:./src ; \
		$(ENV)/bin/gunicorn -b 0.0.0.0:8080 -w 1 app:main

qa:
	$(ENV)/bin/flake8 --max-complexity 6 src setup.py && \
	$(ENV)/bin/pep8 src setup.py

test:
	$(PYTEST) -q -x --pep8 --doctest-modules src/

nose-cover:
	$(NOSE) --stop --with-doctest --detailed-errors --with-coverage \
		--cover-package=public src/

test-cover:
	$(PYTEST) -q -x --cov-report term-missing src/ --cov public

benchmark:
	$(NOSE) -qs -m benchmark_views src/

profile:
	$(NOSE) -qs -m benchmark_views --with-profile \
		--profile-stats-file=profile.pstats src/public

gprof:
	gprof2dot.py -f pstats profile.pstats | dot -Tpng -o profile.png
