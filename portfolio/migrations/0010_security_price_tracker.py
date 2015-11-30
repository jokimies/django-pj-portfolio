# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import portfolio.models


class Migration(migrations.Migration):

    dependencies = [
        ('portfolio', '0009_pricetracker'),
    ]

    operations = [
        migrations.AddField(
            model_name='security',
            name='price_tracker',
            field=models.ForeignKey(default=portfolio.models.set_default_tracker, to='portfolio.PriceTracker'),
        ),
    ]
