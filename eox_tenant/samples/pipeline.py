"""
Filters steps exemplifying how to:
    - Modify filter input
    - No operation
    - Halt process
"""

import copy
from collections import OrderedDict
from django.conf import settings
from django.core.exceptions import ImproperlyConfigured
from openedx_filters import PipelineStep
from openedx.core.djangoapps.site_configuration import helpers as configuration_helpers
from openedx.core.djangolib.markup import HTML, Text


import logging

class CustomFormatter(logging.Formatter):
    """Logging colored formatter, adapted from https://stackoverflow.com/a/56944256/3638629"""

    grey = '\x1b[38;21m'
    blue = '\x1b[38;5;39m'
    yellow = '\x1b[38;5;226m'
    red = '\x1b[38;5;196m'
    bold_red = '\x1b[31;1m'
    reset = '\x1b[0m'

    def __init__(self, fmt):
        super().__init__()
        self.fmt = fmt
        self.FORMATS = {
            logging.DEBUG: self.grey + self.fmt + self.reset,
            logging.INFO: self.blue + self.fmt + self.reset,
            logging.WARNING: self.yellow + self.fmt + self.reset,
            logging.ERROR: self.red + self.fmt + self.reset,
            logging.CRITICAL: self.bold_red + self.fmt + self.reset
        }

    def format(self, record):
        log_fmt = self.FORMATS.get(record.levelno)
        formatter = logging.Formatter(log_fmt)
        return formatter.format(record)


log = logging.getLogger(__name__)
fmt = '%(asctime)s | %(levelname)8s | %(message)s'

stdout_handler = logging.StreamHandler()
stdout_handler.setLevel(logging.DEBUG)
stdout_handler.setFormatter(CustomFormatter(fmt))
log.addHandler(stdout_handler)


class AddCustomFieldsBeforeRegistration(PipelineStep):
    """ Pipeline used to add custom fields to the registration form.

        Example usage:

        Add the following configurations to your configuration file:
                "OPEN_EDX_FILTERS_CONFIG": {
                    "org.openedx.learning.student.registration.render.started.v1": {
                        "fail_silently": false,
                        "pipeline": [
                            "eox_tenant.samples.pipeline.AddCustomFieldsBeforeRegistration"
                        ]
                    }
                }
    """

    def run_filter(self, form_desc):  # pylint: disable=arguments-differ
        """Run the pipeline filter."""

        log.critical("Running filter: %s", self.__class__.__name__)
        extra_fields = self._get_extra_fields()

        for field_name in extra_fields:
            extra_field = {"field_name": field_name}
            self._add_custom_field(
                form_desc,
                required=self._is_field_required(field_name),
                **extra_field
            )
        fields = form_desc.fields
        fields = [field['name'] for field in fields]

        field_order = configuration_helpers.get_value('REGISTRATION_FIELD_ORDER')
        if not field_order:
            field_order = settings.REGISTRATION_FIELD_ORDER or fields

        if set(fields) != set(field_order):
            difference = set(fields).difference(set(field_order))
            field_order.extend(sorted(difference))

        ordered_fields = []
        for field in field_order:
            for form_field in form_desc.fields:
                if field == form_field['name']:
                    ordered_fields.append(form_field)
                    break

        form_desc.fields = ordered_fields
        return form_desc

    def _get_extra_fields(self):
        """Returns the list of extra fields to include in the registration form.
        Returns:
            list of strings
        """
        extended_profile_fields = [field.lower() for field in getattr(settings, 'extended_profile_fields', [])]  # lint-amnesty, pylint: disable=line-too-long

        return list(OrderedDict.fromkeys(extended_profile_fields))

    def _is_field_required(self, field_name):
        """Check whether a field is required based on Django settings. """
        _extra_fields_setting = copy.deepcopy(
            configuration_helpers.get_value('REGISTRATION_EXTRA_FIELDS')
        )
        if not _extra_fields_setting:
            _extra_fields_setting = copy.deepcopy(settings.REGISTRATION_EXTRA_FIELDS)

        return _extra_fields_setting.get(field_name) == "required"

    def _get_custom_field_dict(self, field_name):
        """Given a field name searches for its definition dictionary.
        Arguments:
            field_name (str): the name of the field to search for.
        """
        custom_fields = getattr(settings, "EDNX_CUSTOM_REGISTRATION_FIELDS", [])
        for field in custom_fields:
            if field.get("name").lower() == field_name:
                return field
        return {}

    def _get_custom_html_override(self, text_field, html_piece=None):
        """Overrides field with html piece.
        Arguments:
            text_field: field to override. It must have the following format:
                "Here {} goes the HTML piece." In `{}` will be inserted the HTML piece.
        Keyword Arguments:
            html_piece: string containing HTML components to be inserted.
        """
        if html_piece:
            html_piece = HTML(html_piece) if isinstance(html_piece, str) else ""
            return Text(_(text_field)).format(html_piece)  # pylint: disable=translation-of-non-string
        return text_field

    def _add_custom_field(self, form_desc, required=True, **kwargs):
        """Adds custom fields to a form description.
        Arguments:
            form_desc: A form description
        Keyword Arguments:
            required (bool): Whether this field is required; defaults to False
            field_name (str): Name used to get field information when creating it.
        """
        field_name = kwargs.pop("field_name")
        if field_name in getattr(settings, "EDNX_IGNORE_REGISTER_FIELDS", []):
            return

        custom_field_dict = self._get_custom_field_dict(field_name)
        if not custom_field_dict:
            return

        # Check to convert options:
        field_options = custom_field_dict.get("options")
        if isinstance(field_options, dict):
            field_options = [(str(value.lower()), name) for value, name in field_options.items()]
        elif isinstance(field_options, list):
            field_options = [(str(value.lower()), value) for value in field_options]

        # Set default option if applies:
        default_option = custom_field_dict.get("default")
        if default_option:
            form_desc.override_field_properties(
                field_name,
                default=default_option
            )

        field_type = custom_field_dict.get("type")

        form_desc.add_field(
            field_name,
            label=self._get_custom_html_override(
                custom_field_dict.get("label"),
                custom_field_dict.get("html_override"),
            ),
            field_type=field_type,
            options=field_options,
            instructions=custom_field_dict.get("instructions"),
            placeholder=custom_field_dict.get("placeholder"),
            restrictions=custom_field_dict.get("restrictions"),
            include_default_option=bool(default_option) or field_type == "select",
            required=required,
            error_messages=custom_field_dict.get("errorMessages")
        )


