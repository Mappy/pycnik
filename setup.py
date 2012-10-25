#!/usr/bin/python
# -*- encoding=utf-8 -*-
import os
import re
import sys
from setuptools import setup

if not hasattr(sys, 'version_info') or sys.version_info < (2, 7, 0, 'final'):
    raise SystemExit("pycnik requires Python 2.7 or later.")

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
    req = ['lxml']
    try:
        import mapnik
    except ImportError:
        try:
            import mapnik2
        except:
            req.append('mapnik2')
    return req

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
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
        'Topic :: Utilities'
        ],
    packages=['pycnik'],
    install_requires=install_requires(),
    entry_points=dict(console_scripts=['pycnik=pycnik:main', ]),
    setup_requires=['nose>=1.0'],
    test_suite='nose.collector'
)
