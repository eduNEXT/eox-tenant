"""Module where eox-tenant constants are defined."""
from django.conf import settings

LMS_ENVIRONMENT = getattr(settings, "SERVICE_VARIANT", None) == "lms"
