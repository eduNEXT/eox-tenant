"""
Test file the widgets module
"""
from django.test import TestCase

from eox_tenant.widgets import JsonWidget


class JsonWidgetTest(TestCase):
    """
    Test JsonWidget form
    """

    def test_get_context(self):
        """
        Making sure method get_context works
        """
        widget = JsonWidget()
        context = widget.get_context("name", r'{"value": "value"}', ["value"])
        self.assertIn("widget", context)
        self.assertIn("name", context["widget"])
        self.assertIn("value", context["widget"])

        value_with_indent = str(context["widget"]["value"])
        value_without_indent = str(context["widget"]["value"]).replace(" ", "")
        self.assertGreater(len(value_with_indent) - len(value_without_indent), 0)
