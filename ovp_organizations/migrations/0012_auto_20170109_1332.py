# -*- coding: utf-8 -*-
# Generated by Django 1.10.1 on 2017-01-09 13:32
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ovp_organizations', '0011_organization_cover'),
    ]

    operations = [
        migrations.AlterField(
            model_name='organization',
            name='causes',
            field=models.ManyToManyField(blank=True, to='ovp_core.Cause'),
        ),
    ]
