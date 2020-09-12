# -*- coding: utf-8 -*-
# Generated by Django 1.11.20 on 2019-03-03 11:14
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('pomelo', '0008_auto_20190302_1701'),
    ]

    operations = [
        migrations.CreateModel(
            name='ProductImages',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(null=True, upload_to='product_images', verbose_name='Image')),
            ],
        ),
        migrations.RenameField(
            model_name='product',
            old_name='image',
            new_name='main_image',
        ),
        migrations.AlterField(
            model_name='product',
            name='category',
            field=models.ForeignKey(default=0, on_delete=django.db.models.deletion.CASCADE, related_name='category', to='pomelo.Category', verbose_name='Kategoria'),
        ),
        migrations.AddField(
            model_name='productimages',
            name='product',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, related_name='product', to='pomelo.Product', verbose_name='Produkt'),
        ),
    ]