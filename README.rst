
EOX tenant
----------
Eox-tenant is a multi-tenancy django app for `edx-platform`_. It is build as an `openedx plugin`_ so even as a django app it will auto install in the larger edx-platform core code once installed in the same python environment.

The code is written and maintained by `eduNEXT`_ and it is what we use to support our own multi-tenant services. It was initially created as an extension of the `microsites` and `site_configurations` features of the Open edX platform, but it has grown to completely replace them in order to support more robust multi tenancy model.

If you are looking for professional development or support with multi tenancy or multi sites in the Open edX platform, you can reach out at sales@edunext.co

.. _openedx plugin: https://github.com/edx/edx-platform/tree/master/openedx/core/djangoapps/plugins
.. _edx-platform: https://github.com/edx/edx-platform/
.. _eduNEXT: https://www.edunext.co


EOX tenant migration notes
--------------------------

**Migrating from 0.* version to 1.0.0**

From version **1.0.0**\ , middlewares **RedirectionsMiddleware** and **PathRedirectionMiddleware** are not longer supported in this plugin. These middlewares were moved to the **eox-core** plugin `here <https://github.com/eduNEXT/eox-core/>`_. From this, you can have three cases:


#. You have already installed eox-core alongside eox-tenant. In this case you need to:

   * Upgrade eox-core to version **2.0.0** (previous releases are not compatible with eox-tenant 1.0.0)
   * Run the plugin migrations as indicated below:
     .. code-block::

        $ python manage.py lms migrate eox_tenant --settings=<your app settings>
        $ python manage.py lms migrate eox_core --fake-initial --settings=<your app settings>


   #. You only have installed eox-tenant and you want to keep the functionality the aforementioned middlewares offer. You need to:


   * Install eox-core version **2.0.0** as edx-platform requirement. You can use *Ansible* to add this plugin as an extra requirement.


* Run the plugin migrations as indicated below:
  .. code-block::

     $ python manage.py lms migrate eox_tenant --settings=<your app settings>
     $ python manage.py lms migrate eox_core --fake-initial --settings=<your app settings>


#. In the case your are not using the redirection middlewares, and only have eox-tenant installed, you can simply apply the database migrations for the eox-tenant plugin:

.. code-block::

      $ python manage.py lms migrate eox_tenant --settings=<your app settings>

The table corresponding to the Redirection model will not be deleted but it will be discarded from the Django state

Commands
########

Synchronize Organizations
*************************
This comand will synchronize the course_org_filter values in lms_configs(TenantConfig model) or values(Microsite model) with the TenantOrganization registers, if the organization does not existe, it will be create, otherwise it will be add to the organizations model field.


.. code-block:: python

  ./manage.py lms synchronize_organizations  # only for TenantConfig and Microsite
  ./manage.py lms synchronize_organizations --model TenantConfig # only for TenantConfig
  ./manage.py lms synchronize_organizations --model Microsite # only for Microsite

How to Contribute
-----------------

Contributions are welcome! See our `CONTRIBUTING`_ file for more
information – it also contains guidelines for how to maintain high code
quality, which will make your contribution more likely to be accepted.

.. _CONTRIBUTING: https://github.com/eduNEXT/eox-tenant/blob/master/CONTRIBUTING.rst
