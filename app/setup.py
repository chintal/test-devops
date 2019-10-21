#!/usr/bin/env python
# -*- encoding: utf-8 -*-

from __future__ import absolute_import
from __future__ import print_function

import os
from setuptools import setup, find_packages


# Utility function to read the README file.
# Used for the long_description.  It's nice, because now 1) we have a top level
# README file and 2) it's easier to type in the README file than to put a raw
# string in below ...
def read(fname):
    orig_content = open(os.path.join(os.path.dirname(__file__), fname)).readlines()
    content = ""
    in_raw_directive = 0
    for line in orig_content:
        if in_raw_directive:
            if not line.strip():
                in_raw_directive = in_raw_directive - 1
            continue
        elif line.strip() == '.. raw:: latex':
            in_raw_directive = 2
            continue
        content += line
    return content


install_requires = [
    'psycopg2-binary',
    'SQLAlchemy',
    'Flask',
    'Flask-RESTful',
    'Flask-Caching',
    'redis',
    'gunicorn',
]

doc_requires = ['sphinx', 'sphinx-argparse', 'alabaster']

test_requires = ['pytest', 'pytest-flake8', 'pytest-cov', 'coveralls[yaml]']

setup(
    name='legalist-chintal',
    version='1.0.0',
    author="Chintalagiri Shashank",
    author_email="shashank.chintalagiri@gmail.in",
    description="legalist devops test",
    long_description='\n'.join([read('README.rst'), read('CHANGELOG.rst')]),
    url='https://github.com/chintal/test-devops',
    packages=find_packages('src'),
    package_dir={'': 'src'},
    classifiers=[
        'Natural Language :: English',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: Implementation :: CPython',
    ],
    python_requires='>=2.6',
    install_requires=install_requires,
    setup_requires=install_requires,
    extras_require={
        'docs': doc_requires,
        'tests': test_requires,
    },
    platforms='any',
    entry_points={
        'console_scripts': [
            'legalist-devops-test = chintal.app:run',
        ]
    },
    include_package_data=True
)
