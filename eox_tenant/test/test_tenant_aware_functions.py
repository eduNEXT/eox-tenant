"""This module include a class that checks the tenant aware functions"""
import mock

from django.test import TestCase, override_settings

from eox_tenant.tenant_aware_functions.enrollments import filter_enrollments


class TenantAwareFunctionsTestCase(TestCase):
    """ This class checks the command change_domain.py"""

    def setUp(self):
        """This method creates Microsite objects in database"""

        # Creating mock enrollments
        orgs_for_enrolls = ['org1', 'org2', 'org3', 'org3']
        enrolls = []
        for org in orgs_for_enrolls:
            enroll_mock = mock.MagicMock()
            enroll_mock.course_id.org = org
            enrolls.append(enroll_mock)
        self.enrolls = enrolls

    @override_settings(EOX_TENANT_SKIP_FILTER_FOR_TESTS=True)
    def test_filter_enrollments_dont_filter(self):
        """
        Test the case when the filter is not applied because the
        EOX_TENANT_SKIP_FILTER_FOR_TESTS setting is activated
        """
        result = filter_enrollments(self.enrolls)
        self.assertEqual(len(list(result)), 4)

    @mock.patch('eox_tenant.tenant_aware_functions.enrollments.get_microsite')
    def test_filter_enrollments_not_request_in_microsite(self, get_microsite_mock):
        """
        Test the case when the request is not in a microsite (filter is not applied)
        """
        microsite_module_mock = mock.MagicMock()
        microsite_module_mock.is_request_in_microsite.return_value = False
        get_microsite_mock.return_value = microsite_module_mock

        result = filter_enrollments(self.enrolls)
        self.assertEqual(len(list(result)), 4)

        microsite_module_mock.is_request_in_microsite.assert_called_once()

    @mock.patch('eox_tenant.tenant_aware_functions.enrollments.get_microsite')
    def test_filter_enrollments_function(self, get_microsite_mock):
        """
        Test that the filter works properly
        """
        results_get_value = {
            'course_org_filter': ['org2']
        }

        def side_effect_get_value(key, default=None):
            """
            Mock side effect
            """
            return results_get_value.get(key, default)

        microsite_module_mock = mock.MagicMock()
        microsite_module_mock.get_value.side_effect = side_effect_get_value
        microsite_module_mock.is_request_in_microsite.return_value = True
        get_microsite_mock.return_value = microsite_module_mock

        result = filter_enrollments(self.enrolls)
        list_result = list(result)
        self.assertEqual(len(list_result), 1)
        self.assertEqual(list_result[0].course_id.org, 'org2')

        microsite_module_mock.is_request_in_microsite.assert_called_once()
        microsite_module_mock.get_value.assert_called_once()

    @mock.patch('eox_tenant.tenant_aware_functions.enrollments.get_microsite')
    def test_filter_enrollments_no_org_filter(self, get_microsite_mock):
        """
        Test the case when the microsite does not have a course_org_filter
        """
        results_get_value = {}

        def side_effect_get_value(key, default=None):
            """
            Mock side effect
            """
            return results_get_value.get(key, default)

        microsite_module_mock = mock.MagicMock()
        microsite_module_mock.get_value.side_effect = side_effect_get_value
        microsite_module_mock.is_request_in_microsite.return_value = True
        microsite_module_mock.get_all_orgs.return_value = ['org1', 'org2', 'org3', 'org3']
        get_microsite_mock.return_value = microsite_module_mock

        result = filter_enrollments(self.enrolls)
        self.assertEqual(len(list(result)), 0)

        microsite_module_mock.is_request_in_microsite.assert_called_once()
        microsite_module_mock.get_value.assert_called_once()
        microsite_module_mock.get_all_orgs.assert_called_once()
