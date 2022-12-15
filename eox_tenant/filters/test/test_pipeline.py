"""
Test cases for Open edX Filters steps.
"""
from unittest.mock import MagicMock

import ddt
import mock
from django.test import TestCase, override_settings
from openedx_filters.learning.filters import CertificateRenderStarted
from openedx_filters.tooling import OpenEdxPublicFilter

from eox_tenant.filters.pipeline import FilterRenderCertificatesByOrg
from eox_tenant.tenant_aware_functions.enrollments import filter_enrollments


# This class was temporarily added while the filter is added in openedx-filters.
class CourseEnrollmentSiteFilterRequested(OpenEdxPublicFilter):
    """
    Custom class used to filter user's course enrollments by site.
    """

    filter_type = "org.openedx.learning.course_enrollments_site.filter.requested.v1"

    @classmethod
    def run_filter(cls, context):
        """
        Execute a filter with the signature specified.

        Arguments:
        context (QuerySet): list of all user's course enrollments.
        """
        data = super().run_pipeline(context=context)
        return data.get("context")


class FilterUserCourseEnrollmentsByTenantTestCase(TestCase):
    """
    FilterUserCourseEnrollmentsByTenant test cases.
    """

    def setUp(self):
        """This method creates Microsite objects in database"""

        # Creating mock enrollments
        orgs_for_enrolls = ["org1", "demo", "org3"]
        enrolls = []
        for org in orgs_for_enrolls:
            enroll_mock = MagicMock()
            enroll_mock.course_id.org = org
            enrolls.append(enroll_mock)
        self.course_enrollments = enrolls

    @override_settings(
        OPEN_EDX_FILTERS_CONFIG={
            "org.openedx.learning.course_enrollments_site.filter.requested.v1": {
                "fail_silently": False,
                "pipeline": [
                    "eox_tenant.filters.pipeline.FilterUserCourseEnrollmentsByTenant"
                ],
            }
        }
    )
    @mock.patch("eox_tenant.tenant_aware_functions.enrollments.get_theming_helpers")
    @mock.patch(
        "eox_tenant.tenant_aware_functions.enrollments.get_configuration_helpers"
    )
    def test_filter_user_course_enrollments(
        self, get_conf_helpers_mock, get_theming_helpers_mock
    ):
        """
        Test that filter user course enrollments are made by site.
        """
        results_get_value = {"course_org_filter": ["demo"]}

        def side_effect_get_value(key, default=None):
            """
            Mock side effect
            """
            return results_get_value.get(key, default)

        conf_helpers_mock = MagicMock()
        theming_helpers_mock = MagicMock()
        conf_helpers_mock.get_value.side_effect = side_effect_get_value
        theming_helpers_mock.is_request_in_themed_site.return_value = True

        get_conf_helpers_mock.return_value = conf_helpers_mock
        get_theming_helpers_mock.return_value = theming_helpers_mock

        expected_result = filter_enrollments(self.course_enrollments)

        result = CourseEnrollmentSiteFilterRequested.run_filter(
            context=self.course_enrollments
        )
        expected_result = list(expected_result)
        result = list(result)

        self.assertListEqual(expected_result, result)
        self.assertEqual(expected_result[0].course_id.org, result[0].course_id.org)

    @override_settings(
        OPEN_EDX_FILTERS_CONFIG={
            "org.openedx.learning.course_enrollments_site.filter.requested.v1": {
                "fail_silently": False,
                "pipeline": [
                    "eox_tenant.filters.pipeline.FilterUserCourseEnrollmentsByTenant"
                ],
            }
        }
    )
    @mock.patch("eox_tenant.tenant_aware_functions.enrollments.get_theming_helpers")
    @mock.patch(
        "eox_tenant.tenant_aware_functions.enrollments.get_configuration_helpers"
    )
    def test_filter_user_not_course_enrollments(
        self, get_conf_helpers_mock, get_theming_helpers_mock
    ):
        """
        Test filter when a user is not enroll in any course in the site.
        """
        results_get_value = {}

        def side_effect_get_value(key, default=None):
            """
            Mock side effect
            """
            return results_get_value.get(key, default)

        conf_helpers_mock = MagicMock()
        theming_helpers_mock = MagicMock()
        conf_helpers_mock.get_value.side_effect = side_effect_get_value
        theming_helpers_mock.is_request_in_themed_site.return_value = True
        conf_helpers_mock.get_all_orgs.return_value = ["org1", "demo", "org3"]

        get_conf_helpers_mock.return_value = conf_helpers_mock
        get_theming_helpers_mock.return_value = theming_helpers_mock

        expected_result = filter_enrollments(self.course_enrollments)

        result = CourseEnrollmentSiteFilterRequested.run_filter(
            context=self.course_enrollments
        )

        self.assertListEqual(list(expected_result), list(result))


@ddt.ddt
class FilterRenderCertificatesByOrgTestCase(TestCase):
    """Test FilterRenderCertificatesByOrg that prevent certificates
    render if course org differs from tenant orgs."""

    @mock.patch("eox_tenant.filters.pipeline.get_organizations")
    @ddt.data(
        [["demo"], True],
        [["eduNEXT"], False],
        [[], False],
        [["eduNEXT", "demo"], True],
    )
    @ddt.unpack
    def test_filter_render_certificates_by_org(self, organizations, render, mock_get_organizations):
        """Test the certificates render if course org differs from tenant orgs.

        Args:
            organizations (list): a list of tenant organization names.
            render (bool): this specifies whether to render or not.
            mock_get_organizations (patch): mock for get_organizations method.

        In the ddt data the following structure is being passed:
        [organizations, render]

        Expected result:
        - The get_organizations method is called once.
        - Raise an exception if the course org (ex: demo) differs from tenant org (passed in ddt).
        """

        mock_get_organizations.return_value = organizations
        context = {"course_id": "course-v1:demo+01+01"}

        if not render:
            with self.assertRaises(CertificateRenderStarted.RenderAlternativeInvalidCertificate):
                FilterRenderCertificatesByOrg.run_filter(self, context, {})
                mock_get_organizations.assert_called_once()
        else:
            FilterRenderCertificatesByOrg.run_filter(self, context, {})
            mock_get_organizations.assert_called_once()
