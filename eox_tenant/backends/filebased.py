"""
Microsite backend that reads the configuration from a file
"""
import os.path

from django.conf import settings

# First try to import the core microsite_configuration base backend. The reason for this
# is that get_backed function defined in common/microsite_configuration/microsite.py from
# edx-platform validates that the configured backend classes MICROSITE_BACKEND and
# MICROSITE_TEMPLATE_BACKEND are children of microsite_configuration base backend classes,
# so basically this is avoiding that validation to fail. Eventually we will remove this try
# except and will import only our base backends to have less and less core dependencies
try:
    from microsite_configuration.backends.base import BaseMicrositeTemplateBackend
except ImportError:
    from .base import BaseMicrositeTemplateBackend
from microsite_configuration.microsite import get_value as microsite_get_value  # pylint: disable=import-error
from microsite_configuration.microsite import is_request_in_microsite  # pylint: disable=import-error


class EdunextCompatibleFilebasedMicrositeTemplateBackend(BaseMicrositeTemplateBackend):
    """
    Microsite backend that loads templates from filesystem using the configuration
    held before dogwood by edunext
    """
    def make_absolute_path(self, relative_path):
        """
        TODO: add me
        """
        return '/' + relative_path

    def get_template_path(self, relative_path, **kwargs):
        """
        Returns a path (string) to a Mako template, which can either be in
        an override or will just return what is passed in which is expected to be a string
        """

        leading_slash = kwargs.get('leading_slash', False)

        if not is_request_in_microsite():
            return '/' + relative_path if leading_slash else relative_path

        template_dir = str(microsite_get_value('template_dir', microsite_get_value('microsite_name')))

        if template_dir:
            search_path = os.path.join(
                settings.MICROSITE_ROOT_DIR,
                template_dir,
                'templates',
                relative_path
            )

            if os.path.isfile(search_path):
                path = '{0}/templates/{1}'.format(
                    template_dir,
                    relative_path
                )
                return '/' + path if leading_slash else path

        return '/' + relative_path if leading_slash else relative_path
