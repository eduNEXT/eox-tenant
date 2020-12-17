"""
Template tags and helper functions for displaying breadcrumbs in page titles
based on the current micro site.
"""
import warnings

from django import template
from django.conf import settings
from django.contrib.staticfiles.storage import staticfiles_storage
from django.templatetags.static import static
from django.utils.translation import get_language_bidi

from eox_tenant.edxapp_wrapper.branding_api import get_branding_api
from eox_tenant.edxapp_wrapper.site_configuration_module import get_configuration_helpers
from eox_tenant.edxapp_wrapper.theming_helpers import get_theming_helpers

configuration_helpers = get_configuration_helpers()
branding_api = get_branding_api()
theming_helpers = get_theming_helpers()

register = template.Library()  # pylint: disable=invalid-name


@register.simple_tag(name="favicon_path")
def favicon_path(default=getattr(settings, 'FAVICON_PATH', 'images/favicon.ico')):
    """
    Django template tag that outputs the configured favicon:
    {% favicon_path %}
    """
    path = configuration_helpers.get_value('favicon_path', default)
    return path if path.startswith("http") else staticfiles_storage.url(path)


@register.simple_tag(name="microsite_css_overrides_file")
def microsite_css_overrides_file():
    """
    Django template tag that outputs the css import for a:
    {% microsite_css_overrides_file %}
    DEPRECATED: use tenant_css_overrides_file tag instead
    """
    warnings.warn(
        "microsite_css_overrides_file, use tenant_css_overrides_file tag instead.",
        DeprecationWarning
    )

    if get_language_bidi():
        file_path = configuration_helpers.get_value(
            'css_overrides_file_rtl',
            configuration_helpers.get_value('css_overrides_file')
        )
    else:
        file_path = configuration_helpers.get_value('css_overrides_file')

    if file_path is not None:
        return "<link href='{}' rel='stylesheet' type='text/css'>".format(static(file_path))
    else:
        return ""


@register.simple_tag(name="microsite_rtl")
def microsite_rtl_tag():
    """
    Django template tag that outputs the direction string for rtl support
    DEPRECATED: use tenant_rtl_tag tag instead
    """
    warnings.warn(
        "microsite_rtl_tag, use tenant_rtl_tag tag instead.",
        DeprecationWarning
    )

    return 'rtl' if get_language_bidi() else 'ltr'


@register.filter
def microsite_template_path(template_name):
    """
    Django template filter to apply template overriding to microsites
    DEPRECATED: use tenant_template_path filter instead
    """
    warnings.warn(
        "microsite_template_path, use tenant_template_path filter instead.",
        DeprecationWarning
    )

    return theming_helpers.get_template_path(template_name)


@register.simple_tag
def microsite_get_value(value, *args, **kwargs):  # pylint: disable=unused-argument
    """
    Django template filter that wraps the configuration_helpers.get_value function
    DEPRECATED: use tenant_get_value tag instead
    """
    warnings.warn(
        "microsite_get_value, use tenant_get_value tag instead.",
        DeprecationWarning
    )

    return tenant_get_value(value, *args, **kwargs)


@register.simple_tag
def branding_api_get_logo_url(is_secure=True):
    """
    Branding template tag
    """
    return branding_api.get_logo_url(is_secure)


@register.simple_tag
def branding_get_configuration_url(name):
    """
    Branding template tag
    """
    return branding_api.get_configuration_url(name)


@register.simple_tag
def branding_get_url(name):
    """
    Branding template tag
    """
    return branding_api.get_url(name)


@register.simple_tag
def branding_get_base_url(is_secure):
    """
    Branding template tag
    """
    return branding_api.get_base_url(is_secure)


@register.simple_tag
def branding_get_tos_and_honor_code_url():
    """
    Branding template tag
    """
    return branding_api.get_tos_and_honor_code_url()


@register.simple_tag
def branding_get_privacy_url():
    """
    Branding template tag
    """
    return branding_api.get_privacy_url()


@register.simple_tag
def branding_get_about_url():
    """
    Branding template tag
    """
    return branding_api.get_about_url()


@register.simple_tag
def get_lms_root_url():
    """
    Branding template tag
    """
    return configuration_helpers.get_value('LMS_ROOT_URL', settings.LMS_ROOT_URL)


@register.simple_tag
def get_platform_name():
    """
    Branding template tag
    """
    return configuration_helpers.get_value('platform_name', settings.PLATFORM_NAME)


@register.simple_tag
def get_login_link():
    """
    Get loging link
    """
    if settings.FEATURES.get('ednx_custom_login_link'):
        return settings.FEATURES.get('ednx_custom_login_link')
    else:
        return get_lms_root_url() + "/login"


@register.simple_tag(name="tenant_css_overrides_file")
def tenant_css_overrides_file():
    """
    Django template tag that outputs the css import for a:
    {% tenant_css_overrides_file %}
    """
    if get_language_bidi():
        file_path = configuration_helpers.get_value(
            'css_overrides_file_rtl',
            configuration_helpers.get_value('css_overrides_file')
        )
    else:
        file_path = configuration_helpers.get_value('css_overrides_file')

    if file_path is not None:
        return "<link href='{}' rel='stylesheet' type='text/css'>".format(static(file_path))
    else:
        return ""


@register.simple_tag(name="tenant_rtl")
def tenant_rtl_tag():
    """
    Django template tag that outputs the direction string for rtl support
    """
    return 'rtl' if get_language_bidi() else 'ltr'


@register.filter
def tenant_template_path(template_name):
    """
    Django template filter to apply template overriding to microsites
    """
    return theming_helpers.get_template_path(template_name)


@register.simple_tag
def tenant_get_value(value, *args, **kwargs):  # pylint: disable=unused-argument
    """
    Django template filter that wraps the configuration_helpers.get_value function
    """
    default = kwargs.get('default', None)
    return configuration_helpers.get_value(value, getattr(settings, value, default))
