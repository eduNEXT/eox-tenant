# -*- coding: utf-8 -*-
from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ('eox_tenant', '0003_auto_20190620_1704'),
    ]
    state_operations = [
        migrations.DeleteModel('Redirection'),
    ]
    operations = [
        migrations.SeparateDatabaseAndState(state_operations=state_operations)
    ]
