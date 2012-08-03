#!/usr/bin/python
# -*- encoding=utf-8 -*-
import sys
from setuptools import setup, find_packages

if not hasattr(sys, 'version_info') or sys.version_info < (2, 7, 0, 'final'):
    raise SystemExit("pycnik requires Python 2.7 or later.")

install_requires = ['lxml']

setup(
    name='pycnik',
    version='1.0',
    description="Tool for generating Mapnik's stylesheets from python code",
    url="https://github.com/ldgeo/pycnik.git",
    author='Ludovic Delauné',
    author_email="ludotux@gmail.com",
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
    packages=find_packages('pycnik'),
    install_requires=install_requires,
    entry_points=dict(console_scripts=['pycnik=pycnik:main', ]),
    setup_requires=['nose>=1.0'],
    test_suite='nose.collector'
)
