# Generated by Django 5.1.5 on 2025-01-27 15:51

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0003_remove_postlanguage_post_and_more'),
        ('vacancy', '0002_delete_application'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='application',
            name='extra_description',
        ),
        migrations.AddField(
            model_name='application',
            name='birthday_data',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='application',
            name='experience',
            field=models.CharField(blank=True, max_length=256, null=True),
        ),
        migrations.AddField(
            model_name='application',
            name='gender',
            field=models.CharField(blank=True, max_length=256, null=True),
        ),
        migrations.AddField(
            model_name='application',
            name='job_type',
            field=models.CharField(blank=True, max_length=512, null=True),
        ),
        migrations.AddField(
            model_name='application',
            name='languages',
            field=models.CharField(blank=True, max_length=1024, null=True),
        ),
        migrations.AddField(
            model_name='application',
            name='level_of_education',
            field=models.CharField(blank=True, max_length=1024, null=True),
        ),
        migrations.AddField(
            model_name='application',
            name='marital_status',
            field=models.CharField(blank=True, max_length=123, null=True),
        ),
        migrations.AddField(
            model_name='application',
            name='region',
            field=models.CharField(blank=True, max_length=123, null=True),
        ),
        migrations.AlterField(
            model_name='application',
            name='country',
            field=models.CharField(blank=True, max_length=256, null=True),
        ),
        migrations.AlterField(
            model_name='application',
            name='vacancy',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='applications', to='vacancy.vacancy'),
        ),
        migrations.AlterField(
            model_name='form',
            name='description',
            field=models.TextField(blank=True, null=True),
        ),
    ]
