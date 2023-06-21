"""
Site/Tenant aware languages filter.
"""
from collections import namedtuple

from django.conf import settings

Language = namedtuple('Language', 'code name')


def tenant_languages():
    """Retrieve the list of released languages by tenant.

    Constructs a list of Language tuples by intersecting the
    list of valid language tuples with the list of released
    language codes.

    Returns:
       list of Language: Languages in which full translations are available.

    Example:

        >>> print released_languages()
        [Language(code='en', name=u'English'), Language(code='fr', name=u'Français')]

    """
    released_languages = getattr(settings, "released_languages", "")
    released_language_codes = [lang.lower().strip() for lang in released_languages.split(',')]
    default_language_code = settings.LANGUAGE_CODE

    if default_language_code not in released_language_codes:
        released_language_codes.append(default_language_code)

    released_language_codes.sort()

    # Intersect the list of valid language tuples with the list
    # of released language codes
    return [
        Language(language_info[0], language_info[1])
        for language_info in settings.LANGUAGES
        if language_info[0] in released_language_codes
    ]
