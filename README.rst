==========
OVP Projects
==========

.. image:: https://app.codeship.com/projects/01c71ae0-73a1-0134-6261-42bac1247deb/status?branch=master
.. image:: https://codecov.io/gh/OpenVolunteeringPlatform/django-ovp-nonprofits/branch/master/graph/badge.svg
  :target: https://codecov.io/gh/OpenVolunteeringPlatform/django-ovp-nonprofits

This module implements core user functionality.

Getting Started
---------------
Installing
""""""""""""""
1. Install django-ovp-nonprofits::

    pip install ovp-nonprofits

2. Add it to `INSTALLED_APPS` on `settings.py`

3. Add `rest_framework_jwt` to `INSTALLED_APPS`


Forking
""""""""""""""
If you have your own OVP installation and want to fork this module
to implement custom features while still merging changes from upstream,
take a look at `django-git-submodules <https://github.com/leonardoarroyo/django-git-submodules>`_.

Testing
---------------
To test this module

::

  python ovp_nonprofits/tests/runtests.py

Contributing
---------------
Please read `CONTRIBUTING.md <https://github.com/OpenVolunteeringPlatform/django-ovp-users/blob/master/CONTRIBUTING.md>`_ for details on our code of conduct, and the process for submitting pull requests to us.

Versioning
---------------
We use `SemVer <http://semver.org/>`_ for versioning. For the versions available, see the `tags on this repository <https://github.com/OpenVolunteeringPlatform/django-ovp-users/tags>`_. 

License
---------------
This project is licensed under the GNU GPLv3 License see the `LICENSE.md <https://github.com/OpenVolunteeringPlatform/django-ovp-users/blob/master/LICENSE.md>`_ file for details
