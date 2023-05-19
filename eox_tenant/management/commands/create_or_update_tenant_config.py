"""
Create or updates the TenantConfig for given routes.
"""

import codecs
import json
import logging

from django.core.management import BaseCommand
from jsonfield.fields import JSONField
import six

from eox_tenant.models import Route, TenantConfig

LOG = logging.getLogger(__name__)


def load_json_from_file(filename):
    """
    Loads json content from file.
    """
    with codecs.open(filename, encoding='utf-8') as file:
        return json.load(file)


class Command(BaseCommand):
    """
    Management command to create or update TenantConfig.
    """
    help = 'Create or update TenantConfig'

    def add_arguments(self, parser):
        parser.add_argument(
            '--external-key',
            action='store',
            dest='external_key',
            required=True,
            type=str,
            help='External key of the tenant config'
        )
        parser.add_argument('routes', nargs='+', help='Routes to link to this tenant config')

        parser.add_argument(
            '--config',
            type=json.loads,
            help="Enter JSON tenant configurations",
            required=False
        )
        parser.add_argument(
            '-f',
            '--config-file',
            type=load_json_from_file,
            dest='config_file_data',
            help="Enter the path to the JSON file containing the tenant configuration",
            required=False
        )

    def merge_dict(self, base_dict: dict, override: dict):
        """
        Merge two nested dicts.
        """
        for key, value in override.items():
            if isinstance(value, dict):
                merged = base_dict.get(key, {}).copy()
                merged.update(value)
                base_dict[key] = merged
                continue
            base_dict[key] = value
        return base_dict


    def handle(self, *args, **options):
        """
        Create or update TenantConfig and link related routes.
        """
        external_key = options['external_key']
        routes = options['routes']
        configuration = options.get('config')
        config_file_data = options.get('config_file_data')
        tenant_configuration_values = configuration or config_file_data
        # pylint: disable=no-member,protected-access
        external_key_length = TenantConfig._meta.get_field("external_key").max_length
        if external_key:
            if len(str(external_key)) > external_key_length:
                LOG.warning(
                    "The external_key %s is too long, truncating to %s"
                    " characters. Please update external_key in admin.",
                    external_key,
                    external_key_length
                )
            # trim name as the column has a limit of 63 characters
            external_key = external_key[:external_key_length]
        tenant, created = TenantConfig.objects.get_or_create(
            external_key=external_key,
        )
        if created:
            LOG.info("Tenant does not exist. Created new tenant: '%s'", tenant.external_key)
        else:
            LOG.info("Found existing tenant for: '%s'", tenant.external_key)

        # split out lms, studio, theme, meta from configuration json
        if tenant_configuration_values:
            for field in TenantConfig._meta.get_fields():
                if isinstance(field, JSONField):
                    name = field.name
                    value = tenant_configuration_values.get(name)
                    if value:
                        base_value = getattr(tenant, name, {})
                        merged = self.merge_dict(base_value, value)
                        setattr(tenant, name, merged)

            tenant.save()
        # next add routes and link them
        for route in routes:
            route, created = Route.objects.update_or_create(
                domain=route,
                defaults={"config": tenant}
            )
            if created:
                LOG.info("Route does not exist. Created new route: '%s'", route.domain)
            else:
                LOG.info("Found existing route for: '%s'", route.domain)
