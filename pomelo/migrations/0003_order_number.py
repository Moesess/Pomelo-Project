# -*- coding: utf-8 -*-
# Generated by Django 1.11.20 on 2019-03-01 13:06
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pomelo', '0002_auto_20190301_1402'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='number',
            field=models.IntegerField(default=0),
        ),
    ]
