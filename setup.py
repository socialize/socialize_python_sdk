#! /usr/bin/env python
# -*- coding: utf-8 -*-

from setuptools import setup

depends = [
    'nose',
    'coverage',
    'httplib2',
    'oauth2',
    'mock'
]

setup(name='socialize_python_sdk',
      version='0.0',
      description='Socialize Python SDK',
      author='Champ Somsuk',
      author_email='champ.somsuk@getsocialize.com',
      package_dir = {'': 'socialize'},
      install_requires=depends,
      test_suite='nose.collector'
)

