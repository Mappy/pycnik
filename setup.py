#!/usr/bin/python
# -*- encoding=utf-8 -*-
import sys
from setuptools import setup, find_packages

if not hasattr(sys, 'version_info') or sys.version_info < (2, 7, 0, 'final'):
    raise SystemExit("pycnik requires Python 2.7 or later.")

descr = open('README.rst').read()
# hack for pypi wich doesn't support code-block directive
descr = descr.replace('.. code-block:: python', '::')
descr = descr.replace('.. code-block:: bash', '::')

setup(
    name='pycnik',
    version='1.0',
    description="Tool for generating Mapnik's stylesheets from python code",
    long_description=descr,
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
    packages=['pycnik'],
    install_requires=['lxml', 'mapnik2'],
    entry_points=dict(console_scripts=['pycnik=pycnik:main', ]),
    setup_requires=['nose>=1.0'],
    test_suite='nose.collector'
)
