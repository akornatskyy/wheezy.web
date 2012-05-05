.SILENT: env clean po run test benchmark
.PHONY: env clean po run test benchmark

VERSION=2.7
PYPI=http://pypi.python.org/simple
ENV=../../env

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
	        pytest-pep8 pytest-cov wsgiref
	$(PYTHON) setup.py develop -i $(PYPI)

clean:
	find src/ -type d -name __pycache__ | xargs rm -rf
	find src/ -name '*.py[co]' -delete
	find src/ -name '*.mo' -delete
	rm -rf /tmp/mako_modules/

release:
	$(PYTHON) setup.py -q egg_info sdist

po:
	xgettext --join-existing --sort-by-file --omit-header \
		--language=Python \
		-o i18n/membership.po src/membership/**/*.py \
		content/templates/membership/*.html
	cp i18n/membership.po i18n/en/LC_MESSAGES
	cp i18n/validation.po i18n/en/LC_MESSAGES
	for l in `ls --hide *.po i18n`; do \
		echo -n "$$l => "; \
		msgfmt -v i18n/$$l/LC_MESSAGES/membership.po \
			-o i18n/$$l/LC_MESSAGES/membership.mo; \
		msgfmt -v i18n/$$l/LC_MESSAGES/validation.po \
			-o i18n/$$l/LC_MESSAGES/validation.mo; \
	done

run:
	$(PYTHON) src/app.py

uwsgi:
	$(ENV)/bin/uwsgi -C 777 --logto=/dev/null -p 1 \
		-H $(ENV) --pythonpath src -s /tmp/uwsgi-test.sock \
		-M -w app:main

gunicorn:
	export PYTHONPATH=$$PYTHONPATH:./src ; \
		$(ENV)/bin/gunicorn -b 0.0.0.0:8080 -w 1 app:main

test:
	$(PYTEST) -q -x --pep8 --doctest-modules src/

test-cover:
	$(PYTEST) -q -x --cov membership --cov public \
		--cov-report term-missing \
		src/

benchmark:
	$(NOSE) -qs -m benchmark src/

profile:
	$(NOSE) -qs -m benchmark --with-profile \
		--profile-stats-file=public.pstats src/membership

gropf:
	gprof2dot.py -f pstats public.pstats | dot -Tpng -o public.png
