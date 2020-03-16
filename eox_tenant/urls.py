"""eox-tenant urls"""

from django.conf.urls import url
from eox_tenant import views


urlpatterns = [
    url(r'^eox-info$', views.info_view, name='eox-info'),
]
