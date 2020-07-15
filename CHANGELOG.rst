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

*

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
