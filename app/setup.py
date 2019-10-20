#!/usr/bin/env python
# -*- encoding: utf-8 -*-

from __future__ import absolute_import
from __future__ import print_function

from setuptools import setup, find_packages


install_requires = [
    'psycopg2-binary',
    'SQLAlchemy',
    'Flask',
    'Flask-RESTful',
    'Flask-Caching',
    'redis',
    'gunicorn',
]


setup(
    name='legalist-chintal',
    version='1.0.0',
    author="Chintalagiri Shashank",
    author_email="shashank.chintalagiri@gmail.in",
    description="legalist devops test",
    long_description="legalist devops test",
    url='https://github.com/chintal/test-devops-legalist',
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
    platforms='any',
    entry_points={
        'console_scripts': [
            'legalist-devops-test = chintal.app:run',
        ]
    },
    include_package_data=True
)
