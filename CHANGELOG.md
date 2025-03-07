## v7.1.1 - 2025-03-30

## [v7.1.1](https://github.com/eduNEXT/eox-tenant/compare/v7.0.0...v7.0.1) - (2025-03-30)

### Features
- **API:** Added `update-by-domain` action in `TenantConfigViewSet` to allow updates using `route__domain` as a lookup field. This enhances flexibility for scenarios where only the domain is known.

### Improvements
- **Validation:** Enforced dictionary validation for `lms_configs`, `studio_configs`, `theming_configs`, and `meta` fields in `TenantConfigSerializer`. These fields now strictly accept only dictionary values, preventing unexpected data types.
- Fixes issue with login not being tenant-aware.

## v7.0.0 - 2022-12-19

### [7.0.0](https://github.com/eduNEXT/eox-tenant/compare/v6.3.0...v7.0.0) (2022-12-19)

#### ⚠ BREAKING CHANGES

- drop unnecessary certificate proxy
- 
- feat: add pipeline step that filter render certificates by organization
- 
- refactor: drop unnecessary backend
- 
- fix: fix quality tests
- 

#### Performance Improvements

- filter certificates by org and remove certificate proxy ([#157](https://github.com/eduNEXT/eox-tenant/issues/157)) ([773ac40](https://github.com/eduNEXT/eox-tenant/commit/773ac4046dc5913efee7cc247985a3625a0cdb64))

#### Continuous Integration

- update the changelog updater step in bumpversion ([c45c3e6](https://github.com/eduNEXT/eox-tenant/commit/c45c3e68aedbc94a997806353571b081847904b2))

## v6.3.0 - 2022-11-22

### [6.3.0](https://github.com/eduNEXT/eox-tenant/compare/v6.2.0...v6.3.0) (2022-11-22)

#### Features

- filter user's course enrollment by microsite request ([a8f445d](https://github.com/eduNEXT/eox-tenant/commit/a8f445d3ade47bd049e53115f17f3a3ca441138a))

#### Tests

- add test to custom filter pipeline ([948e455](https://github.com/eduNEXT/eox-tenant/commit/948e45560a3aef0255c408cb9dd3472b031f03e4))

#### Documentation

- add readme filter steps file ([f759510](https://github.com/eduNEXT/eox-tenant/commit/f7595106221d67ed895f33c42c6bd7205fca7f0b))
- update README file ([f0fb19c](https://github.com/eduNEXT/eox-tenant/commit/f0fb19cb3442ae37861e5b302ae6459c24af0321))

#### Continuous Integration

- add workflow to publish python package ([38dd118](https://github.com/eduNEXT/eox-tenant/commit/38dd118e863ff2efb343ff76455528151eb48842))
- drop circleci file ([dcbc494](https://github.com/eduNEXT/eox-tenant/commit/dcbc49437a668038221c3ca6911a35b1b151856f))

## v6.2.0 - 2022-09-20

### [6.2.0](https://github.com/eduNEXT/eox-tenant/compare/v6.1.0...v6.2.0) (2022-09-20)

#### Features

- add extra lookup_field to Microsite and TenantConfig viewsets ([d1c8962](https://github.com/eduNEXT/eox-tenant/commit/d1c89622b90eb1ff739e8e12e0b7db9b28c5eb62))

## v6.1.0 - 2022-09-20

### [6.1.0](https://github.com/eduNEXT/eox-tenant/compare/v6.0.2...v6.1.0) (2022-09-20)

#### Features

- add BearerAuthentication to API and improve EoxTenantAPIPermission checks ([#149](https://github.com/eduNEXT/eox-tenant/issues/149)) ([e8803ea](https://github.com/eduNEXT/eox-tenant/commit/e8803eac29636bf8058d768142b582baf87aa381))

## v6.0.2 - 2022-09-01

### [6.0.2](https://github.com/eduNEXT/eox-tenant/compare/v6.0.1...v6.0.2) (2022-09-01)

### Bug Fixes

- Use get_current_site_orgs instead of get_value ([360abce](https://github.com/eduNEXT/eox-tenant/commit/360abce04a0ea89722cc9d64a5954698e70b00f1))

### Continuous Integration

- add ci pipelines ([#152](https://github.com/eduNEXT/eox-tenant/issues/152)) ([708a248](https://github.com/eduNEXT/eox-tenant/commit/708a2481268d50171e7bbfc69858be73b6eca76b))

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
- to avoid an exception while sending emails.

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
- 
- First release on PyPI.
- 

### Removed

- django-mysql JsonFields

## [3.0.1] - 2020-07-15

### Features

- Add django-mysql==3.6.0 as a dependency for python 3.5 in order to add  the changes described in `here <https://github.com/adamchainz/django-mysql/blob/master/HISTORY.rst#360-2020-06-09>`_.

## [3.0.0] - 2020-07-06

### Features

- ### Features juniper support
- 
- 
- 
- 
- 

### Removed

- ### Removed hawthorn support
- 
- 
- 
- 
- 

## [2.6.0] - 2020-07-02

### Features

- Add tests in python 3.5
- ### Features command to move SignUpSources from a site to another site.
- 
- 
- 
- 
- 

## [2.5.0] - 2020-01-03

### Features

- Add capability to monkey patch a whole djangoapp.

## [2.3.0] - 2020-01-03~

### Fixed

- ### Fixed performance issues with GeneratedCertificates proxy.
- 
- 
- 
- 
- 
- Improve performance get_value_for_org.

## [2.2.0] - 2019-12-20~~

### Fixed

- Changes made to not break the edx-platform tests when this plugin is
- installed.

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
