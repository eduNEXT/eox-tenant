## [6.0.1] - 2022-08-17

### Features

- add support for Nutmeg release
- update django requirement

## [6.0.0] - 2022-03-07

### Changed

- **BREAKING CHANGE**: remove the Course Management feature
- **BREAKING CHANGE**: django32: Drop python 3.5 support in favor of python 3.8.

### Performance Improvements

- django32: add compatibility with openedx maple release
- change code to pass tests

### Continuous Integration

- add test actions to github workflows

### Code Refactoring

- change function format by an f-string

## [5.1.3] - 2022-01-14

### Fixed

- Update backend for edxmako so it's lilac compatible.

## [5.1.2] - 2021-12-02

### Fixed

- TenantSiteConfigProxy.site_values returns a serializable subset of settings
  to avoid an exception while sending emails.


## [5.1.1] - 2021-11-29


### Fixed

- UserSignupSource import in order to avoid raising an exception when running tests.

## [5.1.0] - 2021-11-22


### Features

- Support for message passing via protocol V2

## [5.0.1] - 2021-10-29


### Fixed

- Changed OAUTH2_PROVIDER test setting for the CMS

## [5.0.0] - 2021-10-29


### Fixed

- Changed OAUTH2_PROVIDER test setting to the platform value

### Changed

- **BREAKING CHANGE**: Default backends for edxapp users and branding_api are not compatible with Juniper.

## [4.1.0] - 2021-10-27

### Features

- Set Lilac backends as default in the Common settings file.
- Update readme with new information and formats.


## [4.0.0] - 2021-05-10

### Removed

- Remove python 2.7 support.

### Features

- Lilac backends.

### Features

- Python 3.8 tests


## [3.5.0] - 2021-02-01

### Features

- Add allowed application in order to avoid the site restrictions when a token is created.

## [3.4.1] - 2021-01-26

### Fixed

- Studio error setting.

## [3.4.0] - 2021-01-22

### Features

- New oauth2 validator in order to restrict the tokens creation.

## [3.3.7] - 2020-12-17

### Fixed

- Changes made in template tags to avoid issues getting site values in an async request.

## [3.3.6] - 2020-11-20

### Features

- Add error handler for JSON values in tenant admin.

## [3.3.5] - 2020-11-19

### Features

- Support for getting values from SiteConfigurationProxy in juniper.

## [3.3.4] - 2020-10-15

- Include package data.

## [3.3.3] - 2020-10-15

### Features

- Manifest file.


## [3.3.2] - 2020-10-14

### Features

- Re add pypi

## [3.3.1] - 2020-09-30

### Features

- Django 2.2 tests.

### Removed

- django-mysql unnecessary dependency.

## [3.3.0] - 2020-09-30

### Features

- Override contentstore SiteConfiguration.
- Use TenantOrganization get_value_for_org method.

### Removed

- deprecate_get_value_for_org method


## [3.2.0] - 2020-09-28

### Features

- TenantOrganizations

- First release on PyPI.

### Removed

- django-mysql JsonFields

## [3.0.1] - 2020-07-15

### Features

- Add django-mysql==3.6.0 as a dependency for python 3.5 in order to add  the changes described in `here <https://github.com/adamchainz/django-mysql/blob/master/HISTORY.rst#360-2020-06-09>`_.

## [3.0.0] - 2020-07-06

### Features

- ### Features juniper support

### Removed

- ### Removed hawthorn support

## [2.6.0] - 2020-07-02

### Features

- Add tests in python 3.5
- ### Features command to move SignUpSources from a site to another site.

## [2.5.0] - 2020-01-03

### Features

- Add capability to monkey patch a whole djangoapp.

## [2.3.0] - 2020-01-03~

### Fixed

- ### Fixed performance issues with GeneratedCertificates proxy.
- Improve performance get_value_for_org.


## [2.2.0] - 2019-12-20~~

### Fixed

- Changes made to not break the edx-platform tests when this plugin is
  installed.

## [2.1.0] - 2019-12-19~~

### Features

- Create proxy for GeneratedCertificates model using monkey patch.

## [2.0.0] - 2019-12-19


### Features

- Create a proxy for the edxapp SiteConfiguration model using monkey patch.

### Removed

- **BREAKING CHANGE**: Remove usage of edxapp microsite.

## [1.3.0] - 2019-12-12


### Features

- Support multitenancy in async process.
