# -*- coding: utf-8 -*-
# Generated by Django 1.9.11 on 2016-12-10 16:50
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.manager


class Migration(migrations.Migration):

    dependencies = [
        ('portfolio', '0010_security_price_tracker'),
    ]

    operations = [
        migrations.AlterModelManagers(
            name='account',
            managers=[
                ('div_years', django.db.models.manager.Manager()),
            ],
        ),
        migrations.AlterField(
            model_name='account',
            name='base_currency',
            field=models.CharField(default='EUR', max_length=3, verbose_name='Base currency,ISO-code'),
        ),
        migrations.AlterField(
            model_name='price',
            name='date',
            field=models.DateField(verbose_name='transaction date'),
        ),
        migrations.AlterField(
            model_name='transaction',
            name='action',
            field=models.CharField(choices=[('BUY', 'Buy'), ('SELL', 'Sell')], max_length=10),
        ),
        migrations.AlterField(
            model_name='transaction',
            name='date',
            field=models.DateField(verbose_name='transaction date'),
        ),
    ]