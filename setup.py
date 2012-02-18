#!/usr/bin/env python

import os

try:
    from setuptools import setup
except:
    from distutils.core import setup

README = open(os.path.join(os.path.dirname(__file__), 'README')).read()

install_requires = [
    'wheezy.core',
    'wheezy.caching',
    'wheezy.html',
    'wheezy.http',
    'wheezy.routing',
    'wheezy.security',
    'wheezy.validation',
    'mako'
]

try:
    import uuid
except:
    install_requires.append('uuid')

setup(
    name='wheezy.web',
    version='0.1',
    description='A lightweight web library',
    long_description=README,
    url='https://bitbucket.org/akorn/wheezy.web',

    author='Andriy Kornatskyy',
    author_email='andriy.kornatskyy at live.com',

    license='MIT',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.4',
        'Programming Language :: Python :: 2.5',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.2',
        'Programming Language :: Python :: Implementation :: CPython',
        'Programming Language :: Python :: Implementation :: PyPy',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
        'Topic :: Internet :: WWW/HTTP :: WSGI',
        'Topic :: Internet :: WWW/HTTP :: WSGI :: Application',
        'Topic :: Internet :: WWW/HTTP :: WSGI :: Middleware',
        'Topic :: Software Development :: Libraries :: Application Frameworks',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Topic :: Software Development :: Quality Assurance',
        'Topic :: Software Development :: Testing',
        'Topic :: Utilities'
    ],
    keywords='wsgi web handler static file template mako errors routing '
             'middleware caching transforms',
    packages=[
        'wheezy',
        'wheezy.web',
        'wheezy.web.handlers',
        'wheezy.web.middleware'
    ],
    package_dir={'': 'src'},
    namespace_packages=['wheezy'],

    zip_safe=False,
    install_requires=install_requires,
    extras_require={
        'dev': [
            'coverage',
            'nose',
            'pytest',
            'pytest-pep8',
            'pytest-cov'
        ]
    },

    platforms='any'
)
