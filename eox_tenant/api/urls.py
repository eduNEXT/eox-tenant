"""
Api URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
"""
from django.urls import include, re_path

urlpatterns = [
    re_path(r'^v1/', include(('eox_tenant.api.v1.urls', 'eox_tenant'), namespace='v1'))
]
