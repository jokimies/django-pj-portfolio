# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('portfolio', '0005_price_currency'),
    ]

    operations = [
        migrations.AddField(
            model_name='price',
            name='change',
            field=models.DecimalField(null=True, max_digits=6, decimal_places=2, blank=True),
            preserve_default=True,
        ),
    ]
