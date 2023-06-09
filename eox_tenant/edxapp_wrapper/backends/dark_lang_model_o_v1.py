from openedx.core.djangoapps.dark_lang.models import DarkLangConfig


def get_dark_lang_config_model():
    """Backend to get the DarkLangConfig from openedx."""
    return DarkLangConfig
