# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import jsonfield.fields


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Microsite',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('key', models.CharField(max_length=63, db_index=True)),
                ('subdomain', models.CharField(max_length=127, db_index=True)),
                ('values', jsonfield.fields.JSONField(blank=True)),
            ],
        ),
    ]
