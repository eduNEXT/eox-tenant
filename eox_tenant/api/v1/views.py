"""
APIViews module to manage the HTTPRequest with views based classes
"""
from typing import Dict

from django.http import HttpRequest, Http404

from rest_framework.response import Response
from rest_framework.views import APIView


from eox_tenant.receivers_helpers import get_tenant_config_by_domain


class MFESettingsView(APIView):
    """MFEApiView

    Retrieve the mfe tenant config data
    """

    def get(self, request: HttpRequest, format=None) -> Response:  # pylint: disable=unused-argument, redefined-builtin
        """http get method

        Args:
            request (HttpRequest): request incoming data
            format (_type_, optional): Defaults to None.

        Returns:
            Response: JSON Response
        """
        domain = request.get_host()

        configs, external_key = get_tenant_config_by_domain(domain)

        if not external_key:
            raise Http404

        configs = dict(configs)

        common = {
            "SITE_NAME": configs.get("PLATFORM_NAME"),
            "LOGO_URL": configs.get("logo_image_url", configs.get("LOGO_URL")),
            "LOGO_TRADEMARK_URL": configs.get("footer_logo_src", configs.get("LOGO_TRADEMARK_URL")),
            "LOGO_WHITE_URL": configs.get("LOGO_WHITE_URL"),
            "INFO_EMAIL": configs.get("INFO_EMAIL"),
            "FAVICON_URL": configs.get("FAVICON_URL"),
            "DISCOVERY_API_BASE_URL": configs.get("DISCOVERY_API_BASE_URL"),
            "PUBLISHER_BASE_URL": configs.get("PUBLISHER_BASE_URL"),
            "ECOMMERCE_BASE_URL": configs.get("ECOMMERCE_BASE_URL"),
            "LEARNING_BASE_URL": configs.get("LEARNING_BASE_URL"),
            "LMS_BASE_URL": configs.get("LMS_BASE_URL", configs["LMS_BASE"]),
            "LOGIN_URL": configs.get("LOGIN_URL"),
            "LOGOUT_URL": configs.get("LOGOUT_URL"),
            "STUDIO_BASE_URL": configs.get("STUDIO_BASE_URL"),
            "MARKETING_SITE_BASE_URL": configs.get("MARKETING_SITE_BASE_URL"),
            "ORDER_HISTORY_URL": configs.get("ORDER_HISTORY_URL"),
            "REFRESH_ACCESS_TOKEN_ENDPOINT": configs["REFRESH_ACCESS_TOKEN_ENDPOINT"],
            "SEGMENT_KEY": configs.get("SEGMENT_KEY"),
            "IGNORED_ERROR_REGEX": configs.get("IGNORED_ERROR_REGEX"),
            "CREDENTIALS_BASE_URL": configs.get("CREDENTIALS_BASE_URL"),
        }

        common = dict_filter(common)

        tenant_settings = {
            "id": common["LMS_BASE_URL"],
            "common": common,
            "learning": configs.get("learning", {}),
            "account": configs.get("account", {}),
            "profile": configs.get("profile", {}),
        }

        return Response(tenant_settings)


def dict_filter(object: Dict) -> Dict:  # pylint: disable=redefined-builtin
    """
    Filter None value of a dict argument and return just the items with
    value is not None
    """
    return {key: value for key, value in object.items() if value is not None}
