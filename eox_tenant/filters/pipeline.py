"""
The pipeline module defines custom Filters functions that are used in openedx-filters.
"""
from openedx_filters import PipelineStep
from openedx_filters.learning.filters import CertificateRenderStarted

from eox_tenant.organizations import get_organizations
from eox_tenant.tenant_aware_functions.enrollments import filter_enrollments


class FilterUserCourseEnrollmentsByTenant(PipelineStep):
    """
    Filter enrollments list by a tenant.
    """

    def run_filter(self, context):  # pylint: disable=arguments-differ
        """
        Filter especific user course enrollments by tenant request.
        Example Usage:
        Add the following configurations to you configuration file
            "OPEN_EDX_FILTERS_CONFIG": {
                "org.openedx.learning.course_enrollments_site.filter.requested.v1": {
                    "fail_silently": false,
                    "pipeline": [
                        "eox_tenant.filters.pipeline.FilterUserCourseEnrollmentsByTenant"
                    ]
                }
            }
        """
        tenant_enrollments = filter_enrollments(context)
        return {"context": tenant_enrollments}


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
