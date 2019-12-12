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

    plugin_app = {
        'settings_config': {
            'lms.djangoapp': {
                'test': {'relative_path': 'settings.test'},
                'common': {'relative_path': 'settings.common'},
                'aws': {'relative_path': 'settings.aws'},
            },
            'cms.djangoapp': {
                'test': {'relative_path': 'settings.test'},
                'common': {'relative_path': 'settings.common'},
                'aws': {'relative_path': 'settings.aws'},
            },
        },
        'signals_config': {
            'lms.djangoapp': {
                'relative_path': 'signals',
                'receivers': [
                    {
                        'receiver_func_name': 'start_tenant',
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
                        'receiver_func_name': 'start_async_tenant',
                        'signal_path': 'celery.signals.task_prerun',
                    },
                ],
            }
        },
    }

    def ready(self):
        """
        Method to perform actions after apps registry is ended
        """
        from eox_tenant.permissions import load_permissions
        load_permissions()

        from eox_tenant.monkey_patch import load_monkey_patchs_overrides
        load_monkey_patchs_overrides()
