# Generated by Django 4.2.9 on 2024-03-09 20:34

from django.db import migrations, models
import martor.models


class Migration(migrations.Migration):

    dependencies = [
        ('reporting', '0025_alter_report_nmap_scan_alter_report_openvas_scan'),
    ]

    operations = [
        migrations.CreateModel(
            name='Appendix',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200)),
                ('description', martor.models.MartorField()),
                ('finding', models.ManyToManyField(blank=True, related_name='appendix_finding', to='reporting.finding')),
            ],
        ),
    ]
