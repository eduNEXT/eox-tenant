"""
AWS settings for eox_tenant project.
"""

from .common import * # pylint: disable=wildcard-import


def plugin_settings(settings):
    """
    Set of plugin settings used by the Open Edx platform.
    More info: https://github.com/edx/edx-platform/blob/master/openedx/core/djangoapps/plugins/README.rst
    """
    # Backend settings.
    settings.MICROSITE_BACKEND = getattr(settings, 'ENV_TOKENS', {}).get(
        'MICROSITE_BACKEND',
        settings.MICROSITE_BACKEND
    )
    settings.MICROSITE_TEMPLATE_BACKEND = getattr(settings, 'ENV_TOKENS', {}).get(
        'MICROSITE_TEMPLATE_BACKEND',
        settings.MICROSITE_TEMPLATE_BACKEND
    )
