# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('portfolio', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='account',
            name='base_currency',
            field=models.CharField(default=b'EUR', max_length=3, verbose_name='ISO-code for currency'),
            preserve_default=True,
        ),
    ]
