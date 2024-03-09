# Generated by Django 4.2.9 on 2024-03-08 19:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reporting', '0024_report_openvas_scan'),
    ]

    operations = [
        migrations.AlterField(
            model_name='report',
            name='nmap_scan',
            field=models.TextField(blank=True, default='', help_text='Nmap scan results in JSON format'),
        ),
        migrations.AlterField(
            model_name='report',
            name='openvas_scan',
            field=models.TextField(blank=True, default='', help_text='OpenVAS scan results in JSON format'),
        ),
    ]
