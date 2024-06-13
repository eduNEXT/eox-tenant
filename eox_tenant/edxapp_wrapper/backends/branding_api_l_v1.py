"""Lilac backend branding module."""
try:
    from lms.djangoapps.branding import api as branding_api
except ImportError:
    branding_api = object   # pylint: disable=invalid-name


def get_branding_api():
    """Allow to get the branding api module
    https://github.com/openedx/edx-platform/blob/open-release/lilac.master/lms/djangoapps/branding/api.py

    Returns:
        branding_api module.
    """
    return branding_api
