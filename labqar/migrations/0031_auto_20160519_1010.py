# -*- coding: utf-8 -*-
# Generated by Django 1.9.4 on 2016-05-19 10:10
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('labqar', '0030_auto_20160519_1003'),
    ]

    operations = [
        migrations.AlterField(
            model_name='parametro_local',
            name='par_nome',
            field=models.CharField(blank=True, editable=False, max_length=20, null=True),
        ),
    ]
