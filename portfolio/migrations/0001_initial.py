# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Account',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=50)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Price',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('date', models.DateField(verbose_name=b'transaction date')),
                ('price', models.DecimalField(max_digits=10, decimal_places=2)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Security',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('ticker', models.CharField(max_length=40)),
                ('name', models.CharField(max_length=40)),
            ],
            options={
                'ordering': ['name'],
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Transaction',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('action', models.CharField(max_length=10, choices=[(b'BUY', b'Buy'), (b'SELL', b'Sell')])),
                ('date', models.DateField(verbose_name=b'transaction date')),
                ('shares', models.DecimalField(null=True, max_digits=10, decimal_places=4)),
                ('price', models.DecimalField(null=True, max_digits=10, decimal_places=4)),
                ('commission', models.DecimalField(null=True, max_digits=10, decimal_places=2)),
                ('cash_amount', models.DecimalField(null=True, max_digits=10, decimal_places=2)),
                ('sec_fee', models.DecimalField(null=True, max_digits=10, decimal_places=2)),
                ('split_ratio', models.DecimalField(null=True, max_digits=5, decimal_places=2)),
                ('account', models.ForeignKey(to='portfolio.Account')),
                ('security', models.ForeignKey(to='portfolio.Security')),
            ],
            options={
                'ordering': ['date'],
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='price',
            name='security',
            field=models.ForeignKey(to='portfolio.Security'),
            preserve_default=True,
        ),
    ]
