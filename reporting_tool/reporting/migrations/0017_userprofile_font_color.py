# Generated by Django 4.2.9 on 2024-02-28 20:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reporting', '0016_userprofile_background_color'),
    ]

    operations = [
        migrations.AddField(
            model_name='userprofile',
            name='font_color',
            field=models.CharField(default='', max_length=9),
        ),
    ]