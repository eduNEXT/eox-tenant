# -*- coding: utf-8 -*-
# Generated by Django 1.11.21 on 2020-09-24 17:31
from __future__ import unicode_literals

from django.core.management import call_command
from django.db import migrations


def synchronize_tenants(apps, schema_editor):
    call_command("synchronize_organizations")


class Migration(migrations.Migration):

    dependencies = [
        ('eox_tenant', '0007_auto_20200922_1421'),
    ]

    operations = [
        migrations.RunPython(synchronize_tenants)
    ]
