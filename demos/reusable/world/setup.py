import os

from setuptools import setup

README = open(os.path.join(os.path.dirname(__file__), "README.rst")).read()

install_requires = ["wheezy.template", "wheezy.web", "hello"]

dependency_links = []

setup(
    name="helloworld",
    version="0.1",
    python_requires=">=3.6",
    description="Hello World Project",
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
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: Implementation :: CPython",
        "Programming Language :: Python :: Implementation :: PyPy",
        "Topic :: Internet :: WWW/HTTP",
        "Topic :: Internet :: WWW/HTTP :: Dynamic Content",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
    packages=[],
    package_dir={"": "src"},
    zip_safe=False,
    install_requires=install_requires,
    dependency_links=dependency_links,
    extras_require={},
    platforms="any",
)
