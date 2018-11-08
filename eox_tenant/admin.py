"""
Django admin page for microsite model
"""
from django.contrib import admin

from .models import Microsite


class MicrositeAdmin(admin.ModelAdmin):
    """
    TODO: add me
    """
    list_display = [
        'key',
        'subdomain',
        'sitename',
        'template_dir',
        'course_org_filter',
    ]
    readonly_fields = (
        'sitename',
        'template_dir',
        'course_org_filter',
    )
    search_fields = ('key', 'subdomain', 'values', )

    def sitename(self, microsite):
        """
        TODO: add me
        """
        # pylint: disable=broad-except
        try:
            return microsite.values.get('SITE_NAME', "NOT CONFIGURED")
        except Exception, error:
            return unicode(error)

    def template_dir(self, microsite):
        """
        TODO: add me
        """
        # pylint: disable=broad-except
        try:
            return microsite.values.get('template_dir', "NOT CONFIGURED")
        except Exception, error:
            return unicode(error)

    def course_org_filter(self, microsite):
        """
        TODO: add me
        """
        # pylint: disable=broad-except
        try:
            return microsite.values.get('course_org_filter', "NOT CONFIGURED")
        except Exception, error:
            return unicode(error)


admin.site.register(Microsite, MicrositeAdmin)
