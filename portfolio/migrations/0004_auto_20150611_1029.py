# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('portfolio', '0003_auto_20150610_1811'),
    ]

    operations = [
        migrations.AlterField(
            model_name='transaction',
            name='exchange_rate',
            field=models.DecimalField(default=1, max_digits=10, decimal_places=4),
            preserve_default=True,
        ),
    ]
