# Generated by Django 4.2.9 on 2024-02-23 17:18

from django.db import migrations, models
import django.db.models.deletion
import martor.models


class Migration(migrations.Migration):

    dependencies = [
        ('reporting', '0012_alter_customer_description_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Finding_Template',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('finding_id', models.CharField(max_length=200)),
                ('title', models.CharField(max_length=200)),
                ('severity', models.CharField(blank=True, max_length=200)),
                ('cvss_vector', models.CharField(blank=True, max_length=200)),
                ('cvss_score', models.DecimalField(decimal_places=1, default=0, max_digits=3)),
                ('description', martor.models.MartorField(blank=True)),
                ('location', martor.models.MartorField(blank=True)),
                ('impact', martor.models.MartorField(blank=True)),
                ('recommendation', martor.models.MartorField(blank=True)),
                ('references', martor.models.MartorField(blank=True)),
                ('poc', martor.models.MartorField(blank=True)),
                ('owasp', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='reporting.db_owasp')),
            ],
        ),
    ]
