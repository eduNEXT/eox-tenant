# -*- coding: utf-8 -*-
# Generated by Django 1.11.13 on 2018-11-07 21:04
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ednx_microsites', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelTable(
            name='microsite',
            table='ednx_microsites_microsites',
        ),
    ]
