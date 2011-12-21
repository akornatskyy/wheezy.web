.SILENT: clean po run
.PHONY: clean po run

VERSION=2.6

PYTHON=../../env/bin/python$(VERSION)


clean:
	find src/ -type d -name __pycache__ | xargs rm -rf
	find src/ -name '*.py[co]' -delete
	find src/ -name '*.mo' -delete

run:
	$(PYTHON) src/app.py

po:
	xgettext --join-existing --sort-by-file --omit-header \
		-o i18n/membership.po src/membership/*.py
	cp i18n/membership.po i18n/en/LC_MESSAGES
	for l in `ls --hide *.po i18n`; do \
		echo -n "$$l => "; \
		msgfmt -v i18n/$$l/LC_MESSAGES/membership.po \
			-o i18n/$$l/LC_MESSAGES/membership.mo; \
	done
