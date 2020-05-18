#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Users public function definitions
"""

from importlib import import_module

from django.conf import settings


def get_user_signup_source():
    """ Get the UserSignupSource model """

    backend_function = settings.EOX_TENANT_USERS_BACKEND
    backend = import_module(backend_function)

    return backend.get_user_signup_source()
