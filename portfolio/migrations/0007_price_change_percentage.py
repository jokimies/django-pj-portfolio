# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('portfolio', '0006_price_change'),
    ]

    operations = [
        migrations.AddField(
            model_name='price',
            name='change_percentage',
            field=models.DecimalField(null=True, max_digits=6, decimal_places=2, blank=True),
            preserve_default=True,
        ),
    ]
