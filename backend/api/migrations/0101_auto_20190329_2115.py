# -*- coding: utf-8 -*-
# Generated by Django 1.11.20 on 2019-03-29 21:15
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0100_auto_20190329_1942'),
    ]

    operations = [
        migrations.AddField(
            model_name='fuelcode',
            name='fuel_code_version',
            field=models.IntegerField(default=100),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='fuelcode',
            name='fuel_code_version_minor',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='fuelcode',
            name='fuel_code',
            field=models.CharField(default='BCLCF', max_length=10),
        ),
    ]