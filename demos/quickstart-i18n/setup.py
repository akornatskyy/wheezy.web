#!/usr/bin/env python

import os

from setuptools import setup

README = open(os.path.join(os.path.dirname(__file__), "README.rst")).read()

install_requires = [
    "wheezy.core>=0.1.131",
    "wheezy.caching>=0.1.106",
    "wheezy.html>=0.1.140",
    "wheezy.http>=0.1.314",
    "wheezy.routing>=0.1.153",
    "wheezy.security>=0.1.61",
    "wheezy.template>=0.1.151",
    "wheezy.validation>=0.1.125",
    "wheezy.web>=0.1.450",
]

dependency_links = []

setup(
    name="mysite",
    version="0.1",
    python_requires=">=3.6",
    description="MySite Project",
    long_description=README,
    url="https://scm.dev.local/svn/mysite/trunk",
    author="MySite Team",
    author_email="mysite at dev.local",
    license="COMMERCIAL",
    classifiers=[
        "Environment :: Web Environment",
        "Intended Audience :: Developers",
        "Natural Language :: English",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: Implementation :: CPython",
        "Programming Language :: Python :: Implementation :: PyPy",
        "Topic :: Internet :: WWW/HTTP",
        "Topic :: Internet :: WWW/HTTP :: Dynamic Content",
        "Topic :: Internet :: WWW/HTTP :: WSGI",
        "Topic :: Internet :: WWW/HTTP :: WSGI :: Application",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
    packages=["public", "public.web"],
    package_dir={"": "src"},
    zip_safe=False,
    install_requires=install_requires,
    dependency_links=dependency_links,
    extras_require={},
    platforms="any",
)
