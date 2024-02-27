# -*- coding: utf-8 -*-
"""
Module that defines the class used to handle the async tasks
"""

import logging

from django.conf import settings as base_settings
from django.contrib.sites.models import Site

LOG = logging.getLogger(__name__)


class AsyncTaskHandler:
    """
    Handler used to get the tenant of an async task.
    """

    sender = None

    def get_host_from_task(self, sender):
        """
        Method used to get the function used to get the tenant domain
        accordingly to the type of task.
        """
        self.sender = sender
        value = base_settings.EOX_TENANT_ASYNC_TASKS_HANDLER_DICT.get(sender, 'tenant_from_sync_process')
        action = getattr(self, value)
        return action()

    def get_host_from_siteid(self):
        """
        Get the tenant domain name using its Site id.
        Used in ScheduleRecurringNudge task
        """
        def get_host(body):
            """
            Get host from siteid.
            """
            try:
                siteid = body.get('args')[0]
                site = Site.objects.get(id=siteid)
                domain = site.name
            except (Site.DoesNotExist, KeyError, TypeError):  # pylint: disable=no-member
                return self.tenant_from_sync_process()(body)
            return domain

        return get_host

    def tenant_from_sync_process(self):
        """
        Used when the task is not associated to any tenant.
        """
        host = getattr(base_settings, 'EDNX_TENANT_DOMAIN', None)

        if not host:
            LOG.warning(
                "Could not find the host information for eox_tenant.signals "
                "for the task %s", self.sender
            )

        def get_host(_body):
            """
            Get host using default site id.
            """
            return host

        return get_host
