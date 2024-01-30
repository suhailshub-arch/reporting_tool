# Generated by Django 4.2.9 on 2024-01-14 00:02

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('reporting', '0006_finding_finding_id'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='customer',
            options={'verbose_name_plural': 'Customers'},
        ),
        migrations.AddField(
            model_name='customer',
            name='contact',
            field=models.EmailField(blank=True, max_length=255),
        ),
        migrations.AddField(
            model_name='customer',
            name='description',
            field=models.TextField(blank=True),
        ),
        migrations.AddField(
            model_name='report',
            name='customer',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='reporting.customer'),
            preserve_default=False,
        ),
    ]
