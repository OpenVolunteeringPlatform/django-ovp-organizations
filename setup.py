# -*- coding: utf-8 -*-
from distutils.core import setup

setup(
    name='ovp-nonprofits',
    version='0.1.0',
    author=u'Atados',
    author_email='arroyo@atados.com.br',
    packages=['ovp_nonprofits'],
    url='https://github.com/OpenVolunteeringPlatform/django-ovp-nonprofits',
    download_url = 'https://github.com/OpenVolunteeringPlatform/django-ovp-nonprofits/tarball/0.1.0',
    license='AGPL',
    description='This module has core functionality for' + \
                ' ovp nonprofits, such as: creation, listing,' + \
                ' editing and retrieving.',
    long_description=open('README.rst', encoding='utf-8').read(),
    zip_safe=False,
    install_requires = [
      'Django>=1.10.1,<1.11.0',
      'djangorestframework>=3.4.7,<3.5.0',
      'djangorestframework-jwt>=1.8.0,<1.9.0',
      'python-dateutil>=2.5.3,<2.6.0',
      'codecov>=2.0.5,<2.1.0',
      'coverage>=4.2,<4.3.0'
    ]
)
