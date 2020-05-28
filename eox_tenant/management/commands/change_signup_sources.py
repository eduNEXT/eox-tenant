"""
This module contains the command class to change
masively the domain of the signupsources of a tenant.
"""

from django.core.management.base import BaseCommand

from eox_tenant.utils import move_signupsource


class Command(BaseCommand):
    """
    Move the signupsources from a domain into another domain.
    """
    help = """
        This command will change the domain of all the
         signupsources of a given domain with another domain.

        Usage Example:
        python manage.py lms change_signup_sources --from old.edunext.io --to new.edunext.io --settings=production
    """

    def add_arguments(self, parser):
        """
        Required old and new domain.
        """
        parser.add_argument('--from', type=str, required=True,
                            dest='old_domain')
        parser.add_argument('--to', type=str, required=True,
                            dest='new_domain')

    def handle(self, *args, **options):
        """
        Move the signupsources from a tenant to another domain.
        """
        old_domain = options['old_domain']
        new_domain = options['new_domain']

        move_signupsource(old_domain, new_domain)
