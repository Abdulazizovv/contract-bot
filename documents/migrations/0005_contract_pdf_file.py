# Generated by Django 5.0.7 on 2025-03-17 08:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('documents', '0004_contract_company_oked'),
    ]

    operations = [
        migrations.AddField(
            model_name='contract',
            name='pdf_file',
            field=models.FileField(blank=True, null=True, upload_to='contracts/'),
        ),
    ]
