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
from django.contrib.auth import REDIRECT_FIELD_NAME
from django.contrib.auth.views import redirect_to_login
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.http import Http404, HttpResponseNotFound, HttpResponseRedirect
from django.utils import six

from eox_tenant.models import Redirection
from opaque_keys import InvalidKeyError
from opaque_keys.edx.keys import CourseKey

from eox_tenant.edxapp_wrapper.edxmako_module import get_edxmako_module
from eox_tenant.edxapp_wrapper.get_microsite_configuration import get_microsite
from eox_tenant.utils import cache, fasthash

microsite = get_microsite()  # pylint: disable=invalid-name
HOST_VALIDATION_RE = re.compile(r"^(?:[0-9]{1,3}\.){3}[0-9]{1,3}(:[0-9]{2,5})?$")
LOG = logging.getLogger(__name__)


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
        if isinstance(org_filter, six.string_types):
            org_filter = set([org_filter])
        if course_key.org in org_filter:
            return None

        # If the course does not belong to an ORG defined in a microsite
        all_orgs = microsite.get_all_orgs()
        if course_key.org not in all_orgs:
            return None

        # We could log some of the output here for forensic analysis
        raise Http404


class RedirectionsMiddleware(object):
    """
    Middleware for Redirecting microsites to other domains or to error pages
    """

    def process_request(self, request):
        """
        This middleware handles redirections and error pages according to the
        business logic at edunext
        """
        if not settings.FEATURES.get('USE_REDIRECTION_MIDDLEWARE', True):
            return

        domain = request.META.get('HTTP_HOST', "")

        # First handle the event where a domain has a redirect target
        cache_key = "redirect_cache." + fasthash(domain)
        target = cache.get(cache_key)  # pylint: disable=maybe-no-member

        if not target:
            try:
                target = Redirection.objects.get(domain__iexact=domain)  # pylint: disable=no-member
            except Redirection.DoesNotExist:  # pylint: disable=no-member
                target = '##none'

            cache.set(  # pylint: disable=maybe-no-member
                cache_key, target, 5 * 60
            )

        if target != '##none':
            # If we are already at the target, just return
            if domain == target.target and request.scheme == target.scheme:  # pylint: disable=no-member
                return

            to_url = '{scheme}://{host}{path}'.format(
                scheme=target.scheme,  # pylint: disable=no-member
                host=target.target,  # pylint: disable=no-member
                path=request.path,  # pylint: disable=no-member
            )

            return HttpResponseRedirect(
                to_url,
                status=target.status,  # pylint: disable=no-member
            )

        # By this time, if there is no redirect, and no microsite, the domain is available
        if (not microsite.is_request_in_microsite()
                and settings.FEATURES.get('USE_MICROSITE_AVAILABLE_SCREEN', False)
                and not bool(HOST_VALIDATION_RE.search(domain))):
            return HttpResponseNotFound(get_edxmako_module().shortcuts.render_to_string('microsites/not_found.html', {
                'domain': domain,
            }))

    @staticmethod
    @receiver(post_save, sender=Redirection)
    def clear_cache(sender, instance, **kwargs):  # pylint: disable=unused-argument
        """
        Clear the cached template when the model is saved
        """
        cache_key = "redirect_cache." + fasthash(instance.domain)
        cache.delete(cache_key)  # pylint: disable=maybe-no-member


class PathRedirectionMiddleware(object):
    """
    Middleware to create custom responses based on the request path
    """

    def process_request(self, request):
        """
        This middleware processes the path of every request and determines if there
        is a configured action to take.
        """
        if not microsite.has_override_value("EDNX_CUSTOM_PATH_REDIRECTS"):
            return

        redirects = microsite.get_value("EDNX_CUSTOM_PATH_REDIRECTS", {})

        for regex, values in redirects.iteritems():

            if isinstance(values, dict):
                key = next(iter(values))
            else:
                key = values

            path = request.path_info
            regex_path_match = re.compile(regex.format(
                COURSE_ID_PATTERN=settings.COURSE_ID_PATTERN,
                USERNAME_PATTERN=settings.USERNAME_PATTERN,
            ))

            if regex_path_match.match(path):
                try:
                    action = getattr(self, key)
                    return action(request=request, key=key, values=values, path=path)
                except Http404:  # we expect 404 to be raised
                    raise
                except Exception, error:  # pylint: disable=broad-except
                    LOG.error("The PathRedirectionMiddleware generated an error at: %s%s",
                              request.get_host(),
                              request.get_full_path())
                    LOG.error(error)
                    return

    def login_required(self, request, path, **kwargs):  # pylint: disable=unused-argument
        """
        Action: a user session must exist.
        If it does not, redirect to the login page
        """
        if request.user.is_authenticated():
            return
        else:
            resolved_login_url = microsite.get_dict("FEATURES", {}).get(
                "ednx_custom_login_link", settings.LOGIN_URL)
            return redirect_to_login(path, resolved_login_url, REDIRECT_FIELD_NAME)

    def not_found(self, **kwargs):  # pylint: disable=unused-argument
        """
        Action: return 404 error for anyone
        """
        raise Http404

    def not_found_loggedin(self, request, **kwargs):  # pylint: disable=unused-argument
        """
        Action: return 404 error for users which have a session
        """
        if request.user.is_authenticated():
            raise Http404

    def not_found_loggedout(self, request, **kwargs):  # pylint: disable=unused-argument
        """
        Action: return 404 error for users that don't have a session
        """
        if not request.user.is_authenticated():
            raise Http404

    def redirect_always(self, key, values, **kwargs):  # pylint: disable=unused-argument
        """
        Action: redirect to the given target
        """
        return HttpResponseRedirect(values[key])

    def redirect_loggedin(self, request, key, values, **kwargs):  # pylint: disable=unused-argument
        """
        Action: redirect logged users to the given target
        """
        if request.user.is_authenticated():
            return HttpResponseRedirect(values[key])

    def redirect_loggedout(self, request, key, values, **kwargs):  # pylint: disable=unused-argument
        """
        Action: redirect external visitors to the given target
        """
        if not request.user.is_authenticated():
            return HttpResponseRedirect(values[key])
