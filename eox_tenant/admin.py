"""
Django admin page for microsite model
"""
from django.contrib import admin

from eox_tenant.models import Redirection, Microsite


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
        'ednx_signal',
    ]
    readonly_fields = (
        'sitename',
        'template_dir',
        'course_org_filter',
        'ednx_signal',
    )
    search_fields = ('key', 'subdomain', 'values', )

    def sitename(self, microsite):
        """
        TODO: add me
        """
        # pylint: disable=broad-except
        try:
            return microsite.values.get('SITE_NAME', "NOT CONFIGURED")
        except Exception as error:
            return str(error)

    def template_dir(self, microsite):
        """
        TODO: add me
        """
        # pylint: disable=broad-except
        try:
            return microsite.values.get('template_dir', "NOT CONFIGURED")
        except Exception as error:
            return str(error)

    def course_org_filter(self, microsite):
        """
        TODO: add me
        """
        # pylint: disable=broad-except
        try:
            return microsite.values.get('course_org_filter', "NOT CONFIGURED")
        except Exception as error:
            return str(error)

    def ednx_signal(self, microsite):
        """
        Read only method to see if the site has activated the usage of signals
        """
        # pylint: disable=broad-except
        try:
            return microsite.values.get('EDNX_USE_SIGNAL', "EMPTY")
        except Exception as error:
            return str(error)


class RedirectionAdmin(admin.ModelAdmin):
    """
    Admin view to see and edit edunext redirection objects.
    """
    list_display = [
        'target',
        'domain',
        'scheme',
    ]
    search_fields = ('target', 'domain',)


admin.site.register(Microsite, MicrositeAdmin)
admin.site.register(Redirection, RedirectionAdmin)
