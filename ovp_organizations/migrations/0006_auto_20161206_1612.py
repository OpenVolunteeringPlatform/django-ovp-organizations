# -*- coding: utf-8 -*-
# Generated by Django 1.10.1 on 2016-12-06 16:12
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ovp_organizations', '0005_auto_20161206_1515'),
    ]

    operations = [
        migrations.RenameField(
            model_name='organization',
            old_name='created_at',
            new_name='created_date',
        ),
        migrations.RenameField(
            model_name='organization',
            old_name='deleted_at',
            new_name='deleted_date',
        ),
        migrations.RenameField(
            model_name='organization',
            old_name='modified_at',
            new_name='modified_date',
        ),
        migrations.RenameField(
            model_name='organization',
            old_name='published_at',
            new_name='published_date',
        ),
    ]