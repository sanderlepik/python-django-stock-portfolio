# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('stockInformation', '0006_auto_20170328_1604'),
    ]

    operations = [
        migrations.AddField(
            model_name='stocks',
            name='balance',
            field=models.DecimalField(default=0, max_digits=10, decimal_places=2),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='stocks',
            name='buying_price',
            field=models.DecimalField(default=0, max_digits=10, decimal_places=2),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='stocks',
            name='stocks_owned',
            field=models.IntegerField(default=0),
            preserve_default=False,
        ),
    ]
