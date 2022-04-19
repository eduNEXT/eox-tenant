from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response

from eox_tenant.models import TenantConfig


class MFESettingsView(APIView):
    def get(self, request, format=None, *args, **kwargs) -> Response:
        tenant_key = kwargs["tenant"]
        tenant = get_object_or_404(TenantConfig, external_key__contains=tenant_key)
        configs = tenant.lms_configs

        tennat_settings = {
            "id": configs["LMS_BASE"],
            "common": {
                "SITE_NAME": configs["LMS_BASE"],
                "LOGO_URL": configs["LOGO_URL"],
                "LOGO_TRADEMARK_URL": configs["LOGO_TRADEMARK_URL"],
                "LOGO_WHITE_URL": configs["LOGO_WHITE_URL"],
                "INFO_EMAIL": configs["INFO_EMAIL"],
                "FAVICON_URL": configs["FAVICON_URL"],
                "DISCOVERY_API_BASE_URL": configs["DISCOVERY_API_BASE_URL"],
                "PUBLISHER_BASE_URL": configs["PUBLISHER_BASE_URL"],
                "ECOMMERCE_BASE_URL": configs["ECOMMERCE_BASE_URL"],
                "LEARNING_BASE_URL": configs["LEARNING_BASE_URL"],
                "LMS_BASE_URL": configs["LMS_BASE_URL"],
                "LOGIN_URL": configs["LOGIN_URL"],
                "LOGOUT_URL": configs["LOGOUT_URL"],
                "STUDIO_BASE_URL": configs["STUDIO_BASE_URL"],
                "MARKETING_SITE_BASE_URL": configs["MARKETING_SITE_BASE_URL"],
                "ORDER_HISTORY_URL": configs["ORDER_HISTORY_URL"],
                "REFRESH_ACCESS_TOKEN_ENDPOINT": configs["REFRESH_ACCESS_TOKEN_ENDPOINT"],
                "SEGMENT_KEY": configs["SEGMENT_KEY"],
                "IGNORED_ERROR_REGEX": configs["IGNORED_ERROR_REGEX"],
                "CREDENTIALS_BASE_URL": configs["CREDENTIALS_BASE_URL"],
            },
            "learning": configs.get("learning", dict()),
            "account": configs.get("account", dict()),
            "profile": configs.get("profile", dict()),
        }

        return Response(tennat_settings)
