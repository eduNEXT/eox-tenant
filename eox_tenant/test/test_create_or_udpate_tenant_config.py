"""This module include a class that checks the command create_or_update_tenant_config.py"""
import json
import tempfile

from django.core.management import CommandError, call_command
from django.test import TestCase

from eox_tenant.models import Route, TenantConfig


class CreateOrUpdateTenantConfigTestCase(TestCase):
    """ This class checks the command create_or_update_tenant_config.py"""

    def setUp(self):
        """This method creates TenantConfig objects in database"""
        self.test_conf = {
            "lms_configs": {"NEW KEY": "value-updated", "NESTED_KEY": {"key": "value"}},
            "studio_configs": {"STUDIO_KEY": "value", "STUDIO_NESTED_KEY": {"key": "value"}, }
        }
        self.external_key = "test"
        TenantConfig.objects.create(
            external_key=self.external_key,
            lms_configs={
                "KEY": "value",
            },
        )

    def test_command_happy_path_with_cmd_config(self):
        """Tests that command runs successfully if config is passed via cmd"""
        self.assertFalse(TenantConfig.objects.filter(external_key="new.key").exists())
        self.assertFalse(Route.objects.filter(domain__contains="test.domain").exists())
        call_command(
            "create_or_update_tenant_config",
            "--external-key",
            "new.key",
            "--config",
            json.dumps(self.test_conf),
            "test.domain",
            "studio.test.domain"
        )
        created_config = TenantConfig.objects.get(external_key="new.key")
        self.assertTrue(created_config.lms_configs == self.test_conf["lms_configs"])
        self.assertTrue(created_config.studio_configs == self.test_conf["studio_configs"])
        created_routes = Route.objects.filter(domain__contains="test.domain").count()
        self.assertTrue(created_routes == 2)

    def test_command_happy_path_with_file_config(self):
        """Tests that command runs successfully if config is passed via file"""
        self.assertFalse(TenantConfig.objects.filter(external_key="new.key").exists())
        self.assertFalse(Route.objects.filter(domain__contains="test.domain").exists())
        with tempfile.NamedTemporaryFile('w') as fp:
            fp.write(json.dumps(self.test_conf))
            fp.seek(0)
            call_command(
                "create_or_update_tenant_config",
                "--external-key",
                "new.key",
                "--config-file",
                fp.name,
                "test.domain",
                "studio.test.domain"
            )
        created_config = TenantConfig.objects.get(external_key="new.key")
        self.assertTrue(created_config.lms_configs == self.test_conf["lms_configs"])
        created_routes = Route.objects.filter(domain__contains="test.domain").count()
        self.assertTrue(created_routes == 2)

    def test_command_invalid_config(self):
        """Tests that command raises if config is invalid"""
        self.assertFalse(TenantConfig.objects.filter(external_key="new.key").exists())
        self.assertFalse(Route.objects.filter(domain__contains="test.domain").exists())
        with self.assertRaises(CommandError):
            call_command(
                "create_or_update_tenant_config",
                "--external-key",
                "new.key",
                "--config",
                '{"KEY": "value, "NESTED_KEY": {"key": "value"}}',
                "test.domain",
                "studio.test.domain"
            )
        self.assertFalse(TenantConfig.objects.filter(external_key="new.key").exists())
        self.assertFalse(Route.objects.filter(domain__contains="test.domain").exists())

    def test_command_with_no_config(self):
        """
        Tests that command works even if config is not passed,
        i.e. it adds/updates an entry with external_key and links given routes.
        """
        self.assertFalse(TenantConfig.objects.filter(external_key="new.key").exists())
        self.assertFalse(Route.objects.filter(domain__contains="test.domain").exists())
        call_command(
            "create_or_update_tenant_config",
            "--external-key",
            "new.key",
            "test.domain",
            "studio.test.domain"
        )
        self.assertTrue(TenantConfig.objects.filter(external_key="new.key").exists())
        self.assertTrue(Route.objects.filter(domain__contains="test.domain").exists())

    def test_command_with_long_external_key(self):
        """Tests that command runs successfully even if external key is longer than limit."""
        long_external_key = "areallyreallyreallyreallyreallyreallylongexternalkey"
        self.assertFalse(
            TenantConfig.objects.filter(external_key__in=[long_external_key, long_external_key[:63]]).exists()
        )
        self.assertFalse(Route.objects.filter(domain__contains="test.domain").exists())
        call_command(
            "create_or_update_tenant_config",
            "--external-key",
            long_external_key,
            "--config",
            json.dumps(self.test_conf),
            "test.domain",
            "studio.test.domain"
        )
        created_config = TenantConfig.objects.get(external_key=long_external_key[:63])
        self.assertTrue(created_config.lms_configs == self.test_conf["lms_configs"])
        created_routes = Route.objects.filter(domain__contains="test.domain").count()
        self.assertTrue(created_routes == 2)

    def test_command_update_existing_tenant(self):
        """Tests that command successfully updates existing TenantConfig."""
        config = TenantConfig.objects.get(external_key=self.external_key)
        self.assertTrue(config.lms_configs == {"KEY": "value"})
        self.assertTrue(config.studio_configs == {})
        call_command(
            "create_or_update_tenant_config",
            "--external-key",
            self.external_key,
            "--config",
            json.dumps(self.test_conf),
            "test.domain",
            "studio.test.domain"
        )
        updated_config = TenantConfig.objects.get(external_key=self.external_key)
        for key, value in self.test_conf["lms_configs"].items():
            self.assertTrue(updated_config.lms_configs[key] == value)
        self.assertTrue(updated_config.lms_configs["KEY"] == "value")
        self.assertTrue(updated_config.studio_configs == self.test_conf["studio_configs"])
        created_routes = Route.objects.filter(domain__contains="test.domain").count()
        self.assertTrue(created_routes == 2)

    def test_command_update_existing_tenant_override(self):
        """Tests that command successfully replaces existing TenantConfig with override param."""
        config = TenantConfig.objects.get(external_key=self.external_key)
        self.assertTrue(config.studio_configs == {})
        new_conf = {"lms_configs": {"NEW_KEY": "new value"}}
        call_command(
            "create_or_update_tenant_config",
            "--external-key",
            self.external_key,
            "--config",
            json.dumps(new_conf),
            "test.domain",
            "studio.test.domain",
            "--override",
        )
        updated_config = TenantConfig.objects.get(external_key=self.external_key)
        self.assertTrue(updated_config.lms_configs == new_conf["lms_configs"])
        created_routes = Route.objects.filter(domain__contains="test.domain").count()
        self.assertTrue(created_routes == 2)
