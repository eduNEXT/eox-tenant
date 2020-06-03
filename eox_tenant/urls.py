"""eox-tenant urls"""

from django.conf.urls import include, url

from eox_tenant import views

urlpatterns = [
    url(r'^eox-info$', views.info_view, name='eox-info'),
    url(r'^api/', include(('eox_tenant.api.urls', 'eox_tenant'), namespace='api')),
]
