# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('portfolio', '0007_price_change_percentage'),
    ]

    operations = [
        migrations.AlterField(
            model_name='security',
            name='name',
            field=models.CharField(max_length=40),
        ),
        migrations.AlterField(
            model_name='security',
            name='ticker',
            field=models.CharField(max_length=40),
        ),
    ]
