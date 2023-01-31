"""
Version 1 URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
"""
from django.urls import include, re_path

from eox_tenant.api.v1.routers import router

urlpatterns = [
    re_path(r'', include((router.urls, 'eox_tenant'), namespace='tenant-api')),
]
