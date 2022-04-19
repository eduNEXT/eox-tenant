"""
Version 1 URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
"""
from django.conf.urls import include, url

from eox_tenant.api.v1.routers import router
from eox_tenant.api.v1.views import MFESettingsView

urlpatterns = [
    url(r'^mfe-api/(?P<tenant>[\w+\W]+)/$', MFESettingsView.as_view(), name="mfe-api"),
    url(r'', include((router.urls, 'eox_tenant'), namespace='tenant-api')),
]
