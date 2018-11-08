#!/usr/bin/python
"""
This file implements the Middleware support for the Open edX platform.
A microsite enables the following features:

1) Mapping of sub-domain name to a 'brand', e.g. foo-university.edx.org
2) Present a landing page with a listing of courses that are specific to the 'brand'
3) Ability to swap out some branding elements in the website
"""
import re

from django.conf import settings
from django.http import Http404

from opaque_keys import InvalidKeyError
from opaque_keys.edx.keys import CourseKey
from microsite_configuration import microsite  # pylint: disable=import-error


class SimpleMicrositeMiddleware(object):
    """
    Middleware class which will clear any data from the microsite module on exit
    """

    # pylint: disable=unused-argument
    def process_response(self, request, response):
        """
        Middleware exit point to delete cache data.
        """
        microsite.clear()
        return response


class MicrositeMiddleware(SimpleMicrositeMiddleware):
    """
    Middleware class which will bind configuration information regarding 'microsites' on a per request basis.
    The actual configuration information is taken from Django settings information
    """

    def process_request(self, request):
        """
        Middleware entry point on every request processing. This will associate a request's domain name
        with a 'University' and any corresponding microsite configuration information
        """
        microsite.clear()

        domain = request.META.get('HTTP_HOST', None)

        microsite.set_by_domain(domain)

        return None


class MicrositeCrossBrandingFilterMiddleware():
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
        org_filter = microsite.get_value('course_org_filter', set([]))
        if isinstance(org_filter, basestring):
            org_filter = set([org_filter])
        if course_key.org in org_filter:
            return None

        # If the course does not belong to an ORG defined in a microsite
        all_orgs = microsite.get_all_orgs()
        if course_key.org not in all_orgs:
            return None

        # We could log some of the output here for forensic analysis
        raise Http404