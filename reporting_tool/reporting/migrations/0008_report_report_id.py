# Generated by Django 4.2.9 on 2024-01-14 14:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reporting', '0007_alter_customer_options_customer_contact_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='report',
            name='report_id',
            field=models.CharField(blank=True, max_length=255, unique=True),
        ),
    ]
