"""
Template tags and helper functions for displaying breadcrumbs in page titles
based on the current micro site.
"""
from django import template
from django.conf import settings
from django.templatetags.static import static
from django.contrib.staticfiles.storage import staticfiles_storage
from django.utils.translation import get_language_bidi
from eox_tenant.edxapp_wrapper.get_microsite_configuration import get_microsite
from eox_tenant.edxapp_wrapper.branding_api import get_branding_api
from eox_tenant.edxapp_wrapper.configuration_helpers import get_configuration_helpers

microsite = get_microsite()  # pylint: disable=invalid-name
configuration_helpers = get_configuration_helpers()
branding_api = get_branding_api()

register = template.Library()  # pylint: disable=invalid-name


@register.simple_tag(name="favicon_path")
def favicon_path(default=getattr(settings, 'FAVICON_PATH', 'images/favicon.ico')):
    """
    Django template tag that outputs the configured favicon:
    {% favicon_path %}
    """
    path = microsite.get_value('favicon_path', default)
    return path if path.startswith("http") else staticfiles_storage.url(path)


@register.simple_tag(name="microsite_css_overrides_file")
def microsite_css_overrides_file():
    """
    Django template tag that outputs the css import for a:
    {% microsite_css_overrides_file %}
    """
    file_path = microsite.get_value('css_overrides_file', None)
    if get_language_bidi():
        file_path = microsite.get_value(
            'css_overrides_file_rtl',
            microsite.get_value('css_overrides_file')
        )
    else:
        file_path = microsite.get_value('css_overrides_file')

    if file_path is not None:
        return "<link href='{}' rel='stylesheet' type='text/css'>".format(static(file_path))
    else:
        return ""


@register.simple_tag(name="microsite_rtl")
def microsite_rtl_tag():
    """
    Django template tag that outputs the direction string for rtl support
    """
    return 'rtl' if get_language_bidi() else 'ltr'


@register.filter
def microsite_template_path(template_name):
    """
    Django template filter to apply template overriding to microsites
    """
    return microsite.get_template_path(template_name)


@register.filter
def microsite_get_value(value, default=None):
    """
    Django template filter that wrapps the microsite.get_value function
    """
    return microsite.get_value(value, default)


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
