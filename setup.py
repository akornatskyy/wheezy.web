#!/usr/bin/env python

import os
import re

from setuptools import setup

extra = {}
try:
    from Cython.Build import cythonize
    p = os.path.join('src', 'wheezy', 'web')
    extra['ext_modules'] = cythonize(
        [os.path.join(p, '*.py'),
         os.path.join(p, 'handlers', '*.py'),
         os.path.join(p, 'middleware', '*.py')],
        exclude=[os.path.join(p, '__init__.py'),
                 os.path.join(p, 'handlers', '__init__.py'),
                 os.path.join(p, 'middleware', '__init__.py')],
        nthreads=2, quiet=True)
except ImportError:
    pass

README = open(os.path.join(os.path.dirname(__file__), 'README.md')).read()
VERSION = (
    re.search(
        r'__version__ = "(.+)"',
        open("src/wheezy/web/__init__.py").read(),
    )
    .group(1)
    .strip()
)

install_requires = [
    'wheezy.core>=0.1.131',
    'wheezy.caching>=0.1.96',
    'wheezy.html>=0.1.140',
    'wheezy.http>=0.1.314',
    'wheezy.routing>=0.1.153',
    'wheezy.security>=0.1.61',
    'wheezy.validation>=0.1.125',
]

try:
    import uuid  # noqa
except ImportError:
    install_requires.append('uuid')

setup(
    name='wheezy.web',
    version=VERSION,
    description='A lightweight, high performance, high concurrency WSGI '
    'web framework with the key features to build modern, efficient web',
    long_description=README,
    long_description_content_type='text/markdown',
    url='https://github.com/akornatskyy/wheezy.web',
    author='Andriy Kornatskyy',
    author_email='andriy.kornatskyy@live.com',
    license='MIT',
    classifiers=[
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
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: Implementation :: CPython',
        'Programming Language :: Python :: Implementation :: PyPy',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
        'Topic :: Internet :: WWW/HTTP :: WSGI',
        'Topic :: Internet :: WWW/HTTP :: WSGI :: Application',
        'Topic :: Internet :: WWW/HTTP :: WSGI :: Middleware',
        'Topic :: Software Development :: Libraries :: Application Frameworks',
        'Topic :: Software Development :: Libraries :: Python Modules'
    ],
    keywords='wsgi web handler static template mako tenjin jinja2 '
             'routing middleware caching transforms',
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
            'wheezy.template>=0.1.107'
        ]
    },
    platforms='any',
    **extra
)
