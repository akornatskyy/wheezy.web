.SILENT: clean po run test benchmark
.PHONY: clean po run test benchmark

VERSION=2.7

ENV=../../env
PYTHON=$(ENV)/bin/python$(VERSION)
PYTEST=$(ENV)/bin/py.test-$(VERSION)
NOSE=$(ENV)/bin/nosetests-$(VERSION)


clean:
	find src/ -type d -name __pycache__ | xargs rm -rf
	find src/ -name '*.py[co]' -delete
	find src/ -name '*.mo' -delete
	rm -rf /tmp/mako_modules/

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
	$(ENV)/bin/uwsgi -C 777 --logto=/dev/null -p 2 \
		-H $(ENV) --pythonpath src -s /tmp/uwsgi-test.sock \
		-M -w app:main

gunicorn:
	export PYTHONPATH=$$PYTHONPATH:./src ; \
		$(ENV)/bin/gunicorn -b 0.0.0.0:8080 -w 2 app:main

test:
	$(PYTEST) -q -x --pep8 --doctest-modules src/

benchmark:
	$(NOSE) -qs -m benchmark src/
