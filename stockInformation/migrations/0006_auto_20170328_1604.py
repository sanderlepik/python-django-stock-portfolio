# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-03-28 13:04
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('stockInformation', '0005_auto_20170328_0950'),
    ]

    operations = [
        migrations.AlterField(
            model_name='stocks',
            name='change',
            field=models.CharField(max_length=200),
        ),
    ]