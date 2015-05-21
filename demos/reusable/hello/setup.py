import os

from setuptools import setup


README = open(os.path.join(os.path.dirname(__file__), 'README.rst')).read()

install_requires = [
    'wheezy.template',
    'wheezy.web'
]

dependency_links = [
]

setup(
    name='hello',
    version='0.1',
    description='Hello Project',
    long_description=README,
    url='https://scm.dev.local/svn/mysite/trunk',

    author='MySite Team',
    author_email='mysite at dev.local',

    license='MIT',
    classifiers=[
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: Implementation :: CPython',
        'Programming Language :: Python :: Implementation :: PyPy',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content'
    ],
    packages=[
        'hello',
        'hello.service',
        'hello.web'
    ],
    include_package_data=True,
    package_dir={'': 'src'},

    zip_safe=False,
    install_requires=install_requires,
    dependency_links=dependency_links,
    extras_require={
    },

    platforms='any'
)
