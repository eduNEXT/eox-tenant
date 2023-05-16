"""
This module contains the command class to modify the values
from a tenant so that we can add, remove of edit tenants in bulk.
"""
from __future__ import unicode_literals

import ast
import logging

from django.core.management.base import BaseCommand, CommandError
from six.moves import input

from eox_tenant.models import Microsite

LOGGER = logging.getLogger(__name__)


def tenant_interpolation(value, tenant):
    """
    Uses the information on the tenant to interpolate strings
    """
    context = {
        "subdomain": tenant.subdomain,
        "key": tenant.key,
    }
    context.update(tenant.values)

    return value.format(**context)


def cast_likely_type(value):
    """
    Makes strings like "True" or "None" evaluate to real Bool or None types.
    """
    try:
        # We try to cast is as the most likely type
        return ast.literal_eval(value)
    except Exception:  # pylint: disable=broad-except
        return value


class Command(BaseCommand):
    """
    Main class handling the execution of the command to alter the sites by adding or removing keys

    Examples:
    - python manage.py lms edit_tenant_values --add EDNX_USE_SIGNAL True
    - python manage.py lms edit_tenant_values --delete EDNX_USE_SIGNAL

    Advanced example:
    - python manage.py lms edit_tenant_values --pattern yoursite.com -v 2 --add NESTED.KEY.NAME {interpolated_value} -f
    """
    help = """
        Exposes a cli to perform bulk modification of eox_tenant sites
    """

    def add_arguments(self, parser):
        """
        Cli definition
        """
        # Positional arguments
        # None for now

        # Named (optional) arguments
        parser.add_argument(
            '--add',
            nargs=2,
            dest='add',
        )
        parser.add_argument(
            '--delete',
            nargs="*",
            dest='delete',
        )
        parser.add_argument(
            '--pattern',
            nargs=1,
            dest='pattern',
        )
        parser.add_argument(
            '-f',
            '--force',
            dest='force',
            action='store_true',
        )

    def handle(self, *args, **options):
        """
        Main cli method to iterate over the sites and perform the required modifications
        """

        if options['verbosity'] > 1:
            LOGGER.info('Options recognized from the command call')
            LOGGER.info(options)

        query = Microsite.objects.all()

        if options['pattern']:
            query = query.filter(subdomain__icontains=options['pattern'][0])

        LOGGER.info("This command will affect the following sites:")
        for tenant in query:
            LOGGER.info("{} on: {}".format(tenant, tenant.subdomain))

        if not options['force']:
            user_response = input("Continue? y/n: ")
            if user_response != 'y':
                LOGGER.info("No tenants where modified")
                raise CommandError("Canceled by user")

        for tenant in query:
            if options['delete']:
                self.action_delete(tenant, options['delete'])

            if options['add']:
                self.action_add(tenant, options['add'][0], options['add'][1])

    def action_delete(self, tenant, keys):
        """
        Handles removal of keys in the values dict.
        Keys will be treated as nested dictionaries according
        to a dot separated notations
        """
        for key in keys:
            try:
                chain = key.split('.')

                tmp = tenant.values
                last = chain[-1]
                for link in chain[:-1]:
                    tmp = tmp[link]
                tmp.pop(last)

                tenant.save()
            except KeyError:
                LOGGER.info("Could not find key: {} on site {}".format(key, tenant))

    def action_add(self, tenant, key, value):
        """
        Handles addition to the values dict.
        Keys will be treated as nested dictionaries according
        to a dot separated notations
        """
        try:
            chain = key.split('.')

            tmp = tenant.values
            last = chain[-1]
            for link in chain[:-1]:
                try:
                    tmp = tmp[link]
                except KeyError:
                    tmp[link] = {}
                    tmp = tmp[link]
            interpolated_value = tenant_interpolation(value, tenant)
            tmp[last] = cast_likely_type(interpolated_value)

            tenant.save()
        except Exception:  # pylint: disable=broad-except
            LOGGER.info("Could not add key {} to site {}".format(key, tenant))
