.SILENT: clean env pypy uwsgi gunicorn
.PHONY: clean env pypy uwsgi gunicorn

VERSION=2.7
PYPI=http://pypi.python.org/simple
ENV=../../env

PYTHON=$(ENV)/bin/python$(VERSION)
PYPY=../../pypy-1.9

SERVER=uwsgi


env:
	PYTHON_EXE=/usr/local/bin/python$(VERSION); \
	if [ ! -x $$PYTHON_EXE ]; then \
		    PYTHON_EXE=/usr/bin/python$(VERSION); \
	fi; \
	virtualenv --python=$$PYTHON_EXE --no-site-packages env

	$(ENV)/bin/easy_install-$(VERSION) -i $(PYPI) -O2 \
		uwsgi mako wheezy.web

pypy:
	if [ ! -f $(PYPY)-linux.tar.bz2 ]; then \
		wget https://bitbucket.org/pypy/pypy/downloads/$(PYPY)-linux.tar.bz2; \
	fi; \
	tar xjf $(PYPY)-linux.tar.bz2; \
	wget http://python-distribute.org/distribute_setup.py; \
	$(PYPY)/bin/pypy distribute_setup.py ; \
	$(PYPY)/bin/easy_install -i $(PYPI) -O2 \
		gunicorn mako wheezy.web

clean:
	find ./ -type d -name __pycache__ | xargs rm -rf
	find ./ -name '*.py[co]' -delete

uwsgi:
	$(ENV)/bin/uwsgi --ini config.ini

gunicorn:
	export PYTHONPATH=$$PYTHONPATH:. ; \
	$(ENV)/bin/gunicorn -b 0.0.0.0:8080 -w 4 app:main
