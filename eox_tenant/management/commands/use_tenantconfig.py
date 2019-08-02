"""
This module contains the command class to migrate the site
configurations and microsites data to the TenantConfig .
"""
from django.contrib.sites.models import Site
from django.core.management.base import BaseCommand, CommandError

from eox_tenant.models import Microsite, TenantConfig, Route
from eox_tenant.utils import fasthash


class Command(BaseCommand):

    """
    This class contains the methods to create
    tenant configs from sites and microsites.
    """
    help = """This function will iterate over all microsites an site-configuration objects
            an create a tenant config and the route objects with their information."""

    def add_arguments(self, parser):
        parser.add_argument('--site-configurations', action="store_true", dest='siteconfigurations', default=False)
        parser.add_argument('--microsites', action="store_true", dest='microsites', default=False)

    def handle(self, *args, **options):
        """
        This method will iterate over all microsites and site objects to
        create the route and the tenant config objects with their information.
        """

        if not options['microsites'] and not options['siteconfigurations']:
            raise CommandError("Use --microsites and/or --site-configurations options.")

        if options['microsites']:

            # Iterating microsites objects
            for microsite in Microsite.objects.all():  # pylint: disable=no-member
                try:
                    route = Route.objects.get(domain=microsite.subdomain)  # pylint: disable=no-member
                except Route.DoesNotExist:  # pylint: disable=no-member
                    route = None

                try:
                    tenant = TenantConfig.objects.get(external_key=microsite.key)
                except TenantConfig.DoesNotExist:  # pylint: disable=no-member
                    tenant = None

                #  If there is a route do nothing.
                if route:
                    continue

                if not tenant:
                    tenant = TenantConfig(
                        external_key=microsite.key,
                        lms_configs=microsite.values)
                    tenant.save()

                route = Route(domain=microsite.subdomain, config=tenant)
                route.save()

        if options['siteconfigurations']:

            # Iterating django sites objects
            for site in Site.objects.all():

                # Only do the changes for the site_configurations enabled
                try:
                    if not site.configuration.enabled:
                        continue
                except AttributeError:
                    continue

                try:
                    route = Route.objects.get(domain=site.domain)  # pylint: disable=no-member
                except Route.DoesNotExist:  # pylint: disable=no-member
                    route = None

                api_key = fasthash(site.domain)

                try:
                    tenant = TenantConfig.objects.get(external_key=api_key)
                except TenantConfig.DoesNotExist:  # pylint: disable=no-member
                    tenant = None

                # If there is a route do nothing.
                if route:
                    continue

                if not tenant:
                    tenant = TenantConfig(
                        external_key=api_key,
                        lms_configs=site.configuration.values)
                    tenant.save()

                route = Route(domain=site.domain, config=tenant)
                route.save()
