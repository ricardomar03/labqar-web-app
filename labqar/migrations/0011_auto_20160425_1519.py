# -*- coding: utf-8 -*-
# Generated by Django 1.9.4 on 2016-04-25 15:19
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('labqar', '0010_auto_20160425_1512'),
    ]

    operations = [
        migrations.AlterField(
            model_name='dados',
            name='dad_id',
            field=models.IntegerField(primary_key=True, serialize=False),
        ),
    ]