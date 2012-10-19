#! /usr/bin/env python
# -*- coding: utf-8 -*-

from distutils.core import setup

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
      packages = ['socialize'],
      requires=depends
)

