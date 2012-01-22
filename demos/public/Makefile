.SILENT: clean po run test
.PHONY: clean po run test

VERSION=2.7

PYTHON=../../env/bin/python$(VERSION)
PYTEST=../../env/bin/py.test-$(VERSION)


clean:
	find src/ -type d -name __pycache__ | xargs rm -rf
	find src/ -name '*.py[co]' -delete
	find src/ -name '*.mo' -delete
	rm -rf /tmp/mako_modules/

po:
	xgettext --join-existing --sort-by-file --omit-header \
		-o i18n/membership.po src/membership/**/*.py
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
	/usr/bin/uwsgi_python27 -C 777 --logto=/dev/null \
		-H ../../env/ --pythonpath src -s /tmp/uwsgi-test.sock \
		-M -w app:main

test:
	$(PYTEST) -q -x --pep8 --doctest-modules src/
