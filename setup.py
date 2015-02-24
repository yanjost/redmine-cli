import os, sys
from setuptools import setup, find_packages

from redminecli import __version__


def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

requirements = [
    "prettytable==0.7.2",
    "requests==2.2.0",
    "memoizer==0.0.1"
]

if sys.version.startswith("2.6"):
    requirements.append("argparse==1.3.0")

setup(
    name = "Redmine-CLI",
    version = ".".join(map(str, __version__)),
    description = "A command-line utility to interact with Redmine",
    long_description = read('README.rst'),
    url = 'http://github.com/yanjost/redmine-cli',
    license = 'MIT',
    author = 'Yannick JOST',
    author_email = 'yannick@yjost.com',
    packages = ['redminecli'],#find_packages(exclude=['tests']),
    include_package_data = True,
    classifiers = [
        'Development Status :: 3 - Alpha',
        'Environment :: Console',
        'Intended Audience :: Developers',
        'Intended Audience :: Information Technology',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
    ],
    install_requires = requirements,
    tests_require = [],
    entry_points={
        'console_scripts': [
            'redmine = redminecli.main:main',
        ]
    }
)
