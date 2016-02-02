#!/usr/bin/env python
# -*- coding: utf-8 -*-


from setuptools import setup


setup(name='pydebitoor',
      version='0.0.1',
      description='A wrapper around requests for easy communication for Debitoor API',
      url='https://github.com/idlead/pydebitoor.git',
      author='François Schmidts',
      author_email='francois.schmidts@dolead.com',
      install_requires=['requests'],
      packages=['pydebitoor', 'pydebitoor.services'])
