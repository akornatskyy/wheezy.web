#!/usr/bin/env python

import os
import sys

try:
    from setuptools import setup
except:
    from distutils.core import setup  # noqa

README = open(os.path.join(os.path.dirname(__file__), 'README.rst')).read()

install_requires = [
    'wheezy.core>=0.1.131',
    'wheezy.caching>=0.1.96',
    'wheezy.html>=0.1.140',
    'wheezy.http>=0.1.314',
    'wheezy.routing>=0.1.153',
    'wheezy.security>=0.1.61',
    'wheezy.validation>=0.1.125',
    'wheezy.web>=0.1.450'
]

install_optional = [
    #'PIL>=1.1.7',
    'pycrypto>=2.6.1'
]

if sys.version_info[0] == 2:
    install_optional.append('pylibmc>=1.2.3')

install_requires += install_optional

try:
    import uuid  # noqa
except ImportError:
    install_requires.append('uuid')

dependency_links = [
    # pylibmc
    'https://bitbucket.org/akorn/wheezy.caching/downloads',
    # PIL
    #'https://bitbucket.org/akorn/wheezy.captcha/downloads',
    # pycrypto
    'https://bitbucket.org/akorn/wheezy.security/downloads'
]

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
        'membership.repository',
        'membership.service',
        'membership.web',
        'public',
        'public.web'
    ],
    package_dir={'': 'src'},

    zip_safe=False,
    install_requires=install_requires,
    dependency_links=dependency_links,
    extras_require={
        'dev': [
            'coverage',
            'nose',
            'pytest',
            'pytest-pep8',
            'pytest-cov',
            'mock'
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
            'wheezy.template>=0.1.107'
        ]
    },

    platforms='any'
)
