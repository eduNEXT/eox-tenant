# Add collation for tenant organization name column to make it case sensitive.

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):
    db_engine = settings.DATABASES['default']['ENGINE']
    # If the engine is SQLite, use BINARY
    if 'sqlite' in db_engine:
        db_collation_name = 'BINARY'
    # Otherwise, default to MySQL's utf8mb4_bin
    elif 'mysql' in db_engine:
        db_collation_name = 'utf8mb4_bin'

    dependencies = [
        ('eox_tenant', '0008_synchronize_tenants'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tenantorganization',
            name='name',
            field=models.CharField(db_collation=db_collation_name, db_index=True, max_length=100, unique=True),
        ),
    ]
