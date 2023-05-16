"""This module include a class that checks the command change_domain.py"""
from django.core.management import call_command
from django.core.management.base import CommandError
from django.test import TestCase
from mock import patch

from eox_tenant.models import Microsite


class EditTenantValuesTestCase(TestCase):
    """ This class checks the command edit_microsite_values.py"""

    def setUp(self):
        """This method creates Microsite objects in database"""
        Microsite.objects.create(
            key="test",
            subdomain="first.test.prod.edunext.co",
            values={
                "KEY": "value",
                "NESTED_KEY": {"key": "value"},
            })

    @patch('eox_tenant.management.commands.edit_microsite_values.input', return_value='y')
    def test_command_can_be_called(self, _):
        """Tests that we can actually run the command"""
        call_command('edit_microsite_values')

    @patch('eox_tenant.management.commands.edit_microsite_values.input', return_value='n')
    def test_command_exec_confirmation_false(self, _):
        """Tests that when the confirmation returns other than 'y' we raise the abort error"""
        with self.assertRaises(CommandError):
            call_command('edit_microsite_values')

    @patch('eox_tenant.management.commands.edit_microsite_values.input', return_value='y')
    def test_command_exec_confirmation_add(self, _):
        """Tests that we can add a new key"""
        call_command('edit_microsite_values', '--add', 'NEW_KEY', 'NEW_VALUE')
        tenant = Microsite.objects.get(key='test')
        self.assertIn('NEW_KEY', tenant.values)
        self.assertEqual('NEW_VALUE', tenant.values.get('NEW_KEY'))

    @patch('eox_tenant.management.commands.edit_microsite_values.input', return_value='y')
    def test_command_exec_confirmation_add_nested(self, _):
        """Tests that we can add a new nested key"""
        call_command('edit_microsite_values', '--add', 'NEW_KEY.nested', 'NEW_VALUE')
        tenant = Microsite.objects.get(key='test')
        self.assertIn('nested', tenant.values.get('NEW_KEY'))
        self.assertEqual('NEW_VALUE', tenant.values.get('NEW_KEY').get('nested'))

    @patch('eox_tenant.management.commands.edit_microsite_values.input', return_value='y')
    def test_command_exec_confirmation_delete(self, _):
        """Tests that we can remove a key"""
        call_command('edit_microsite_values', '--delete', 'KEY')
        tenant = Microsite.objects.get(key='test')
        self.assertNotIn('KEY', tenant.values)

    @patch('eox_tenant.management.commands.edit_microsite_values.input', return_value='y')
    def test_command_exec_confirmation_delete_chain(self, _):
        """Tests that we can remove a nested key"""
        call_command('edit_microsite_values', '--delete', 'NESTED_KEY.key')
        tenant = Microsite.objects.get(key='test')
        self.assertIn('NESTED_KEY', tenant.values)
        self.assertNotIn('key', tenant.values.get('NESTED_KEY'))

    @patch('eox_tenant.management.commands.edit_microsite_values.input', return_value='y')
    def test_command_exec_confirmation_pattern(self, _):
        """Tests that we can affect only the sites defined by a pattern in their subdomain"""
        Microsite.objects.create(
            key="test2",
            subdomain="second.test.prod.edunext.co",
            values={
                "KEY": "value",
                "NESTED_KEY": {"key": "value"},
            })

        call_command('edit_microsite_values', '--delete', 'KEY', '--pattern', 'second.test.prod.edunext.co')
        tenant1 = Microsite.objects.get(key='test')
        tenant2 = Microsite.objects.get(key='test2')

        self.assertIn('KEY', tenant1.values)
        self.assertNotIn('KEY', tenant2.values)
