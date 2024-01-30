# Generated by Django 4.2.9 on 2024-01-13 15:00

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('reporting', '0003_db_owasp_alter_db_cwe_options'),
    ]

    operations = [
        migrations.CreateModel(
            name='Customer',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='Report',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255)),
                ('executive_summary', models.TextField()),
                ('scope', models.TextField()),
                ('outofscope', models.TextField()),
                ('methodology', models.TextField()),
                ('recommendation', models.TextField()),
                ('creation_date', models.DateTimeField(auto_now_add=True)),
                ('report_date', models.DateTimeField()),
                ('audit_start', models.DateField(blank=True, null=True)),
                ('audit_end', models.DateField(blank=True, null=True)),
            ],
            options={
                'verbose_name_plural': 'Reports',
            },
        ),
        migrations.AddField(
            model_name='finding',
            name='closed_at',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='finding',
            name='cwe',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='reporting.db_cwe'),
        ),
        migrations.AddField(
            model_name='finding',
            name='owasp',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='reporting.db_owasp'),
        ),
        migrations.AlterField(
            model_name='finding',
            name='description',
            field=models.TextField(),
        ),
    ]
