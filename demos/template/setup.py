#!/usr/bin/env python

import os

try:
    from setuptools import setup
except:
    from distutils.core import setup

README = open(os.path.join(os.path.dirname(__file__), 'README')).read()

install_requires = [
    'wheezy.core>=0.1.70',
    'wheezy.caching>=0.1.54',
    'wheezy.html>=0.1.106',
    'wheezy.http>=0.1.236',
    'wheezy.routing>=0.1.124',
    'wheezy.security>=0.1.36',
    'wheezy.validation>=0.1.74',
    'wheezy.web>=0.1.259',
]

try:
    import uuid
except:
    install_requires.append('uuid')

setup(
    name='mysite',
    version='0.1',
    description='MySite Project',
    long_description=README,
    url='https://scm.dev.local/svn/mysite/trunk',

	author='MySite Team',
    author_email='mysite at dev.local',

    license='COMMERCIAL',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'Natural Language :: English',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: Implementation :: CPython',
        'Programming Language :: Python :: Implementation :: PyPy',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
        'Topic :: Internet :: WWW/HTTP :: WSGI',
        'Topic :: Internet :: WWW/HTTP :: WSGI :: Application',
        'Topic :: Software Development :: Libraries :: Python Modules'
    ],
    packages=[
        'membership',
        'public',
    ],
    package_dir={'': 'src'},

    zip_safe=False,
    install_requires=install_requires,
    extras_require={
        'dev': [
            'coverage',
            'nose',
            'pytest',
            'pytest-pep8',
            'pytest-cov'
        ],
        'mako': [
            'mako>=0.7.0'
        ],
        'tenjin': [
            'tenjin>=1.1.0'
        ],
        'jinja2': [
            'jinja2>=2.6'
        ],
        'wheezy.template': [
            'wheezy.template>=0.1.75'
        ]
    },

    platforms='any'
)
