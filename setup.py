#!/usr/bin/env python
# -*- coding: utf-8 -*-
from setuptools import setup, find_packages

setup(
    name='ovp-organizations',
    version='1.0.4',
    author=u'Atados',
    author_email='arroyo@atados.com.br',
    packages=find_packages(),
    include_package_data=True,
    url='https://github.com/OpenVolunteeringPlatform/django-ovp-organizations',
    download_url = 'https://github.com/OpenVolunteeringPlatform/django-ovp-organizations/tarball/1.0.4',
    license='AGPL',
    description='This module has core functionality for' + \
                ' ovp organization, such as: creating, listing,' + \
                ' editing and retrieving.',
    long_description=open('README.rst', encoding='utf-8').read(),
    zip_safe=False,
    install_requires = [
      'Django>=1.10.1,<1.11.0',
      'djangorestframework>=3.5.3,<3.6.0',
      'codecov>=2.0.5,<2.1.0',
      'coverage>=4.2,<4.3.0',
      'ovp-users>=1.0.10,<1.1.0',
      'ovp-core>=1.0.3,<1.1.0',
      'ovp-uploads>=1.0.0,<1.1.0',
      'ovp-users>=1.0.10,<1.1.0',
      'ovp-core>=1.0.11,<1.1.0',
      'ovp-uploads>=1.0.0,<1.1.0'
    ]
)
