.SILENT: env clean po run test benchmark
.PHONY: env clean po run test benchmark

VERSION=2.7
PYPI=http://pypi.python.org/simple
ENV=../../env
TEMPLATE_ENGINE=wheezy.preprocessor

PYTHON=$(ENV)/bin/python$(VERSION)
EASY_INSTALL=$(ENV)/bin/easy_install-$(VERSION)
PYTEST=$(ENV)/bin/py.test-$(VERSION)
NOSE=$(ENV)/bin/nosetests-$(VERSION)


all: clean po test-cover release

env:
	PYTHON_EXE=/usr/local/bin/python$(VERSION); \
	if [ ! -x $$PYTHON_EXE ]; then \
		    PYTHON_EXE=/usr/bin/python$(VERSION); \
	fi;\
	virtualenv --python=$$PYTHON_EXE env
	$(EASY_INSTALL) -i $(PYPI) -O2 coverage nose pytest \
	        pytest-pep8 pytest-cov lxml mako tenjin jinja2 wheezy.template
	# The following packages available for python == 2.4
	if [ "$$(echo $(VERSION) | sed 's/\.//')" -eq 24 ]; then \
		$(EASY_INSTALL) -i $(PYPI) -O2 wsgiref; \
	fi
	$(PYTHON) setup.py develop -i $(PYPI)

clean:
	find src/ -type d -name __pycache__ | xargs rm -rf
	find src/ -name '*.py[co]' -delete
	find src/ -name '*.mo' -delete
	find src/ -name '*.cache' -delete
	rm -rf /tmp/mako_modules/ .cache .coverage

release:
	$(PYTHON) setup.py -q egg_info sdist

po:
	xgettext --join-existing --sort-by-file --omit-header \
		--language=Python \
		-o i18n/en/LC_MESSAGES/shared.po \
		content/templates-jinja2/shared/**/*.html \
		content/templates-mako/shared/**/*.html \
		content/templates-tenjin/shared/**/*.html \
		content/templates-preprocessor/shared/**/*.html \
		content/templates-wheezy/shared/**/*.html
	xgettext --join-existing --sort-by-file --omit-header \
		--language=Python \
		-o i18n/en/LC_MESSAGES/public.po src/public/**/*.py \
		content/templates-jinja2/public/*.html \
		content/templates-mako/public/*.html \
		content/templates-tenjin/public/*.html \
		content/templates-preprocessor/public/*.html \
		content/templates-wheezy/public/*.html
	xgettext --join-existing --sort-by-file --omit-header \
		--language=Python \
		-o i18n/en/LC_MESSAGES/membership.po src/membership/**/*.py \
		content/templates-jinja2/membership/*.html \
		content/templates-mako/membership/*.html \
		content/templates-tenjin/membership/*.html \
		content/templates-preprocessor/membership/*.html \
		content/templates-wheezy/membership/*.html
	for l in `ls -d i18n/*/ | cut -d / -f 2`; do \
		echo -n "$$l => "; \
		msgfmt -v i18n/$$l/LC_MESSAGES/public.po \
			i18n/$$l/LC_MESSAGES/shared.po \
			-o i18n/$$l/LC_MESSAGES/public.mo; \
		msgfmt -v i18n/$$l/LC_MESSAGES/membership.po \
			i18n/$$l/LC_MESSAGES/shared.po \
			-o i18n/$$l/LC_MESSAGES/membership.mo; \
		msgfmt -v i18n/$$l/LC_MESSAGES/validation.po \
			-o i18n/$$l/LC_MESSAGES/validation.mo; \
	done

run:
	echo $(TEMPLATE_ENGINE) ; export TEMPLATE_ENGINE=$(TEMPLATE_ENGINE) ; \
	$(PYTHON) src/app.py

uwsgi:
	echo $(TEMPLATE_ENGINE) ; export TEMPLATE_ENGINE=$(TEMPLATE_ENGINE) ; \
	$(ENV)/bin/uwsgi --ini development.ini

gunicorn:
	echo $(TEMPLATE_ENGINE) ; export TEMPLATE_ENGINE=$(TEMPLATE_ENGINE) ; \
	export PYTHONPATH=$$PYTHONPATH:./src ; \
		$(ENV)/bin/gunicorn -b 0.0.0.0:8080 -w 1 app:main

qa:
	if [ "$$(echo $(VERSION) | sed 's/\.//')" -eq 27 ]; then \
		flake8 --max-complexity 6 src setup.py && \
		pep8 src setup.py ; \
	fi

test:
	echo $(TEMPLATE_ENGINE) ; export TEMPLATE_ENGINE=$(TEMPLATE_ENGINE) ; \
	$(PYTEST) -q -x --pep8 --doctest-modules src/

nose-cover:
	$(NOSE) --stop --with-doctest --detailed-errors \
		--with-coverage --cover-package=public --cover-package=membership

test-cover:
	$(PYTEST) -q -x --cov membership --cov public \
		--cov-report term-missing \
		src/

benchmark:
	echo $(TEMPLATE_ENGINE) ; export TEMPLATE_ENGINE=$(TEMPLATE_ENGINE) ; \
	$(NOSE) -qs -m benchmark_views src/

profile:
	echo $(TEMPLATE_ENGINE) ; export TEMPLATE_ENGINE=$(TEMPLATE_ENGINE) ; \
	$(NOSE) -qs -m benchmark_views --with-profile \
		--profile-stats-file=profile.pstats src/public

gropf:
	gprof2dot.py -f pstats profile.pstats | dot -Tpng -o profile.png
