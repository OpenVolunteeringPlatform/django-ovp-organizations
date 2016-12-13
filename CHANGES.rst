===========
Change log
===========

v0.1.0
-----------
* Start project
* Update README
* Add initial migration

v0.1.1
-----------
* Implement basic Organization resource

v0.1.2
-----------
* Add egg-info to gitignore
* Fix requirements.txt packages name

v0.1.3
-----------
* Add ovp_core and ovp_users to runtests
* Upgrade ovp_core, ovp_users and rest-framework

v0.1.4
-----------
* Add causes field

v0.1.5
-----------
* Return address field on OrganizationSearchSerializer

v0.1.6
-----------
* Make address field not required on OrganizationCreateSerializer

v0.1.7
-----------
* Implement slug field on Organization
* Rename .published_at, .modified_at, .deleted_at, .created_at to .published_date, .modified_date, .deleted_date, .created_date
* Update test suite coverage to 100%
* Add invite, revoke invite, join, leave and remove member routes and emails
* Add image and cover do organization

v0.1.8
-----------
* Include templates on package

v1.0.0
-----------
* Implement organization patch routes

v1.0.1
-----------
* Fix install_requires
