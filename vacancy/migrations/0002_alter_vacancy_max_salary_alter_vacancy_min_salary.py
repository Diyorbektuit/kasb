# Generated by Django 5.1.5 on 2025-02-14 05:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('vacancy', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='vacancy',
            name='max_salary',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='vacancy',
            name='min_salary',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]
