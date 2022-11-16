"""
The pipeline module defines custom Filters functions that are used in openedx-filters.
"""
from openedx_filters import PipelineStep

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
