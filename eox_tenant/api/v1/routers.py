"""
Routers file for eox_tenant api v1.
"""
from rest_framework import routers

from eox_tenant.api.v1.viewsets import MicrositeViewSet, RouteViewSet, TenantConfigViewSet

router = routers.DefaultRouter()
router.register(r'microsites', MicrositeViewSet)
router.register(r'configs', TenantConfigViewSet)
router.register(r'routes', RouteViewSet)
