#!/usr/bin/env python

import os

from setuptools import setup


README = open(os.path.join(os.path.dirname(__file__), 'README.rst')).read()

install_requires = [
    'wheezy.core>=0.1.104',
    'wheezy.caching>=0.1.90',
    'wheezy.html>=0.1.130',
    'wheezy.http>=0.1.287',
    'wheezy.routing>=0.1.145',
    'wheezy.security>=0.1.46',
    'wheezy.template>=0.1.135',
    'wheezy.validation>=0.1.91',
    'wheezy.web>=0.1.373',
]

install_optional = [
    'pylibmc>=1.2.3',
    #'PIL>=1.1.7',
    'lxml>=3.2.0',
    'pycrypto>=2.6',
]

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
    # lxml
    'https://bitbucket.org/akorn/wheezy.http/downloads',
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
        'public',
        'public.web'
    ],
    package_dir={'': 'src'},

    zip_safe=False,
    install_requires=install_requires,
    dependency_links=dependency_links,
    extras_require={
    },

    platforms='any'
)