# Generated by Django 5.0.7 on 2025-03-17 07:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('documents', '0002_contract_status'),
    ]

    operations = [
        migrations.AddField(
            model_name='contract',
            name='company_account',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='contract',
            name='company_phone',
            field=models.CharField(blank=True, max_length=15, null=True),
        ),
        migrations.AddField(
            model_name='contract',
            name='contact_phone',
            field=models.CharField(blank=True, max_length=15, null=True),
        ),
    ]
