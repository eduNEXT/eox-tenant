"""
DarkLangMiddleware Backend.
"""
from openedx.core.djangoapps.dark_lang.middleware import DarkLangMiddleware  # pylint: disable=import-error


def get_dark_lang_middleware():
    """Backend to get the DarkLangMiddleware from openedx."""
    return DarkLangMiddleware