class AddCustomOptionsOnAccountSettings(PipelineStep):
    """ Pipeline used to add custom option fields in account settings.

        Example usage:

        Add the following configurations to your configuration file:
                "OPEN_EDX_FILTERS_CONFIG": {
                    "org.openedx.learning.student.settings.render.started.v1": {
                        "fail_silently": false,
                        "pipeline": [
                            "eox_tenant.samples.pipeline.AddCustomOptionsOnAccountSettings"
                        ]
                    }
                }
    """

    def run_filter(self, context):  # pylint: disable=arguments-differ
        """ Run the pipeline filter. """
        extended_profile_fields = context.get("extended_profile_fields", [])

        custom_options, field_labels_map = self._get_custom_context(extended_profile_fields)  # pylint: disable=line-too-long

        extended_profile_field_options = configuration_helpers.get_value('EXTRA_FIELD_OPTIONS', custom_options)  # pylint: disable=line-too-long
        extended_profile_field_option_tuples = {}
        for field in extended_profile_field_options.keys():
            field_options = extended_profile_field_options[field]
            extended_profile_field_option_tuples[field] = [(option.lower(), option) for option in field_options]  # pylint: disable=line-too-long

        for field in custom_options:
            field_dict = {
                "field_name": field,
                "field_label": field_labels_map.get(field, field),
            }

            field_options = extended_profile_field_option_tuples.get(field)
            if field_options:
                field_dict["field_type"] = "ListField"
                field_dict["field_options"] = field_options
            else:
                field_dict["field_type"] = "TextField"

            field_index = next((index for (index, d) in enumerate(extended_profile_fields) if d["field_name"] == field_dict["field_name"]), None)  # pylint: disable=line-too-long
            if field_index is not None:
                context["extended_profile_fields"][field_index] = field_dict
        return context

    def _get_custom_context(self, extended_profile_fields):
        """ Get custom context for the field. """
        field_labels = {}
        field_options = {}
        custom_fields = getattr(settings, "EDNX_CUSTOM_REGISTRATION_FIELDS", [])

        for field in custom_fields:
            field_name = field.get("name")

            if not field_name:  # Required to identify the field.
                msg = "Custom fields must have a `name` defined in their configuration."
                raise ImproperlyConfigured(msg)

            field_label = field.get("label")
            if not any(extended_field['field_name'] == field_name for extended_field in extended_profile_fields) and field_label:  # pylint: disable=line-too-long
                field_labels[field_name] = _(field_label)  # pylint: disable=translation-of-non-string

            options = field.get("options")

            if options:
                field_options[field_name] = options

            return field_options, field_labels
