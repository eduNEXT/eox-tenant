"""
Common settings for eox_tenant project.
"""
from __future__ import absolute_import, unicode_literals

import codecs
import os

import yaml

from .common import *  # pylint: disable=wildcard-import,unused-wildcard-import


class SettingsClass:
    """ dummy settings class """
    OAUTH2_PROVIDER = {}


ALLOWED_HOSTS = ['*']
SETTINGS = SettingsClass()
# This is executing the plugin_settings method imported from common module
plugin_settings(SETTINGS)
vars().update(SETTINGS.__dict__)
INSTALLED_APPS = vars().get('INSTALLED_APPS', [])
TEST_INSTALLED_APPS = [
    'django.contrib.sites',
    'django.contrib.admin',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
]
for app in TEST_INSTALLED_APPS:
    if app not in INSTALLED_APPS:
        INSTALLED_APPS.append(app)

GET_SITE_CONFIGURATION_MODULE = 'eox_tenant.edxapp_wrapper.backends.site_configuration_module_test_v1'
GET_THEMING_HELPERS = 'eox_tenant.edxapp_wrapper.backends.theming_helpers_test_v1'
EOX_TENANT_USERS_BACKEND = 'eox_tenant.edxapp_wrapper.backends.users_test_v1'
EOX_TENANT_BEARER_AUTHENTICATION = 'eox_tenant.edxapp_wrapper.backends.bearer_authentication_test_v1'

COURSE_KEY_PATTERN = r'(?P<course_key_string>[^/+]+(/|\+)[^/+]+(/|\+)[^/?]+)'
COURSE_ID_PATTERN = COURSE_KEY_PATTERN.replace('course_key_string', 'course_id')

TEST_DICT_OVERRIDE_TEST = {
    'key1': 'Some Value'
}

EOX_TENANT_SKIP_FILTER_FOR_TESTS = False
EOX_TENANT_LOAD_PERMISSIONS = True

FEATURES = {}
FEATURES['USE_MICROSITE_AVAILABLE_SCREEN'] = False
FEATURES['USE_REDIRECTION_MIDDLEWARE'] = False
USE_EOX_TENANT = True

SITE_ID = 1

ROOT_URLCONF = 'eox_tenant.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

MIDDLEWARE = [
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
]


def plugin_settings(settings):  # pylint: disable=function-redefined
    """
    For the platform tests, we want everything to be disabled
    """
    settings.FEATURES['USE_MICROSITE_AVAILABLE_SCREEN'] = False
    settings.FEATURES['USE_REDIRECTION_MIDDLEWARE'] = False
    settings.GET_SITE_CONFIGURATION_MODULE = 'eox_tenant.edxapp_wrapper.backends.site_configuration_module_test_v1'
    settings.GET_THEMING_HELPERS = 'eox_tenant.edxapp_wrapper.backends.theming_helpers_test_v1'
    settings.EOX_TENANT_SKIP_FILTER_FOR_TESTS = True
    settings.EOX_TENANT_LOAD_PERMISSIONS = False
    if hasattr(settings, 'OAUTH2_PROVIDER'):
        settings.OAUTH2_PROVIDER['OAUTH2_VALIDATOR_CLASS'] = (
            'openedx.core.djangoapps.oauth_dispatch.dot_overrides.validators.EdxOAuth2Validator'
        )

    # setup the databases used in the tutor local environment
    with codecs.open(os.environ['LMS_CFG'], encoding='utf-8') as f:
        env_tokens = yaml.safe_load(f)
    settings.DATABASES = env_tokens['DATABASES']


# Integration test settings
INTEGRATION_TEST_SETTINGS = {
    # Retrieved from the Tutor environment where the integration tests run
    "EOX_TENANT_BASE_URL": f"http://{os.environ.get('LMS_HOST', 'local.edly.io')}/eox-tenant",
    "API_TIMEOUT": 5,
}
