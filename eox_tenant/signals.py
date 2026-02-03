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
from datetime import datetime
from os import getpid

import six
from django.apps.config import AppConfig
from django.conf import settings as base_settings

from eox_tenant.async_utils import AsyncTaskHandler
from eox_tenant.constants import CMS_CONFIG_COLUMN, LMS_CONFIG_COLUMN
from eox_tenant.receivers_helpers import get_tenant_config_by_domain
from eox_tenant.utils import synchronize_tenant_organizations

LOG = logging.getLogger(__name__)

# Read at the beginning so this can not be modified by the tenant configs
EOX_MAX_CONFIG_OVERRIDE_SECONDS = getattr(base_settings, "EOX_MAX_CONFIG_OVERRIDE_SECONDS", 300)


def _update_settings(domain, config_key):
    """
    Perform the override procedure on the settings object
    """
    config, tenant_key = get_tenant_config_by_domain(domain, config_key)

    if not config.get("EDNX_USE_SIGNAL"):
        LOG.info("Site %s, does not use eox_tenant signals", domain)
        return

    base_settings.EDNX_TENANT_KEY = tenant_key
    base_settings.EDNX_TENANT_DOMAIN = domain
    base_settings.EDNX_TENANT_SETUP_TIME = datetime.now()

    LOG.debug("PID: %s CONFIGURING THE SETTINGS OBJECT | %s", getpid(), tenant_key)
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

    # Some django apps need to be reinitialized
    try:
        if base_settings.EDNX_TENANT_INSTALLED_APPS:
            _repopulate_apps(base_settings.EDNX_TENANT_INSTALLED_APPS)
    except AttributeError:
        pass


def _repopulate_apps(apps):
    """
    After the initial loading of the settings, some djangoapps can override the AppConfig.ready() method
    to alter the settings in a particular way.
    In this case we need to run the app config again.
    We delegate the decision to the specific tenant on the EDNX_TENANT_INSTALLED_APPS key.
    If present, the key is passed in the apps argument
    """
    LOG.debug("PID: %s REPOPULATING APPS | %s", getpid(), apps)
    for entry in apps:
        app_config = AppConfig.create(entry)
        app_config.ready()


def can_keep_settings(domain):
    """
    Find what we need to do about the current setting and the incoming request.domain
    and Reset settings if needed.
    """
    must_reset, can_keep = _analyze_current_settings(domain)

    if _ttl_reached() or must_reset:  # Perform the reset
        _perform_reset()
        can_keep = False

    return can_keep


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
        LOG.debug("PID: %s | The current_key: %s | the current domain: %s", getpid(), current_key, domain)
    except AttributeError:
        must_reset = False
        LOG.debug("PID: %s | No TENANT CONFIGURED SO FAR", getpid())

    try:
        if has_tenant_key and base_settings.EDNX_TENANT_DOMAIN == domain:
            must_reset = False
            can_keep = True
        elif must_reset:
            LOG.debug("SETTINGS WILL RESET | Reason: domain and current settings do not match")
    except AttributeError:
        must_reset = True
        LOG.debug("SETTINGS WILL RESET | Reason: we could not find "
                  "EDNX_TENANT_DOMAIN in the current settings object. PID: %s", getpid())

    return must_reset, can_keep


def _perform_reset():
    """
    Defers to the original django.conf.settings to a new initialization
    """
    base_settings._setup()  # pylint: disable=protected-access
    LOG.debug("Reset on the settings object for PID: %s", getpid())


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


def start_lms_tenant(sender, environ, **kwargs):  # pylint: disable=unused-argument
    """
    This function runs every time a request is started in LMS.
    Read documentation of `_start_tenant` for more details.
    """
    _start_tenant(environ, LMS_CONFIG_COLUMN)


def start_studio_tenant(sender, environ, **kwargs):  # pylint: disable=unused-argument
    """
    This function runs every time a request is started in studio.
    Read documentation of `_start_tenant` for more details.
    """
    _start_tenant(environ, CMS_CONFIG_COLUMN)


def _start_tenant(environ, config_key):
    """
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

    domain = http_host.split(':')[0]

    if can_keep_settings(domain):
        return

    # Do the update
    _update_settings(domain, config_key)


def finish_tenant(sender, **kwargs):  # pylint: disable=unused-argument
    """
    This function should terminate the tenant specific changes

    Signal: django.core.signals.request_finished

    Since the signal is not very reliable nothing is being done in it
    """


def clear_tenant(sender, request, **kwargs):  # pylint: disable=unused-argument
    """
    This function should terminate the tenant specific changes when the request fails unexpectedly

    Signal: django.core.signals.got_request_exception
    """


def tenant_context_addition(sender, body, headers, *args, **kwargs):  # pylint: disable=unused-argument
    """
    Receiver used to add context to the async process about the tenant associated to the task that need to be done.

    Dispatched before a celery task is published. Note that this is executed in the process sending the task.
    See:
        https://celery.readthedocs.io/en/latest/userguide/signals.html#before-task-publish
    """
    if not getattr(base_settings, "USE_EOX_TENANT", False):
        return

    get_host_func = AsyncTaskHandler().get_host_from_task(sender)
    headers['eox_tenant_sender'] = get_host_func(body)
    body['kwargs']['eox_tenant_sender'] = get_host_func(body)


def start_async_lms_tenant(sender, *args, **kwargs):  # pylint: disable=unused-argument
    """
    Receiver that runs on the LMS async process to update the settings accordingly to the tenant.
    Read documentation of `_start_tenant` for more details.
    """
    _start_async_tenant(sender, LMS_CONFIG_COLUMN)


def start_async_studio_tenant(sender, *args, **kwargs):  # pylint: disable=unused-argument
    """
    Receiver that runs on the studio async process to update the settings accordingly to the tenant.
    Read documentation of `_start_tenant` for more details.
    """
    _start_async_tenant(sender, CMS_CONFIG_COLUMN)


def _start_async_tenant(sender, config_key):
    """
    Dispatched before a task is executed.
    See:
       https://celery.readthedocs.io/en/latest/userguide/signals.html#task-prerun
    """
    if not getattr(base_settings, "USE_EOX_TENANT", False):
        return

    context = sender.request
    headers = context.get('headers') or {}
    http_host = headers.get('eox_tenant_sender')
    http_host = context.get('kwargs', {}).pop('eox_tenant_sender', http_host)

    if not http_host:  # Reset settings in case of no tenant.
        LOG.warning("Could not find the host information for eox_tenant.signals. ")
        _perform_reset()
        return

    domain = http_host

    if can_keep_settings(domain):
        return

    # Do the update
    _update_settings(domain, config_key)


def update_tenant_organizations(instance, **kwargs):  # pylint: disable=unused-argument
    """
    Receiver method  which synchronizes the course_org_filter value with
    the instance.organizations field.

    Args:
        instance: This could be a TenantConfig or Microsite model instance.
        kwargs: extra arguments.
    """
    synchronize_tenant_organizations(instance)
