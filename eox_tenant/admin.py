"""
Django admin page for microsite model
"""
from itertools import chain

from django import forms
from django.conf import settings
from django.contrib import admin
from django.db import models
from django.urls import reverse
from django.utils.safestring import mark_safe
from jsonfield.fields import JSONField

from eox_tenant.models import Microsite, Route, TenantConfig, TenantOrganization
from eox_tenant.widgets import JsonWidget


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
        'organizations',
    )
    formfield_overrides = {
        JSONField: {'widget': JsonWidget}
    }
    search_fields = ('key', 'subdomain', 'values')

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
        'organizations',
    )
    search_fields = ('external_key', 'route__domain', 'lms_configs', 'studio_configs', 'theming_configs', 'meta')
    formfield_overrides = {
        JSONField: {'widget': JsonWidget}
    }

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
            return tenant_config.lms_configs.get("template_dir", "NOT CONFIGURED")
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

    formfield_overrides = {
        models.ForeignKey: {'widget': forms.TextInput},
    }

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
        url = reverse(f'admin:{route._meta.app_label}_tenantconfig_change', args=[route.config.id])
        return mark_safe(f'<a href="{url}">{route.config.__unicode__()}</a>')

    config_link.allow_tags = True
    config_link.short_description = "Configuration"


class TenantOrganizationAdmin(admin.ModelAdmin):
    """TenantOrganization admin class.

    Define the basic attributes for searching and display.
    """

    list_display = [
        'name',
        'microsites',
        'tenants',
    ]
    readonly_fields = [
        'name',
        'microsites',
        'tenants',
    ]
    search_fields = [
        "name"
    ]
    list_per_page = 20
    # Prevent expensive duplicated COUNT query
    show_full_result_count = False

    def microsites(self, org):
        """Return links for the associated microsites.

        Args:
            org: TenantOrganization instance.

        Returns:
            String: Concatenated list of subdomains
        """
        domains = []
        microsites = Microsite.objects.filter(organizations=org)

        for microsite in microsites:
            url = reverse(
                f'admin:{microsite._meta.app_label}_microsite_change',  # pylint: disable=protected-access
                args=[microsite.id],
            )
            domains.append(f'<a href="{url}">{microsite.subdomain}</a>')

        return mark_safe('\n'.join(domains))

    def tenants(self, org):
        """Return links for the associated tenants.

        Args:
            org: TenantOrganization instance.

        Returns:
            String: Concatenated list of domains.
        """
        domains = []
        tenants = TenantConfig.objects.filter(organizations=org)

        for tenant in tenants:
            url = reverse(
                f'admin:{tenant._meta.app_label}_tenantconfig_change',  # pylint: disable=protected-access
                args=[tenant.id],
            )
            domains += [f'<a href="{url}">{route.domain}</a>' for route in tenant.route_set.all()]

        return mark_safe('\n'.join(domains))

    tenants.allow_tags = True
    microsites.allow_tags = True

    def get_search_results(self, request, queryset, search_term):
        """Perform a searching by using the organization name, microsite subdomain and route domain.

        Args:
            request: Current request.
            queryset: Queryset with the CertificateTemplate data.
            search_term: String with the filter value.

        Returns:
            Tuple containing a queryset to implement the search,
            and a boolean indicating if the results may contain duplicates.
        """
        queryset, _ = super().get_search_results(request, queryset, search_term)

        if search_term:
            tenant_orgs = Route.objects.filter(
                domain__icontains=search_term,
            ).values_list('config__organizations', flat=True).distinct()
            microsite_orgs = Microsite.objects.filter(
                subdomain__icontains=search_term,
            ).values_list('organizations', flat=True).distinct()

            queryset = queryset | TenantOrganization.objects.filter(id__in=chain(tenant_orgs, microsite_orgs))

        return queryset, _


if getattr(settings, "SERVICE_VARIANT", None) == "lms":
    admin.site.register(Microsite, MicrositeAdmin)
    admin.site.register(TenantConfig, TenantConfigAdmin)
    admin.site.register(Route, RouteAdmin)
    admin.site.register(TenantOrganization, TenantOrganizationAdmin)
