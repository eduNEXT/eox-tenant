"""
File configuration for eox-tenant.
"""
from django.apps import AppConfig
from django.conf import settings as base_settings

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

        if base_settings.EOX_TENANT_CHANGE_ENROLLMENT_MANAGER:
            from eox_tenant.edxapp_wrapper.enrollments import get_enrollments_model
            from eox_tenant.models import EdnxCourseEnrollmentManager
            enrollments = get_enrollments_model()
            enrollments.objects = EdnxCourseEnrollmentManager()
