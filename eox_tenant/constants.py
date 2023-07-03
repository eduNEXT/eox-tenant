"""Module where eox-tenant constants are defined."""
from django.conf import settings

LMS_ENVIRONMENT = getattr(settings, "SERVICE_VARIANT", None) == "lms"
CMS_ENVIRONMENT = getattr(settings, "SERVICE_VARIANT", None) == "cms"
LMS_CONFIG_COLUMN = "lms_configs"
CMS_CONFIG_COLUMN = "studio_configs"
