==========
EOX tenant
==========
|Maintainance Badge| |Test Badge| |PyPI Badge|

.. |Maintainance Badge| image:: https://img.shields.io/badge/Status-Maintained-brightgreen
   :alt: Maintainance Status
.. |Test Badge| image:: https://img.shields.io/github/actions/workflow/status/edunext/eox-tenant/.github%2Fworkflows%2Ftests.yml?label=Test
   :alt: GitHub Actions Workflow Test Status
.. |PyPI Badge| image:: https://img.shields.io/pypi/v/eox-tenant?label=PyPI
   :alt: PyPI - Version
   
Eox-tenant is a multi-tenancy Django app for `edx-platform`_. It is built as an `openedx plugin`_ so even as a Django app it will be auto-installed in the larger edx-platform core code once is installed in the same Python environment.

The code is written and maintained by `edunext`_ and we use it to support our multi-tenant services. It was initially created as an extension of the `microsites` and `site_configurations` features of the Open edX platform, however, it has grown to completely replace them to support a more robust multitenancy model.

If you are looking for professional development or support with multitenancy or multi-sites in the Open edX platform, you can reach out to sales@edunext.co

.. _openedx plugin: https://github.com/edx/edx-platform/tree/master/openedx/core/djangoapps/plugins
.. _edx-platform: https://github.com/edx/edx-platform/
.. _eduNEXT: https://www.edunext.co

Installation
============

#. Add this plugin in your Tutor ``config.yml`` with the ``OPENEDX_EXTRA_PIP_REQUIREMENTS`` setting.

   .. code-block:: yaml
      
      OPENEDX_EXTRA_PIP_REQUIREMENTS:
         - eox-tenant=={{version}}
         
#. Save the configuration with ``tutor config save``.
#. Build an open edx image with ``tutor images build openedx``.
#. Launch your platform with ``tutor local launch``.

Usage
=====

Once your instance is running, you can access the Django admin site and locate the ``EDUNEXT OPENEDX MULTITENANCY`` models.

- **Microsites:** Store the microsite configuration.
- **Routes:** Configure the URL for a tenant.
- **Tenant configs:** Store the configuration for each tenant.
- **Tenant organizations:** Link each organization with one or multiple tenants.

Add ``EDNX_USE_SIGNAL = True`` in each microsite/tenant that wants to use the plugin. 
 
Compatibility Notes
--------------------

+------------------+-----------------------+
| Open edX Release | Version               |
+==================+=======================+
| Ironwood         | < 3.0                 |
+------------------+-----------------------+
| Juniper          | >= 3.0 < 4.0          |
+------------------+-----------------------+
| Koa              | >= 4.0 <= 5.1.3       |
+------------------+-----------------------+
| Lilac            | >= 4.0 < 6.2          |
+------------------+-----------------------+
| Maple            | >= 6.0                |
+------------------+-----------------------+
| Nutmeg           | >= 6.2                |
+------------------+-----------------------+
| Olive            | >= 8.0                |
+------------------+-----------------------+
| Palm             | >= v11.7.0            |
+------------------+-----------------------+
| Quince           | >= v11.7.0            |
+------------------+-----------------------+
| Redwood          | >= v11.7.0            |
+------------------+-----------------------+

**NOTE**: Since the 6.2 version, eox-tenant does not support Django 2.2

The plugin is configured for the latest release (Quince). The following changes in the plugin settings should be applied to be used for previous releases.

If the release you are looking for is not listed, the actual configuration is sufficient or it is incompatible with the current eox-tenant version.

**Maple**

For version  11.X compatible

.. code-block:: yaml

  EOX_TENANT_EDX_AUTH_BACKEND = "eox_tenant.edxapp_wrapper.backends.edx_auth_i_v1"

Those settings can be changed in ``eox_tenant/settings/common.py`` or, for example, in ansible configurations.

**NOTE**

For version > 10.0.0 you need to enable eox-tenant adding in the LMS configuration:
 
.. code-block:: yaml
  
  USE_EOX_TENANT = True

