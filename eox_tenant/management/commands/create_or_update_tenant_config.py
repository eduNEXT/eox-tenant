"""
Create or updates the TenantConfig for given routes.
"""

import json
import logging

from django.core.management import BaseCommand
from jsonfield.fields import JSONField

from eox_tenant.models import Route, TenantConfig

LOG = logging.getLogger(__name__)


def load_json_from_file(filename):
    """
    Loads json content from file.
    """
    with open(filename, encoding='utf-8') as file:
        return json.load(file)


class Command(BaseCommand):
    """
    Management command to create or update TenantConfig.

    Examples:
    # create/update tenant config and link 2 routes
    - python manage.py create_or_update_tenant_config --external-key lacolhost.com \
        --config '{"lms_configs": {"PLATFORM_NAME": "Lacolhost", "CONTACT_EMAIL": "edx@example.com"}}' \
        lacolhost.com preview.lacolhost.com

    # Override existing lms_configs under a tenant, for example, below command will overwrite `lms_configs`
    # with given dictionary instead of updating it.
    - python manage.py create_or_update_tenant_config --external-key lacolhost.com \
        --config '{"lms_configs": {"PLATFORM_NAME": "New name"}}' lacolhost.com preview.lacolhost.com

    # create/update tenant config using json file
    - python manage.py create_or_update_tenant_config --external-key lacolhost.com \
        --config-file /tmp/lms.json lacolhost.com preview.lacolhost.com

    # Link studio.lacolhost.com route to existing/empty tenant config with given external key
    - python manage.py create_or_update_tenant_config --external-key lacolhost.com studio.lacolhost.com

    """
    help = 'Create or update TenantConfig'

    def add_arguments(self, parser):
        parser.add_argument(
            '--external-key',
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
        parser.add_argument(
            '--override',
            dest='override',
            action='store_true',
            required=False
        )

    def merge_dict(self, base_dict, override):
        """
        Merge two nested dicts.
        """
        if isinstance(base_dict, dict) and isinstance(override, dict):
            for key, value in override.items():
                base_dict[key] = self.merge_dict(base_dict.get(key, {}), value)
            return base_dict

        return override

    def handle(self, *args, **options):     # pylint: disable=too-many-branches
        """
        Create or update TenantConfig and link related routes.
        """
        data = {
            "external_key": options['external_key'],
            "routes": options['routes'],
            "tenant_configuration_values": options.get('config') or options.get('config_file_data'),
            "override": options.get('override'),
        }
        # pylint: disable=no-member,protected-access
        external_key_length = TenantConfig._meta.get_field("external_key").max_length
        if data["external_key"]:
            if len(str(data["external_key"])) > external_key_length:
                LOG.warning(
                    "The external_key %s is too long, truncating to %s"
                    " characters. Please update external_key in admin.",
                    data["external_key"],
                    external_key_length
                )
            # trim name as the column has a limit of 63 characters
            data["external_key"] = data["external_key"][:external_key_length]
        tenant, created = TenantConfig.objects.get_or_create(
            external_key=data["external_key"],
        )
        if created:
            LOG.info("Tenant does not exist. Created new tenant: '%s'", tenant.external_key)
        else:
            LOG.info("Found existing tenant for: '%s'", tenant.external_key)

        # split out lms, studio, theme, meta from configuration json
        if data["tenant_configuration_values"]:
            for field in TenantConfig._meta.get_fields():
                if isinstance(field, JSONField):
                    name = field.name
                    value = data["tenant_configuration_values"].get(name)
                    if not value:
                        continue
                    if data["override"]:
                        setattr(tenant, name, value)
                    else:
                        base_value = getattr(tenant, name, {})
                        merged = self.merge_dict(base_value, value)
                        setattr(tenant, name, merged)

            tenant.save()
        # next add routes and link them
        for route in data["routes"]:
            route, created = Route.objects.update_or_create(
                domain=route,
                defaults={"config": tenant}
            )
            if created:
                LOG.info("Route does not exist. Created new route: '%s'", route.domain)
            else:
                LOG.info("Found existing route for: '%s'", route.domain)
