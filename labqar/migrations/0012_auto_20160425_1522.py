# -*- coding: utf-8 -*-
# Generated by Django 1.9.4 on 2016-04-25 15:22
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('labqar', '0011_auto_20160425_1519'),
    ]

    operations = [
        migrations.AlterField(
            model_name='dados',
            name='est_id',
            field=models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, to='labqar.Estacao', verbose_name=b'est'),
        ),
    ]
