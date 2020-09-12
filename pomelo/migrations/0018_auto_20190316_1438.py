# -*- coding: utf-8 -*-
# Generated by Django 1.11.20 on 2019-03-16 13:38
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('pomelo', '0017_profile_email_confirmed'),
    ]

    operations = [
        migrations.CreateModel(
            name='Reviews',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.TextField()),
                ('stars', models.IntegerField(choices=[(1, b'1 Gwiazdka'), (2, b'2 Gwiazdki'), (3, b'3 Gwiazdki'), (4, b'4 Gwiazdki'), (5, b'5 Gwiazdek')], default=0)),
                ('product', models.ForeignKey(default=0, on_delete=django.db.models.deletion.CASCADE, related_name='product_review', to='pomelo.Product')),
            ],
        ),
        migrations.AlterField(
            model_name='profile',
            name='account_type',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='AccountType', to='pomelo.AccountType', verbose_name='U\u017cytkownik'),
        ),
        migrations.AddField(
            model_name='reviews',
            name='user',
            field=models.ForeignKey(default=0, on_delete=django.db.models.deletion.CASCADE, related_name='user_review', to='pomelo.Profile'),
        ),
    ]