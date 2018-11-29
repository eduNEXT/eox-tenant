"""
This module contains the command class to change
the subdomain from prod domains to stage versions.
"""
import json
import logging

from django.conf import settings
from django.core.management.base import BaseCommand

from eox_tenant.models import Microsite
LOGGER = logging.getLogger(__name__)


class Command(BaseCommand):

    """
    This class contains the methods to change
    microsite prod domains to a stage versions.
    """
    help = """This function will iterate over all microsites objects
            to change microsite prod domains to a stage versions."""
    suffix_stage_domain = ""

    def add_arguments(self, parser):
        """
        Add optional domain from the line command
        """
        default_name_value = getattr(settings, 'CHANGE_DOMAIN_DEFAULT_SITE_NAME', '')
        parser.add_argument('suffix_domain', type=str,
                            nargs='?', default=default_name_value)

    def handle(self, *args, **options):
        """
        This method will iterate over all microsites
        objects to change microsite prod domains to a stage versions.
        """

        self.suffix_stage_domain = options['suffix_domain']

        for microsite in Microsite.objects.all():  # pylint: disable=no-member

            # Don't bother on changing anything if the suffix is correct
            if microsite.subdomain.endswith(self.suffix_stage_domain):
                continue

            stage_domain = self.change_subdomain(microsite.subdomain)

            if not stage_domain:
                continue

            prod_subdomain = microsite.subdomain
            microsite.subdomain = stage_domain

            configs_string = json.dumps(microsite.values)
            # Replacing all concidences of the prod domain inside the
            # configurations by the stage domain
            modified_configs_string = configs_string.replace(
                prod_subdomain,
                stage_domain
            )
            microsite.values = json.loads(modified_configs_string)
            microsite.save()

    def change_subdomain(self, subdomain):
        """
        Transforming the domain to format
        my-microsite-domain-{suffix_stage_domain}
        """

        try:
            stage_domain = "{}-{}".format(
                subdomain.replace('.', '-'),
                self.suffix_stage_domain
            )
        except TypeError as exc:
            stage_domain = ""
            message = u"Unable to define stage url for microsite {}".format(
                subdomain
            )
            # pylint: disable=no-member
            LOGGER.warning(message)
            LOGGER.error(exc.message)
        return stage_domain
