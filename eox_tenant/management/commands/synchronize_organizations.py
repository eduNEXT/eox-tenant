"""
This module contains the command class to synchronize the
course_org_filter values with the organizations field.
"""
import logging
from time import sleep

from django.core.management.base import BaseCommand, CommandError

from eox_tenant import models
from eox_tenant.utils import synchronize_tenant_organizations

LOGGER = logging.getLogger(__name__)


class Command(BaseCommand):
    """
    Synchronize organizations.
    """
    help = """
        This command will synchronize the organizations field with
        the value in 'course_org_filter'.

        Usage Example:
        python manage.py lms synchronize_organizations --model TenantConfig
    """

    def add_arguments(self, parser):
        """
        The model parameter is optional.
        """
        parser.add_argument(
            "--model",
            type=str,
            required=False,
            dest="model"
        )

    def handle(self, *args, **options):
        """
        Synchronize  course_org_filter with organizations field.
        """
        option_model = options.get("model")
        valid_models = ["TenantConfig", "Microsite"]

        if option_model and option_model in valid_models:
            valid_models = [option_model]
        elif option_model:
            raise CommandError("Invalid model")

        for valid_model in valid_models:
            model = getattr(models, valid_model)
            queryset = model.objects.all()

            LOGGER.info("Synchronize %s %s registers.",
                        len(queryset),
                        valid_model,
                        )

            for instance in queryset:
                synchronize_tenant_organizations(instance)
                sleep(0.2)

        LOGGER.info("Successful Synchronization.")
