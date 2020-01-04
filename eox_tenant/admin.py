"""
Django admin page for microsite model
"""
from django.contrib import admin
from django.core.urlresolvers import reverse

from eox_tenant.models import Microsite, TenantConfig, Route


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
    search_fields = ('key', 'subdomain', )

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
        Read only method to calculate template dir attribute from config model.
        """
        # pylint: disable=broad-except
        try:
            themes_keys = ["name", "parent", "grandparent"]
            theme_config = TenantConfig.objects.get(external_key=microsite.key)
            theme_config = theme_config.theming_configs.get("THEME_OPTIONS", {})
            theme = theme_config.get("theme", {})
            values = [theme[key] for key in themes_keys if key in theme]
            if values:
                return " <- ".join(values)
            return "NOT CONFIGURED"
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


class TenantConfigAdmin(admin.ModelAdmin):
    """
    Tenant config model admin.
    """
    list_display = [
        'external_key',
        'domains',
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
    search_fields = ('external_key', 'route__domain', )

    def sitename(self, tenant_config):
        """
        Read only method to calculate sitename attribute from config model.
        """
        # pylint: disable=broad-except
        try:
            return tenant_config.lms_configs.get("SITE_NAME", "NOT CONFIGURED")
        except Exception as error:
            return str(error)

    def template_dir(self, tenant_config):
        """
        Read only method to calculate template dir attribute from config model.
        """
        # pylint: disable=broad-except
        try:
            themes_keys = ["name", "parent", "grandparent"]
            theme_config = tenant_config.theming_configs.get("THEME_OPTIONS", {})
            theme = theme_config.get("theme", {})
            values = [theme[key] for key in themes_keys if key in theme]
            if values:
                return " <- ".join(values)
            return "NOT CONFIGURED"
        except Exception as error:
            return str(error)

    def course_org_filter(self, tenant_config):
        """
        Read only method to calculate course org filter attribute from config model.
        """
        # pylint: disable=broad-except
        try:
            return tenant_config.lms_configs.get("course_org_filter", "NOT CONFIGURED")
        except Exception as error:
            return str(error)

    def ednx_signal(self, tenant_config):
        """
        Read only method to see if the site has activated the usage of signals.
        """
        # pylint: disable=broad-except
        try:
            return tenant_config.lms_configs.get("EDNX_USE_SIGNAL", "EMPTY")
        except Exception as error:
            return str(error)

    def domains(self, tenant_config):
        """
        Read only method to calculate the domain.
        """
        # pylint: disable=broad-except
        try:
            domains = [route.domain for route in tenant_config.route_set.all()]
            separator = '\n'
            return separator.join(domains)
        except Exception as error:
            return str(error)


class RouteAdmin(admin.ModelAdmin):
    """
    Route model admin.
    """
    raw_id_fields = [
        'config',
    ]

    list_display = [
        "domain",
        "config_link",
    ]

    search_fields = [
        "domain"
    ]

    def config_link(self, route):
        """
        Helper method to display a link to the related config model.
        """
        # pylint: disable=protected-access
        url = reverse('admin:%s_%s_change' % (route._meta.app_label, "tenantconfig"), args=[route.config.id])
        return u'<a href="%s">%s</a>' % (url, route.config.__unicode__())

    config_link.allow_tags = True
    config_link.short_description = "Configuration"


admin.site.register(Microsite, MicrositeAdmin)
admin.site.register(TenantConfig, TenantConfigAdmin)
admin.site.register(Route, RouteAdmin)
