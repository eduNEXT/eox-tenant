import json
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
        return {'widget': {
            'name': name,
            'value': json.dumps(json.loads(value), indent=4),
        }}
