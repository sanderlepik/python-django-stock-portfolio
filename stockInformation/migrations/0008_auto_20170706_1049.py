# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('stockInformation', '0007_auto_20170705_2111'),
    ]

    operations = [
        migrations.AlterField(
            model_name='stocks',
            name='change',
            field=models.DecimalField(max_digits=10, decimal_places=2),
            preserve_default=True,
        ),
    ]
