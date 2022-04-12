from rest_framework.decorators import api_view
from rest_framework.views import APIView
from rest_framework.response import Response


class MFESettingsView(APIView):
    def get(self, request, format=None, *args, **kwargs):
        return Response(
            {
                "id": "localhost",
                "common": {
                    "SITE_NAME": "json-server",
                    "LOGO_URL": "https://www.w3.org/TR/SVG-access/tiger.png",
                    "LOGO_TRADEMARK_URL": "https://www.w3.org/TR/SVG-access/tiger.png",
                    "LOGO_WHITE_URL": "https://www.w3.org/TR/SVG-access/tiger.png",
                    "INFO_EMAIL": "diana.olarte@edunext.co",
                    "FAVICON_URL": "https://www.w3.org/TR/SVG-access/tiger.png",
                    "DISCOVERY_API_BASE_URL": "http://localhost:18381",
                    "PUBLISHER_BASE_URL": "http://localhost:18400",
                    "ECOMMERCE_BASE_URL": "http://localhost:18130",
                    "LEARNING_BASE_URL": "http://localhost:2000",
                    "LMS_BASE_URL": "http://localhost:18000",
                    "LOGIN_URL": "http://localhost:18000/login",
                    "LOGOUT_URL": "http://localhost:18000/logout",
                    "STUDIO_BASE_URL": "http://localhost:18010",
                    "MARKETING_SITE_BASE_URL": "http://localhost:18000",
                    "ORDER_HISTORY_URL": "http://localhost:1996/orders",
                    "REFRESH_ACCESS_TOKEN_ENDPOINT": "http://localhost:18000/login_refresh",
                    "SEGMENT_KEY": "",
                    "IGNORED_ERROR_REGEX": "",
                    "CREDENTIALS_BASE_URL": "http://localhost:18150",
                },
                "learning": {},
                "account": {},
                "profile": {},
            }
        )
