
EOX tenant
----------
Eox-tenant is a multi-tenancy django app for `edx-platform`_. It is build as an `openedx plugin`_ so even as a django app it will auto install in the larger edx-platform core code once installed in the same python environment.

The code is written and maintained by `eduNEXT`_ and it is what we use to support our own multi-tenant services. It was initially created as an extension of the `microsites` and `site_configurations` features of the Open edX platform, but it has grown to completely replace them in order to support more robust multi tenancy model.

If you are looking for professional development or support with multi tenancy or multi sites in the Open edX platform, you can reach out at sales@edunext.co

.. _openedx plugin: https://github.com/edx/edx-platform/tree/master/openedx/core/djangoapps/plugins
.. _edx-platform: https://github.com/edx/edx-platform/
.. _eduNEXT: https://www.edunext.co

Compatibility Notes
--------------------

+-------------------+-----------------------+
| Open edX Release  |         Version       |
+===================+=======================+
|      Ironwood     |          < 3.0        |
+-------------------+-----------------------+
|       Juniper     |       >= 3.0 < 4.0    |
+-------------------+-----------------------+
|        Koa        |     >= 4.0 <= 5.1.3   |
+-------------------+-----------------------+
|       Lilac       |     >= 4.0 < 6.2      |
+-------------------+-----------------------+
|       Maple       |         >= 6.0        |
+-------------------+-----------------------+
|      Nutmeg       |         >= 6.2        |
+-------------------+-----------------------+
|       Olive       |         >= 8.0        |
+-------------------+-----------------------+
|       Palm        |         >=v10.0.0     |
+-------------------+-----------------------+

**NOTE**: Since 6.2 version, eox-tenant does not support Django 2.2

The following changes to the plugin settings are necessary. If the release you are looking for is
not listed, then the accumulation of changes from previous releases is enough.

**Ironwood**

.. code-block:: yaml

  GET_BRANDING_API: 'eox_tenant.edxapp_wrapper.backends.branding_api_h_v1'
  GET_CERTIFICATES_MODULE: 'eox_tenant.edxapp_wrapper.backends.certificates_module_i_v1'
  GET_SITE_CONFIGURATION_MODULE: 'eox_tenant.edxapp_wrapper.backends.site_configuration_module_i_v1'
  GET_THEMING_HELPERS: 'eox_tenant.edxapp_wrapper.backends.theming_helpers_h_v1'
  EOX_TENANT_EDX_AUTH_BACKEND: "eox_tenant.edxapp_wrapper.backends.edx_auth_i_v1"
  EOX_TENANT_USERS_BACKEND: 'eox_tenant.edxapp_wrapper.backends.users_i_v1'
  EDXMAKO_MODULE_BACKEND: 'eox_tenant.edxapp_wrapper.backends.edxmako_h_v1'
  UTILS_MODULE_BACKEND: 'eox_tenant.edxapp_wrapper.backends.util_h_v1'

**Juniper**

For version >= 3.4

.. code-block:: yaml

  GET_OAUTH_DISPATCH_BACKEND: 'eox_tenant.edxapp_wrapper.backends.oauth_dispatch_j_v1'

**Koa (optional)**

.. code-block:: yaml

  GET_BRANDING_API: 'eox_tenant.edxapp_wrapper.backends.branding_api_l_v1'
  EOX_TENANT_USERS_BACKEND: 'eox_tenant.edxapp_wrapper.backends.users_l_v1'
  EDXMAKO_MODULE_BACKEND: eox_tenant.edxapp_wrapper.backends.edxmako_l_v1

**Lilac**

.. code-block:: yaml

  GET_BRANDING_API: 'eox_tenant.edxapp_wrapper.backends.branding_api_l_v1'
  EOX_TENANT_USERS_BACKEND: 'eox_tenant.edxapp_wrapper.backends.users_l_v1'
  EDXMAKO_MODULE_BACKEND: eox_tenant.edxapp_wrapper.backends.edxmako_l_v1

