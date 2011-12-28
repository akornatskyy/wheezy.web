.SILENT: clean po run
.PHONY: clean po run

VERSION=2.6

PYTHON=../../env/bin/python$(VERSION)


clean:
	find src/ -type d -name __pycache__ | xargs rm -rf
	find src/ -name '*.py[co]' -delete
	find src/ -name '*.mo' -delete
	rm -rf /tmp/mako_modules/

run:
	$(PYTHON) src/app.py

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
