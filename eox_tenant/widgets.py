"""
Widgets for eox-tenant forms.
"""
import json

import six
from django.forms.widgets import Widget


class JsonWidget(Widget):
    """
    Widget form for mysql JSONField.
    """
    template_name = 'eox-tenant/widgets/json_widget.html'

    def get_context(self, name, value, attrs):
        """
        Add indent to JSONField.
        """
        try:
            value = json.loads(value) if isinstance(value, six.string_types) else value
            value = json.dumps(value, indent=4, sort_keys=True)
        except (ValueError, json.decoder.JSONDecodeError):
            pass
        return {'widget': {
            'name': name,
            'value': value,
        }}