**Maple**

.. code-block:: yaml

  GET_BRANDING_API: 'eox_tenant.edxapp_wrapper.backends.branding_api_l_v1'
  EOX_TENANT_USERS_BACKEND: 'eox_tenant.edxapp_wrapper.backends.users_l_v1'
  EDXMAKO_MODULE_BACKEND: eox_tenant.edxapp_wrapper.backends.edxmako_l_v1

Those settings can be changed in ``eox_tenant/settings/common.py`` or, for example, in ansible configurations.

**NOTE**: the current ``common.py`` works with Open edX juniper version.

Migration notes
---------------

**Migrating from 0.* version to 1.0.0**

From version **1.0.0**\ , middlewares **RedirectionsMiddleware** and **PathRedirectionMiddleware** are not longer supported in this plugin.These middlewares were moved to the **eox-core** plugin `here <https://github.com/eduNEXT/eox-core/>`_. From this, you can have three cases:


#. You have already installed eox-core alongside eox-tenant. In this case you need to:

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


#. In the case your are not using the redirection middlewares, and only have eox-tenant installed, you can simply apply the database migrations for the eox-tenant plugin:

   .. code-block:: bash

     ./manage.py manage.py lms migrate eox_tenant --settings=<your app settings>

   The table corresponding to the Redirection model will not be deleted but it will be discarded from the Django state

Commands
########

Synchronize Organizations
*************************
This command will synchronize the course_org_filter values in lms_configs(TenantConfig model) or values(Microsite model) with the TenantOrganization registers, if the organization does not exist, it will be created, otherwise it will be add to the organizations model field.


.. code-block:: bash

  ./manage.py lms synchronize_organizations  # only for TenantConfig and Microsite
  ./manage.py lms synchronize_organizations --model TenantConfig # only for TenantConfig
  ./manage.py lms synchronize_organizations --model Microsite # only for Microsite

Create/Edit tenant configuration
********************************
`create_or_update_tenant_config` helps to add or edit ``TenantConfig`` and linked ``Routes`` via command line.

.. code-block:: bash

  # this command will create/edit entry in TenantConfig with external_key lacolhost.com and update its JSONField(s) with passed json content.
  ./manage.py lms create_or_update_tenant_config --external-key lacolhost.com --config '{"lms_configs": {"PLATFORM_NAME": "Lacolhost"}, "studio_configs": {"PLATFORM_NAME": "Lacolhost"}}' lacolhost.com studio.lacolhost.com preview.lacolhost.com

  # this command will create/edit entry in TenantConfig with external_key lacolhost.com and update its JSONField(s) with passed json config file content.
  ./manage.py lms create_or_update_tenant_config --external-key lacolhost.com --config-file /tmp/some.json lacolhost.com studio.lacolhost.com preview.lacolhost.com

  # Same as above, but it will override configuration instead of updating it.
  ./manage.py lms create_or_update_tenant_config --external-key lacolhost.com --config-file /tmp/some.json lacolhost.com studio.lacolhost.com preview.lacolhost.com --override

Caveats
-------

- SSO that uses the LMS while authenticating does so with server-to-server communication. Therefore, when the `AvailableScreenMiddleware` gets the current domain, it finds that `lms:8000` as in `SOCIAL_AUTH_EDX_OAUTH2_URL_ROOT` which does not exist, then raises 404 exception. In order to avoid this error, set in your LMS settings file:

.. code-block:: python

  SOCIAL_AUTH_EDX_OAUTH2_URL_ROOT = SOCIAL_AUTH_EDX_OAUTH2_PUBLIC_URL_ROOT

How to Contribute
-----------------

Contributions are welcome! See our `CONTRIBUTING`_ file for more
information – it also contains guidelines for how to maintain high code
quality, which will make your contribution more likely to be accepted.

.. _CONTRIBUTING: https://github.com/eduNEXT/eox-tenant/blob/master/CONTRIBUTING.rst
