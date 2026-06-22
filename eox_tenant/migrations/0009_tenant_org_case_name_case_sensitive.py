# Add collation for tenant organization name column to make it case sensitive.

import collections
from django.db import migrations, models
import jsonfield.fields


class Migration(migrations.Migration):

    dependencies = [
        ('eox_tenant', '0008_synchronize_tenants'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tenantorganization',
            name='name',
            field=models.CharField(db_collation='utf8mb4_bin', db_index=True, max_length=100, unique=True),
        ),
    ]
