"""
This module contains the command class to change
the subdomain from prod domains to stage versions.
"""
import json
import logging

from django.conf import settings
from django.contrib.sites.models import Site
from django.core.management.base import BaseCommand

from eox_tenant.edxapp_wrapper.get_common_util import strip_port_from_host
from eox_tenant.edxapp_wrapper.users import get_user_signup_source
from eox_tenant.models import Microsite

try:
    from urllib.parse import urlparse  # Python 3 Compatible
except ImportError:
    from urlparse import urlparse  # Python 2 Compatible


LOGGER = logging.getLogger(__name__)
UserSignupSource = get_user_signup_source()


class Command(BaseCommand):
    """
    This class contains the methods to change
    microsite prod domains to a stage versions.
    """
    help = help = """
        This function will iterate over all microsites objects
        to change microsite prod domains to a stage versions.
        Usage Example:
        python manage.py lms change_domain ".i.stage.ednx.co" ".i.ecom.ednx.co" --signupsources --settings=production
    """
    suffix_stage_domain = ""
    suffix_stage_ecommerce_domain = ""

    def add_arguments(self, parser):
        """
        Add optional domain from the line command
        """
        default_name_value = getattr(settings, 'CHANGE_DOMAIN_DEFAULT_SITE_NAME', '')
        parser.add_argument('suffix_domain', type=str,
                            nargs='?', default=default_name_value)
        parser.add_argument('suffix_ecommerce_domain', type=str,
                            nargs='?', default=default_name_value)
        parser.add_argument('--signupsources', action="store_true",
                            dest='signupsources', default=False)

    def handle(self, *args, **options):
        """
        This method will iterate over all microsites, sites and signupsources
        objects to change microsite prod domains to a stage versions.
        """
        self.suffix_stage_domain = options['suffix_domain']
        self.suffix_stage_ecommerce_domain = options['suffix_ecommerce_domain']

        # Changing microsites objects
        for microsite in Microsite.objects.all():

            stage_domain = self.change_subdomain(microsite.subdomain)

            if not stage_domain:
                continue

            prod_subdomain = microsite.subdomain
            microsite.subdomain = stage_domain

            # If the microsite has no values, just save and go to the next
            if not microsite.values:
                microsite.save()
                continue

            # Getting ecommerce urls before modifying the values dict
            ecommerce_public_url_root = microsite.values.get('ECOMMERCE_PUBLIC_URL_ROOT')
            ecommerce_api_url = microsite.values.get('ECOMMERCE_API_URL')

            configs_string = json.dumps(microsite.values)
            # Replacing all concidences of the prod domain inside the
            # configurations by the stage domain
            modified_configs_string = configs_string.replace(
                prod_subdomain,
                stage_domain
            )
            microsite.values = json.loads(modified_configs_string)
            # Modifying ecommerce urls
            if ecommerce_public_url_root and ecommerce_api_url:
                microsite.values['ECOMMERCE_PUBLIC_URL_ROOT'] = self.change_url(
                    ecommerce_public_url_root,
                    self.suffix_stage_ecommerce_domain
                ) or ecommerce_public_url_root
                microsite.values['ECOMMERCE_API_URL'] = self.change_url(
                    ecommerce_api_url,
                    self.suffix_stage_ecommerce_domain
                ) or ecommerce_api_url

            microsite.save()

        # Changing django sites objects
        for site in Site.objects.all():

            stage_domain = self.change_subdomain(site.domain)

            if not stage_domain:
                continue

            site.domain = stage_domain
            site.name = stage_domain
            site.save()

        if options['signupsources']:
            for signupsource in UserSignupSource.objects.all():

                stage_domain = self.change_subdomain(signupsource.site)

                if not stage_domain:
                    continue

                signupsource.site = stage_domain
                signupsource.save()

    def change_subdomain(self, subdomain, suffix_domain=None):
        """
        Transforming the domain to format
        my-site-domain-{suffix_domain}
        """
        if not suffix_domain:
            suffix_domain = self.suffix_stage_domain

        domain = strip_port_from_host(subdomain)

        # Don't bother on changing anything if the suffix is correct
        if domain.endswith(suffix_domain):
            return ""

        port = None
        if ':' in subdomain:
            port = subdomain.split(':')[1]

        pre_formatted = "{}-{}"
        if suffix_domain.startswith("."):
            pre_formatted = "{}{}"
        try:
            stage_domain = pre_formatted.format(
                domain.replace('.', '-'),
                suffix_domain
            )
            if port:
                stage_domain += ':' + port
        except TypeError as exc:
            stage_domain = ""
            message = u"Unable to define stage url for site {}".format(
                subdomain
            )
            LOGGER.warning(message)
            LOGGER.error(exc.message)  # pylint: disable=no-member
        return stage_domain

    def change_url(self, url, suffix_domain=None):
        """
        Transforming the url to format
        http://my-site-domain-{suffix_domain}/path
        """
        parsed_url = urlparse(url)
        url_domain = parsed_url.netloc
        changed_domain = self.change_subdomain(url_domain, suffix_domain)

        if not changed_domain:
            return ""

        new_parsed_url = parsed_url._replace(netloc=changed_domain)
        return new_parsed_url.geturl()
