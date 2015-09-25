# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('currency_history', '__first__'),
        ('portfolio', '0004_auto_20150611_1029'),
    ]

    operations = [
        migrations.AddField(
            model_name='price',
            name='currency',
            field=models.ForeignKey(default=2, to='currency_history.Currency'),
            preserve_default=False,
        ),
    ]