Commands
--------
Synchronize Organizations
^^^^^^^^^^^^^^^^^^^^^^^^^
This command will synchronize the course_org_filter values in lms_configs(TenantConfig model) or values(Microsite model) with the TenantOrganization registers if the organization does not exist, it will be created, otherwise, it will be added to the organizations model field.


.. code-block:: bash

  ./manage.py lms synchronize_organizations  # only for TenantConfig and Microsite
  ./manage.py lms synchronize_organizations --model TenantConfig # only for TenantConfig
  ./manage.py lms synchronize_organizations --model Microsite # only for Microsite

Create/Edit tenant configuration
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
`create_or_update_tenant_config` helps to add or edit ``TenantConfig`` and linked ``Routes`` via command line.

.. code-block:: bash

  # This command will create/edit an entry in TenantConfig with external_key lacolhost.com and update its JSONField(s) with passed JSON content.
  ./manage.py lms create_or_update_tenant_config --external-key lacolhost.com --config '{"lms_configs": {"PLATFORM_NAME": "Lacolhost"}, "studio_configs": {"PLATFORM_NAME": "Lacolhost"}}' lacolhost.com studio.lacolhost.com preview.lacolhost.com

  # This command will create/edit an entry in TenantConfig with external_key lacolhost.com and update its JSONField(s) with passed JSON config file content.
  ./manage.py lms create_or_update_tenant_config --external-key lacolhost.com --config-file /tmp/some.json lacolhost.com studio.lacolhost.com preview.lacolhost.com

  # Same as above, but it will override configuration instead of updating it.
  ./manage.py lms create_or_update_tenant_config --external-key lacolhost.com --config-file /tmp/some.json lacolhost.com studio.lacolhost.com preview.lacolhost.com --override


Migration notes
===============

**Migrating from 0.* version to 1.0.0**

From version **1.0.0**, middlewares **RedirectionsMiddleware** and **PathRedirectionMiddleware** are no longer supported in this plugin. These middlewares were moved to the **eox-core** plugin `here <https://github.com/eduNEXT/eox-core/>`_. From this, you can have three cases:


#. You have already installed eox-core alongside eox-tenant. In this case, you need to:

   * Upgrade eox-core to version **2.0.0** (previous releases are not compatible with eox-tenant 1.0.0)
   * Run the plugin migrations as indicated below:

   .. code-block:: bash

     ./manage.py lms migrate eox_tenant --settings=<your app settings>
     ./manage.py lms migrate eox_core --fake-initial --settings=<your app settings>


#. You only have installed eox-tenant and you want to keep the functionality that middlewares offer. You need to:

   * Install eox-core version **2.0.0** as edx-platform requirement. You can use *Ansible* to add this plugin as an extra requirement.

   * Run the plugin migrations as indicated below:

   .. code-block:: bash

     ./manage.py lms migrate eox_tenant --settings=<your app settings>
     ./manage.py manage.py lms migrate eox_core --fake-initial --settings=<your app settings>


#. In the case you are not using the redirection middlewares, and only have eox-tenant installed, you can simply apply the database migrations for the eox-tenant plugin:

   .. code-block:: bash

     ./manage.py manage.py lms migrate eox_tenant --settings=<your app settings>

   The table corresponding to the Redirection model will not be deleted but it will be discarded from the Django state


Caveats
-------

- SSO that uses the LMS while authenticating does so with server-to-server communication. Therefore, when the `AvailableScreenMiddleware` gets the current domain, it finds that `lms:8000` as in `SOCIAL_AUTH_EDX_OAUTH2_URL_ROOT` which does not exist, then raises a 404 exception. To avoid this error, set in your LMS settings file:

.. code-block:: python

  SOCIAL_AUTH_EDX_OAUTH2_URL_ROOT = SOCIAL_AUTH_EDX_OAUTH2_PUBLIC_URL_ROOT

How to Contribute
=================

Contributions are welcome! See our `CONTRIBUTING`_ file for more
information – it also contains guidelines for how to maintain high code
quality, which will make your contribution more likely to be accepted.

.. _CONTRIBUTING: https://github.com/eduNEXT/eox-tenant/blob/master/CONTRIBUTING.rst

License
=======

This project is licensed under the AGPL-3.0 License. See the LICENSE file for details.
