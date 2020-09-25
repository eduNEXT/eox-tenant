"""
API v1 viewsets.
"""
from rest_framework import viewsets
from rest_framework.parsers import JSONParser

from eox_tenant.api.v1.permissions import EoxTenantAPIPermission
from eox_tenant.api.v1.serializers import MicrositeSerializer, RouteSerializer, TenantConfigSerializer
from eox_tenant.models import Microsite, Route, TenantConfig


class MicrositeViewSet(viewsets.ModelViewSet):
    """MicrositeViewSet that allows the basic API actions."""

    parser_classes = [JSONParser]
    permission_classes = [EoxTenantAPIPermission]
    serializer_class = MicrositeSerializer
    queryset = Microsite.objects.all()


class TenantConfigViewSet(viewsets.ModelViewSet):
    """TenantConfigViewSet that allows the basic API actions."""

    parser_classes = [JSONParser]
    permission_classes = [EoxTenantAPIPermission]
    serializer_class = TenantConfigSerializer
    queryset = TenantConfig.objects.all()


class RouteViewSet(viewsets.ModelViewSet):
    """RouteViewSet that allows the basic API actions."""

    parser_classes = [JSONParser]
    permission_classes = [EoxTenantAPIPermission]
    serializer_class = RouteSerializer
    queryset = Route.objects.all()
