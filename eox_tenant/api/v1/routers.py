"""
Routers file for eox_tenant api v1.
"""
from rest_framework import routers
from eox_tenant.api.v1.viewsets import MicrositeViewSet, TenantConfigViewSet, RouteViewSet

router = routers.DefaultRouter()
router.register(r'microsites', MicrositeViewSet)
router.register(r'tenant-config', TenantConfigViewSet)
router.register(r'routes', RouteViewSet)
