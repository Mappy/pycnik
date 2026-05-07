#!/usr/bin/python
# -*- encoding=utf-8 -*-
import os
import re
import sys
from setuptools import setup

if sys.argv[-1] == 'publish':
    os.system('python setup.py register sdist upload')
    sys.exit()


def rst(filename):
    '''
    Load rst file and sanitize it for PyPI.
    Remove unsupported tags:
     - code-block directive
    '''
    content = open(filename).read()
    return re.sub(r'\.\.\s? code-block::\s*(\w|\+)+', '::', content)


long_description = '\n'.join((
    rst('README.rst'),
    rst('CHANGELOG.rst'),
    ''
))


def install_requires():
    """
    don't try to override mapnik installation with the pypi version
    """
    req = ['lxml', 'pyproj']
    return req

develop_requirements = install_requires() + ['pytest>=8.0']

setup(
    name='pycnik',
    version=__import__('pycnik').__version__,
    description="Tool for generating Mapnik's stylesheets from python code",
    long_description=long_description,
    url="https://github.com/Mappy/pycnik.git",
    author='Ludovic Delauné',
    author_email="ludovic.delaune@mappy.com",
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'Intended Audience :: Science/Research',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.13',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
        'Topic :: Utilities'
        ],
    python_requires='>=3.13,<4',
    packages=['pycnik'],
    install_requires=install_requires(),
    extras_require={
        'develop': develop_requirements,
    },
    entry_points=dict(console_scripts=['pycnik=pycnik:main', ])
)
