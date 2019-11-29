# -*- coding: utf-8 -*-
"""
Eox Tenant Signals
==================
This module makes it possible to override the settings object for a tenant.

How to debug in devstack
========================

Add the following lines to the lms.envs.devstack_docker module

LOGGING['handlers']['console']['level'] = 'DEBUG'
LOGGING['loggers']['']['level'] = 'INFO'
LOGGING['loggers']['eox_tenant'] = {
    'handlers': ['console'],
    'propagate': False,
    'level': 'DEBUG'
}

"""
from __future__ import print_function, unicode_literals

import logging
import os
from datetime import datetime

import six

from django.apps.config import AppConfig
from django.conf import settings as base_settings

from eox_tenant.backends.database import TenantConfigCompatibleMicrositeBackend

LOG = logging.getLogger(__name__)

# Read at the beginning so this can not be modified by the tenant configs
EOX_MAX_CONFIG_OVERRIDE_SECONDS = getattr(base_settings, "EOX_MAX_CONFIG_OVERRIDE_SECONDS", 300)


def _update_settings(domain):
    """
    Perform the override procedure on the settings object
    """
    config, tenant_key = _get_tenant_config(domain)

    if not config.get("EDNX_USE_SIGNAL"):
        LOG.info("Site %s, does not use eox_tenant signals", domain)
        return

    base_settings.EDNX_TENANT_KEY = tenant_key
    base_settings.EDNX_TENANT_DOMAIN = domain
    base_settings.EDNX_TENANT_SETUP_TIME = datetime.now()

    LOG.debug("PID: %s CONFIGURING THE SETTINGS OBJECT | %s", os.getpid(), tenant_key)
    for key, value in six.iteritems(config):
        if isinstance(value, dict):
            try:
                merged = getattr(base_settings, key, {}).copy()
            except AttributeError:
                merged = {}
            merged.update(value)
            setattr(base_settings, key, merged)
            continue
        setattr(base_settings, key, value)


def _repopulate_apps(apps):
    """
    After the initial loading of the settings, some djangoapps can override the AppConfig.ready() method
    to alter the settings in a particular way.
    In this case we need to run the app config again.
    We delegate the decision to the specific tenant on the EDNX_TENANT_INSTALLED_APPS key.
    If present, the key is passed in the apps argument
    """
    LOG.debug("PID: %s REPOPULATING APPS | %s", os.getpid(), apps)
    for entry in apps:
        app_config = AppConfig.create(entry)
        app_config.ready()


def _analyze_current_settings(domain):
    """
    The logic in here will determine if the current settings object has already been
    updated and if it has the matching overrides for the current request

    By default should anything go wrong, the function will always return that
    the settings object MUST be reset, and can NOT be kept
    """
    must_reset = True
    can_keep = False

    has_tenant_key = False
    try:
        current_key = base_settings.EDNX_TENANT_KEY
        has_tenant_key = True
        LOG.debug("PID: %s | The current_key: %s | the current domain: %s", os.getpid(), current_key, domain)
    except AttributeError:
        must_reset = False
        LOG.debug("PID: %s | No TENANT CONFIGURED SO FAR", os.getpid())

    try:
        if has_tenant_key and base_settings.EDNX_TENANT_DOMAIN == domain:
            must_reset = False
            can_keep = True
        elif must_reset:
            LOG.debug("SETTINGS WILL RESET | Reason: domain and current settings do not match")
    except AttributeError:
        must_reset = True
        LOG.debug("SETTINGS WILL RESET | Reason: we could not find "
                  "EDNX_TENANT_DOMAIN in the current settings object. PID: %s", os.getpid())

    return must_reset, can_keep


def _perform_reset():
    """
    Defers to the original django.conf.settings to a new initialization
    """
    base_settings._setup()  # pylint: disable=protected-access
    LOG.debug("Reset on the settings object for PID: %s", os.getpid())


