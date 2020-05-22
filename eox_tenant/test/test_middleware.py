#!/usr/bin/python
"""
TODO: add me
"""
import mock
from django.contrib.sites.models import Site
from django.http import Http404
from django.test import RequestFactory, TestCase, override_settings

from eox_tenant.middleware import (
    AvailableScreenMiddleware,
    CurrentSiteMiddleware,
    MicrositeCrossBrandingFilterMiddleware,
)


class MicrositeCrossBrandingFilterMiddlewareTest(TestCase):

    """
    Testing the middleware MicrositeCrossBrandingFilterMiddleware
    """
    def setUp(self):
        """ setup """
        self.request_factory = RequestFactory()
        self.middleware_instance = MicrositeCrossBrandingFilterMiddleware()

    def test_no_url_courses_match(self):
        """
        Test when request url does not match the course id pattern
        """
        request = self.request_factory.get('/courses/nomatch')
        result = self.middleware_instance.process_request(request)
        self.assertIsNone(result)

    @mock.patch('eox_tenant.middleware.configuration_helper')
    def test_url_courses_match_org_in_filter(self, conf_helper_mock):
        """
        Test when request url match the course id pattern but the course org
        belongs to the current site/microsite
        """
        request = self.request_factory.get('/courses/course-v1:TEST_ORG+CS101+2019_T1/')
        conf_helper_mock.get_value.return_value = ['TEST_ORG']
        result = self.middleware_instance.process_request(request)
        conf_helper_mock.get_value.assert_called_once()
        conf_helper_mock.get_all_orgs.assert_not_called()
        self.assertIsNone(result)

    @mock.patch('eox_tenant.middleware.configuration_helper')
    def test_url_courses_match_org_not_in_all_orgs(self, conf_helper_mock):
        """
        Test when request url match the course id pattern but the course org
        does not belong to any site/microsite
        """
        request = self.request_factory.get('/courses/course-v1:TEST_ORG+CS101+2019_T1/')
        conf_helper_mock.get_value.return_value = []
        conf_helper_mock.get_all_orgs.return_value = ['Some_org', 'new_org', 'other_org']
        result = self.middleware_instance.process_request(request)
        conf_helper_mock.get_value.assert_called_once()
        conf_helper_mock.get_all_orgs.assert_called_once()
        self.assertIsNone(result)

    @mock.patch('eox_tenant.middleware.configuration_helper')
    def test_url_courses_match_org_in_other_site(self, conf_helper_mock):
        """
        Test when request url match the course id pattern but the course org
        does belong to any site/microsite
        """
        request = self.request_factory.get('/courses/course-v1:TEST_ORG+CS101+2019_T1/')
        conf_helper_mock.get_value.return_value = ['other_org']
        conf_helper_mock.get_all_orgs.return_value = ['Some_org', 'new_org', 'TEST_ORG']

        with self.assertRaises(Http404) as _:
            self.middleware_instance.process_request(request)
            conf_helper_mock.get_value.assert_called_once()
            conf_helper_mock.get_all_orgs.assert_called_once()


class AvailableScreenMiddlewareTest(TestCase):
    """
    Testing the middleware AvailableScreenMiddleware
    """
    def setUp(self):
        """ setup """
        self.request_factory = RequestFactory()
        self.middleware_instance = AvailableScreenMiddleware()

    @mock.patch('eox_tenant.middleware.theming_helper')
    @mock.patch('eox_tenant.middleware.HttpResponseNotFound')
    def test_request_in_site(self, http_resp_not_found_mock, theming_helper_mock):
        """
        Test when the request is in a site/microsite
        """
        request = self.request_factory.get('/custom/path/')
        theming_helper_mock.is_request_in_themed_site.return_value = True
        result = self.middleware_instance.process_request(request)
        theming_helper_mock.is_request_in_themed_site.assert_called_once()
        http_resp_not_found_mock.assert_not_called()
        self.assertIsNone(result)

    @override_settings(FEATURES={
        'USE_MICROSITE_AVAILABLE_SCREEN': True,
    })
    @mock.patch('eox_tenant.middleware.get_edxmako_module')
    @mock.patch('eox_tenant.middleware.theming_helper')
    @mock.patch('eox_tenant.middleware.HttpResponseNotFound')
    def test_request_triggers_not_found(
        self, http_resp_not_found_mock, theming_helper_mock, _
    ):
        """
        Test when the not found response is triggered
        """
        request = self.request_factory.get('/custom/path/')
        http_host = 'my.custom.host'
        request.META['HTTP_HOST'] = http_host
        theming_helper_mock.is_request_in_themed_site.return_value = False
        http_resp_not_found_mock.return_value = 'redirect_response'

        result = self.middleware_instance.process_request(request)
        theming_helper_mock.is_request_in_themed_site.assert_called_once()
        http_resp_not_found_mock.assert_called_once()
        self.assertEqual(result, 'redirect_response')


class CurrentSiteMiddlewareTest(TestCase):
    """
    Test eox-tenant CurrentSiteMiddleware.
    """

    def setUp(self):
        """ Setup. """
        self.request_factory = RequestFactory(SERVER_NAME='test-domain.com')
        self.middleware_instance = CurrentSiteMiddleware()

        Site.objects.create(
            domain='test-domain.com',
            name='test-site',
        )

    @mock.patch('eox_tenant.middleware.TenantSiteConfigProxy')
    def test_override_site_configuration(self, create_site_mock):
        """
        Test that the Site object has the right configuration.
        """
        with self.settings(ALLOWED_HOSTS=['test-domain.com']):
            request = self.request_factory.get('custom/path/')
            new_configuration = 'new_configuration'
            create_site_mock.return_value = new_configuration

            self.middleware_instance.process_request(request)

            create_site_mock.assert_called_once()
            self.assertEqual(request.site.configuration, new_configuration)  # pylint: disable=no-member
