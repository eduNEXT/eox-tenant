"""
API v1 viewsets.
"""
from rest_framework import viewsets

from eox_tenant.api.v1.serializers import (
    MicrositeSerializer,
    RouteSerializer,
    TenantConfigSerializer
)
from eox_tenant.api.v1.permissions import EoxTenantAPIPermission
from eox_tenant.models import Microsite, Route, TenantConfig


class MicrositeViewSet(viewsets.ModelViewSet):
    """
    Microsite viewset.
    """
    resource_name = 'data'
    permission_classes = [EoxTenantAPIPermission]
    serializer_class = MicrositeSerializer
    queryset = Microsite.objects.all()


class TenantConfigViewSet(viewsets.ModelViewSet):
    """
    TenantConfig viewset.
    """
    permission_classes = [EoxTenantAPIPermission]
    serializer_class = TenantConfigSerializer
    queryset = TenantConfig.objects.all()


class RouteViewSet(viewsets.ModelViewSet):
    """
    Route viewset.
    """
    permission_classes = [EoxTenantAPIPermission]
    serializer_class = RouteSerializer
    queryset = Route.objects.all()
