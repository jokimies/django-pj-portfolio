# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('currency_history', '__first__'),
        ('portfolio', '0002_account_base_currency'),
    ]

    operations = [
        migrations.AddField(
            model_name='transaction',
            name='currency',
            field=models.ForeignKey(default=2, to='currency_history.Currency'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='transaction',
            name='exchange_rate',
            field=models.DecimalField(default=1, null=True, max_digits=10, decimal_places=4),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='account',
            name='base_currency',
            field=models.CharField(default=b'EUR', max_length=3, verbose_name='Base currency,ISO-code'),
            preserve_default=True,
        ),
    ]