def _ttl_reached():
    """
    Determines if the current settings object has been configured too long ago
    as defined in the MAX_CONFIG_OVERRIDE_SECONDS settings variable
    """
    try:
        if (datetime.now() - base_settings.EDNX_TENANT_SETUP_TIME).seconds > EOX_MAX_CONFIG_OVERRIDE_SECONDS:
            LOG.debug("SETTINGS WILL RESET | Reason: maximum time for this config override was reached")
            return True
    except AttributeError:
        pass

    return False


def _get_tenant_config(domain):
    """
    Reach for the configuration for a given domain

    Using the model directly introduces a circular dependency.
    That is why we go through the MicrositeBacked implementation.
    """
    backend = TenantConfigCompatibleMicrositeBackend()
    return backend.get_config_by_domain(domain)


def start_tenant(sender, environ, **kwargs):  # pylint: disable=unused-argument
    """
    This function runs every time a request is started.
    It will analyze the current settings object, the domain from the incoming
    request and the configuration stored in the tenants for this domain.

    Based on this input it will modify the settings objects in one of three possible ways:

    - reset the object to remove any previous modification
    - override the object with the settings stored for the tenant
    - reset the object and then override with a new tenant

    Signal: django.core.signals.request_started
    """
    http_host = environ.get("HTTP_HOST")
    if not http_host:
        LOG.warning("Could not find the host information for eox_tenant.signals")
        return
    try:
        if base_settings.SERVICE_VARIANT == "cms":
            LOG.debug("Studio does not support eox_tenant signals yet")
            return
    except AttributeError:
        LOG.warning("Could not determine the SERVICE_VARIANT on eox_tenant.signals")
        return

    domain = http_host.split(':')[0]

    # Find what we need to do about the current setting and the incoming request.domain
    must_reset, can_keep = _analyze_current_settings(domain)

    # Reset minimum once every so often
    must_reset = _ttl_reached() or must_reset

    # Perform the reset
    if must_reset:
        _perform_reset()
        can_keep = False

    if can_keep:
        return

    # Do the update
    _update_settings(domain)

    # Some django apps need to be reinitialized
    try:
        if base_settings.EDNX_TENANT_INSTALLED_APPS:
            _repopulate_apps(base_settings.EDNX_TENANT_INSTALLED_APPS)
    except AttributeError:
        pass


def finish_tenant(sender, **kwargs):  # pylint: disable=unused-argument
    """
    This function should terminate the tenant specific changes

    Signal: django.core.signals.request_finished

    Since the signal is not very reliable nothing is being done in it
    """
    pass


def clear_tenant(sender, request, **kwargs):  # pylint: disable=unused-argument
    """
    This function should terminate the tenant specific changes when the request fails unexpectedly

    Signal: django.core.signals.got_request_exception
    """
    pass


def debug_sender(sender, *args, **kwargs):  # pylint: disable=unused-argument
    """
    This function should terminate the tenant specific changes when the request fails unexpectedly
    """
    print("===================debug_sender===================")

    headers = kwargs.get('headers')
    headers['eox_tenant_sender'] = 'site1.localhost:18000'
    headers['X-Forwarded-For'] = 'CRITICAL_PIECE_OF_INFO'


from celery.contrib import rdb


def debug_receiver(sender, *args, **kwargs):  # pylint: disable=unused-argument
    """
    This function should terminate the tenant specific changes when the request fails unexpectedly
    """

    print("==================debug_receiver====================")
    headers = sender.request.get('headers', {})


    http_host = headers.get('eox_tenant_sender')



    domain = http_host.split(':')[0]

    # Find what we need to do about the current setting and the incoming request.domain
    must_reset, can_keep = _analyze_current_settings(domain)

    # Reset minimum once every so often
    must_reset = _ttl_reached() or must_reset

    # Perform the reset
    if must_reset:
        _perform_reset()
        can_keep = False

    if can_keep:
        return

    # Do the update
    _update_settings(domain)

    # Some django apps need to be reinitialized
    try:
        if base_settings.EDNX_TENANT_INSTALLED_APPS:
            _repopulate_apps(base_settings.EDNX_TENANT_INSTALLED_APPS)
    except AttributeError:
        pass