# Generated by Django 5.2.3 on 2025-07-17 09:47

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0019_job_company'),
    ]

    operations = [
        migrations.AlterField(
            model_name='job',
            name='company',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='accounts.companyprofile'),
            preserve_default=False,
        ),
    ]
