"""
File configuration for eox-tenant.
"""
from django.apps import AppConfig

class EdunextOpenEdxExtensionsConfig(AppConfig):
    """
    """
    name = 'eox_tenant'
    verbose_name = "Edunext Open edx extensions tenant."

    plugin_app = {
        'settings_config': {
            'lms.djangoapp': {},
            'cms.djangoapp': {},
        },
    }
