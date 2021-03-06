# -*- coding: utf-8 -*-
# Generated by Django 1.11.20 on 2019-03-01 13:02
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('pomelo', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='accounttype',
            options={'verbose_name': 'Typ Konta', 'verbose_name_plural': 'Typy Kont'},
        ),
        migrations.AlterModelOptions(
            name='category',
            options={'verbose_name': 'Kategoria', 'verbose_name_plural': 'Kategorie'},
        ),
        migrations.AlterModelOptions(
            name='order',
            options={'verbose_name': 'Zam\xf3wienie', 'verbose_name_plural': 'Zam\xf3wienia'},
        ),
        migrations.AlterModelOptions(
            name='product',
            options={'verbose_name': 'Produkt', 'verbose_name_plural': 'Produkty'},
        ),
        migrations.AlterModelOptions(
            name='status',
            options={'verbose_name': 'Stan', 'verbose_name_plural': 'Stan'},
        ),
        migrations.AlterModelOptions(
            name='storehouse',
            options={'verbose_name': 'Magazyn', 'verbose_name_plural': 'Magazyny'},
        ),
        migrations.AlterModelOptions(
            name='user',
            options={'verbose_name': 'U\u017cytkownik', 'verbose_name_plural': 'U\u017cytkownicy'},
        ),
        migrations.AddField(
            model_name='accounttype',
            name='name',
            field=models.CharField(default='Hej', max_length=255, unique=True),
        ),
        migrations.AddField(
            model_name='status',
            name='number',
            field=models.IntegerField(default='0'),
        ),
        migrations.AddField(
            model_name='storehouse',
            name='city',
            field=models.CharField(default='', max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='user',
            name='email',
            field=models.EmailField(default='def@def.def', max_length=254),
        ),
        migrations.AddField(
            model_name='user',
            name='login',
            field=models.CharField(default='def', max_length=255, unique=True),
        ),
        migrations.AddField(
            model_name='user',
            name='password',
            field=models.CharField(default='def', max_length=32),
        ),
        migrations.AlterField(
            model_name='category',
            name='name',
            field=models.CharField(default='def', max_length=255, unique=True),
        ),
        migrations.AlterField(
            model_name='product',
            name='category',
            field=models.ForeignKey(default=0, on_delete=django.db.models.deletion.CASCADE, related_name='category', to='pomelo.Category', verbose_name='Produkt'),
        ),
        migrations.AlterField(
            model_name='product',
            name='name',
            field=models.CharField(default='def', max_length=255, unique=True),
        ),
        migrations.AlterField(
            model_name='product',
            name='price',
            field=models.DecimalField(decimal_places=2, default='0', max_digits=10),
        ),
        migrations.AlterField(
            model_name='storehouse',
            name='address',
            field=models.CharField(default='', max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='user',
            name='account_type',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='AccountType', to='pomelo.AccountType', verbose_name='U\u017cytkownik'),
        ),
    ]
