"""eox-tenant urls"""

from django.urls import include, re_path

from eox_tenant import views

urlpatterns = [
    re_path(r'^eox-info$', views.info_view, name='eox-info'),
    re_path(r'^api/', include(('eox_tenant.api.urls', 'eox_tenant'), namespace='api')),
]
