# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-03-27 20:47
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('stockInformation', '0003_auto_20170327_2304'),
    ]

    operations = [
        migrations.AlterField(
            model_name='stocks',
            name='change',
            field=models.DecimalField(decimal_places=3, default=0, max_digits=10),
        ),
        migrations.AlterField(
            model_name='stocks',
            name='price',
            field=models.DecimalField(decimal_places=3, default=0, max_digits=10),
        ),
    ]
