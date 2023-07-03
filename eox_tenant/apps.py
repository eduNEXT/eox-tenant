"""
File configuration for eox-tenant.
"""
from django.apps import AppConfig


class EdunextOpenedxExtensionsTenantConfig(AppConfig):
    """
    App configuration
    """
    name = 'eox_tenant'
    verbose_name = "Edunext Openedx Multitenancy."
    default = False

    plugin_app = {
        'url_config': {
            'lms.djangoapp': {
                'namespace': 'eox-tenant',
                'regex': r'^eox-tenant/',
                'relative_path': 'urls',
            },
        },
        'settings_config': {
            'lms.djangoapp': {
                'test': {'relative_path': 'settings.test'},
                'common': {'relative_path': 'settings.common'},
                'production': {'relative_path': 'settings.production'},
            },
            'cms.djangoapp': {
                'test': {'relative_path': 'settings.test'},
                'common': {'relative_path': 'settings.common'},
                'production': {'relative_path': 'settings.production'},
            },
        },
        'signals_config': {
            'lms.djangoapp': {
                'relative_path': 'signals',
                'receivers': [
                    {
                        'receiver_func_name': 'start_lms_tenant',
                        'signal_path': 'django.core.signals.request_started',
                    },
                    {
                        'receiver_func_name': 'finish_tenant',
                        'signal_path': 'django.core.signals.request_finished',
                    },
                    {
                        'receiver_func_name': 'clear_tenant',
                        'signal_path': 'django.core.signals.got_request_exception',
                    },
                    {
                        'receiver_func_name': 'tenant_context_addition',
                        'signal_path': 'celery.signals.before_task_publish',
                    },
                    {
                        'receiver_func_name': 'start_async_lms_tenant',
                        'signal_path': 'celery.signals.task_prerun',
                    },
                    {
                        'receiver_func_name': 'update_tenant_organizations',
                        'signal_path': 'django.db.models.signals.post_save',
                        'dispatch_uid': 'update_tenant_organizations_receiver',
                        'sender_path': 'eox_tenant.models.TenantConfig',
                    },
                    {
                        'receiver_func_name': 'update_tenant_organizations',
                        'signal_path': 'django.db.models.signals.post_save',
                        'dispatch_uid': 'update_tenant_organizations_receiver',
                        'sender_path': 'eox_tenant.models.Microsite',
                    },
                ],
            },
            'cms.djangoapp': {
                'relative_path': 'signals',
                'receivers': [
                    {
                        'receiver_func_name': 'start_studio_tenant',
                        'signal_path': 'django.core.signals.request_started',
                    },
                    {
                        'receiver_func_name': 'tenant_context_addition',
                        'signal_path': 'celery.signals.before_task_publish',
                    },
                    {
                        'receiver_func_name': 'start_async_studio_tenant',
                        'signal_path': 'celery.signals.task_prerun',
                    },
                ],
            },
        },
    }

    def ready(self):
        """
        Method to perform actions after apps registry is ended
        """
        from eox_tenant.api.v1.permissions import \
            load_permissions as load_api_permissions  # pylint: disable=import-outside-toplevel
        load_api_permissions()

        from eox_tenant.permissions import load_permissions  # pylint: disable=import-outside-toplevel
        load_permissions()

        from eox_tenant.tenant_wise import load_tenant_wise_overrides  # pylint: disable=import-outside-toplevel
        load_tenant_wise_overrides()
