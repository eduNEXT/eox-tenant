"""
The pipeline module defines custom Filters functions that are used in openedx-filters.
"""
from django.conf import settings
from openedx_filters import PipelineStep
from openedx_filters.learning.filters import CertificateRenderStarted

from eox_tenant.edxapp_wrapper.site_configuration_module import get_configuration_helpers
from eox_tenant.organizations import get_organizations
from eox_tenant.tenant_aware_functions.enrollments import filter_enrollments

configuration_helpers = get_configuration_helpers()


class FilterUserCourseEnrollmentsByTenant(PipelineStep):
    """
    Filter enrollments list by a tenant.
    """

    def run_filter(self, enrollments):  # pylint: disable=arguments-differ
        """
        Filter especific user course enrollments by tenant request.
        Example Usage:
        Add the following configurations to your configuration file
            "OPEN_EDX_FILTERS_CONFIG": {
                "org.openedx.learning.course_enrollment_queryset.requested.v1": {
                    "fail_silently": false,
                    "pipeline": [
                        "eox_tenant.filters.pipeline.FilterUserCourseEnrollmentsByTenant"
                    ]
                }
            }
        """
        tenant_enrollments = filter_enrollments(enrollments)
        return {"enrollments": tenant_enrollments}


class FilterRenderCertificatesByOrg(PipelineStep):
    """
    Stop certificate generation process raising a exception
    if course org is different to tenant orgs.
    Example usage:
    Add the following configurations to your configuration file:
        "OPEN_EDX_FILTERS_CONFIG": {
            "org.openedx.learning.certificate.render.started.v1": {
                "fail_silently": False,
                "pipeline": [
                    "eox_tenant.filters.pipeline.FilterRenderCertificatesByOrg"
                ]
            }
        }
    """

    def run_filter(self, context, custom_template, *args, **kwargs):  # pylint: disable=arguments-differ,unused-argument
        """Pipeline step that stops the certificate render process if course org is different to tenant orgs."""
        org_filter = get_organizations()
        # breakpoint()
        for org in org_filter:
            if context.get("course_id", "").startswith(f"course-v1:{org}+"):
                return
        raise CertificateRenderStarted.RenderAlternativeInvalidCertificate(
            "You can't generate a certificate from this site.",
        )


class OrgAwareLMSURLStudio(PipelineStep):
    """
    Generates a new LMS URL for asset URL generation based on the course organization settings.
    """

    def run_filter(self, url, org):  # pylint: disable=arguments-differ,unused-argument
        """
        Filter especific tenant aware link form Studio to the LMS.
        Example Usage:
        Add the following configurations to you configuration file
            "OPEN_EDX_FILTERS_CONFIG": {
                "org.openedx.course_authoring.lms.page.url.requested.v1": {
                    "fail_silently": false,
                    "pipeline": [
                        "eox_tenant.filters.pipeline.OrgAwareLMSURLStudio"
                    ]
                }
            }
        """
        lms_root = configuration_helpers.get_value_for_org(
            org,
            'LMS_ROOT_URL',
            settings.LMS_ROOT_URL
        )
        return {"url": lms_root, "org": org}


class OrgAwareCourseAboutPageURL(PipelineStep):
    """
    Generates a new course about URL based on the course organization settings.
    """

    def run_filter(self, url, org):  # pylint: disable=arguments-differ,unused-argument
        """
        The url looks like this:
        <LMS_ROOT>/courses/course-v1:org+course+number/about

        This method will filter the url to be tenant aware.
        Example Usage:
        Add the following configurations to you configuration file
            "OPEN_EDX_FILTERS_CONFIG": {
                "org.openedx.learning.course_about.page.url.requested.v1": {
                    "fail_silently": false,
                    "pipeline": [
                        "eox_tenant.filters.pipeline.OrgAwareCourseAboutPageURL"
                    ]
                },
            }
        """
        lms_root = configuration_helpers.get_value_for_org(
            org,
            'LMS_ROOT_URL',
            settings.LMS_ROOT_URL
        )
        course_about_url = url.replace(settings.LMS_ROOT_URL, lms_root)
        return {"url": course_about_url, "org": org}
