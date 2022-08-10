#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Eox tenant permissions module
"""
from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Permission
from django.contrib.contenttypes.models import ContentType
from django.core.exceptions import ImproperlyConfigured
from django.db.utils import ProgrammingError

LOGIN_ALL_TENANTS_PERMISSION_APP_LABEL = 'auth'
LOGIN_ALL_TENANTS_PERMISSION_CODENAME = 'can_login_all_eox_tenants'
LOGIN_ALL_TENANTS_PERMISSION_NAME = '.'.join([
    LOGIN_ALL_TENANTS_PERMISSION_APP_LABEL,
    LOGIN_ALL_TENANTS_PERMISSION_CODENAME,
])


def load_permissions():
    """
    Helper method to load a custom permission on DB that will be use to control login permissions
    on tenants.
    """
    try:
        if settings.EOX_TENANT_LOAD_PERMISSIONS:
            try:
                content_type = ContentType.objects.get_for_model(get_user_model())
                obj, created = Permission.objects.get_or_create(  # pylint: disable=unused-variable
                    codename=LOGIN_ALL_TENANTS_PERMISSION_CODENAME,
                    name='Can login to all eox-tenant Tenants',
                    content_type=content_type,
                )
            except ProgrammingError:
                # This code runs when the app is loaded, if a migration has not been done a ProgrammingError exception
                # is raised we are bypassing those cases to let migrations run smoothly.
                pass
    except ImproperlyConfigured:
        pass
