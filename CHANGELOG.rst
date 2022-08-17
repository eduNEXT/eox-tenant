Change Log
----------

..
   All enhancements and patches to eox-tenant will be documented
   in this file.  It adheres to the structure of http://keepachangelog.com/ ,
   but in reStructuredText instead of Markdown (for ease of incorporation into
   Sphinx documentation and the PyPI description).
   
   This project adheres to Semantic Versioning (http://semver.org/).
.. There should always be an "Unreleased" section for changes pending release.

Unreleased
~~~~~~~~~~

[6.0.1] - 2022-08-17
~~~~~~~~~~~~~~~~~~~~

added
-----

* add support for Nutmeg release
* update django requirement

[6.0.0] - 2022-03-07
~~~~~~~~~~~~~~~~~~~~

Changed
-------

* **BREAKING CHANGE**: remove the Course Management feature
* **BREAKING CHANGE**: django32: Drop python 3.5 support in favor of python 3.8.

Performance Improvements
------------------------

* django32: add compatibility with openedx maple release
* change code to pass tests

Continuous Integration
----------------------

* add test actions to github workflows

Code Refactoring
----------------

* change function format by an f-string

[5.1.3] - 2022-01-14
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Fixed
-----

* Update backend for edxmako so it's lilac compatible.

[5.1.2] - 2021-12-02
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Fixed
-----

* TenantSiteConfigProxy.site_values returns a serializable subset of settings
  to avoid an exception while sending emails.


[5.1.1] - 2021-11-29
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Fixed
_____

* UserSignupSource import in order to avoid raising an exception when running tests.

[5.1.0] - 2021-11-22
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Added
_______

* Support for message passing via protocol V2

[5.0.1] - 2021-10-29
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Fixed
_____

* Changed OAUTH2_PROVIDER test setting for the CMS

[5.0.0] - 2021-10-29
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Fixed
_____

* Changed OAUTH2_PROVIDER test setting to the platform value

Changed
_____

* **BREAKING CHANGE**: Default backends for edxapp users and branding_api are not compatible with Juniper.

[4.1.0] - 2021-10-27
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Added
_______

* Set Lilac backends as default in the Common settings file.
* Update readme with new information and formats.


[4.0.0] - 2021-05-10
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Removed
_______

* Remove python 2.7 support.

Added
_______

* Lilac backends.

Added
_____

* Python 3.8 tests


[3.5.0] - 2021-02-01
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Added
_____

* Add allowed application in order to avoid the site restrictions when a token is created.

[3.4.1] - 2021-01-26
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Fixed
_____

* Studio error setting.

[3.4.0] - 2021-01-22
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Added
_____

* New oauth2 validator in order to restrict the tokens creation.

[3.3.7] - 2020-12-17
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Fixed
_____

* Changes made in template tags to avoid issues getting site values in an async request.

[3.3.6] - 2020-11-20
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Added
_____

* Add error handler for JSON values in tenant admin.

[3.3.5] - 2020-11-19
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Added
_____

* Support for getting values from SiteConfigurationProxy in juniper.

[3.3.4] - 2020-10-15
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

* Include package data.

[3.3.3] - 2020-10-15
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Added
_____

* Manifest file.


[3.3.2] - 2020-10-14
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Added
_____

* Re add pypi

[3.3.1] - 2020-09-30
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Added
_____

* Django 2.2 tests.

Removed
_______

* django-mysql unnecessary dependency.

[3.3.0] - 2020-09-30
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Added
_____

* Override contentstore SiteConfiguration.
* Use TenantOrganization get_value_for_org method.

Removed
_______

* deprecate_get_value_for_org method


[3.2.0] - 2020-09-28
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Added
_____

* TenantOrganizations

* First release on PyPI.

Removed
_______

* django-mysql JsonFields

[3.0.1] - 2020-07-15
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Added
_____

* Add django-mysql==3.6.0 as a dependency for python 3.5 in order to add  the changes described in `here <https://github.com/adamchainz/django-mysql/blob/master/HISTORY.rst#360-2020-06-09>`_.

[3.0.0] - 2020-07-06
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Added
_____

* Added juniper support

Removed
_______

* Removed hawthorn support

[2.6.0] - 2020-07-02
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Added
_____

* Add tests in python 3.5
* Added command to move SignUpSources from a site to another site.

[2.5.0] - 2020-01-03
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Added
_____

* Add capability to monkey patch a whole djangoapp.

[2.3.0] - 2020-01-03
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Fixed
_____

* Fixed performance issues with GeneratedCertificates proxy.
* Improve performance get_value_for_org.


[2.2.0] - 2019-12-20
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Fixed
_____

* Changes made to not break the edx-platform tests when this plugin is
  installed.

[2.1.0] - 2019-12-19
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Added
_____

* Create proxy for GeneratedCertificates model using monkey patch.

[2.0.0] - 2019-12-19
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Added
_____

* Create a proxy for the edxapp SiteConfiguration model using monkey patch.

Removed
_______

* **BREAKING CHANGE**: Remove usage of edxapp microsite.

[1.3.0] - 2019-12-12
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Added
_____

* Support multitenancy in async process.
