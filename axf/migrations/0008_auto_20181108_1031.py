# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2018-11-08 02:31
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('axf', '0007_auto_20181107_1454'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='order',
            name='sum_price',
        ),
        migrations.AddField(
            model_name='orderitem',
            name='buy_money',
            field=models.FloatField(default=1, verbose_name='订单总金额'),
            preserve_default=False,
        ),
    ]
