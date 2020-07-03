#!/usr/bin/python
"""
This file implements the Middleware support for the Open edX platform.
A microsite enables the following features:

1) Mapping of sub-domain name to a 'brand', e.g. foo-university.edx.org
2) Present a landing page with a listing of courses that are specific to the 'brand'
3) Ability to swap out some branding elements in the website
"""
import logging
import re

from django.conf import settings
from django.contrib.sites.shortcuts import get_current_site
from django.http import Http404, HttpResponseNotFound
from django.utils import six
from django.utils.deprecation import MiddlewareMixin
from opaque_keys import InvalidKeyError
from opaque_keys.edx.keys import CourseKey

from eox_tenant.edxapp_wrapper.edxmako_module import get_edxmako_module
from eox_tenant.edxapp_wrapper.site_configuration_module import get_configuration_helpers
from eox_tenant.edxapp_wrapper.theming_helpers import get_theming_helpers
from eox_tenant.tenant_wise.proxies import TenantSiteConfigProxy

configuration_helper = get_configuration_helpers()  # pylint: disable=invalid-name
theming_helper = get_theming_helpers()
HOST_VALIDATION_RE = re.compile(r"^(?:[0-9]{1,3}\.){3}[0-9]{1,3}(:[0-9]{2,5})?$")
LOG = logging.getLogger(__name__)


class MicrositeCrossBrandingFilterMiddleware(MiddlewareMixin):
    """
    Middleware class that prevents a course defined in a branded ORG trough a microsite, to be displayed
    on a different microsite with a different branding.
    """
    def process_request(self, request):
        """
        Raise an 404 exception if the course being rendered belongs to an ORG in a
        microsite, but it is not the current microsite
        """
        path = request.path_info
        regex_path_match = re.compile('/courses/{}/'.format(settings.COURSE_ID_PATTERN))
        matched_regex = regex_path_match.match(path)

        # If there is no match, then we are not in a ORG-restricted area
        if matched_regex is None:
            return None

        course_id = matched_regex.group('course_id')
        try:
            course_key = CourseKey.from_string(course_id)
        except InvalidKeyError:
            raise Http404

        # If the course org is the same as the current microsite
        org_filter = configuration_helper.get_value('course_org_filter', set([]))
        if isinstance(org_filter, six.string_types):
            org_filter = set([org_filter])
        if course_key.org in org_filter:
            return None

        # If the course does not belong to an ORG defined in a microsite
        all_orgs = configuration_helper.get_all_orgs()
        if course_key.org not in all_orgs:
            return None

        # We could log some of the output here for forensic analysis
        raise Http404


class AvailableScreenMiddleware(MiddlewareMixin):
    """
    Middleware for Redirecting microsites to other domains or to error pages
    """

    def process_request(self, request):
        """
        This middleware handles redirections and error pages according to the
        business logic at edunext
        """
        domain = request.META.get('HTTP_HOST', "")

        if (
            not theming_helper.is_request_in_themed_site()
            and settings.FEATURES.get('USE_MICROSITE_AVAILABLE_SCREEN', False)
            and not bool(HOST_VALIDATION_RE.search(domain))
        ):
            return HttpResponseNotFound(
                get_edxmako_module().shortcuts.render_to_string(
                    'eox-tenant/not_found.html',
                    {'domain': domain, }
                )
            )


class CurrentSiteMiddleware(MiddlewareMixin):
    """
    Middleware class that defines the site and its configuration.

    This is a replacement of  <django.contrib.sites.middleware.CurrentSiteMiddleware>
    that uses as configuration the model TenantSiteConfigProxy.

    Original middleware info in https://docs.djangoproject.com/en/1.11/_modules/django/contrib/sites/middleware/
    """

    def process_request(self, request):
        """
        Get the current site for a given request a set the configuration.
        """
        site = get_current_site(request)
        site.configuration = TenantSiteConfigProxy()
        request.site = site
