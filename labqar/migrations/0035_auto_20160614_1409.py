# -*- coding: utf-8 -*-
# Generated by Django 1.9.4 on 2016-06-14 14:09
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('labqar', '0034_auto_20160614_1402'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='dados',
            options={'ordering': ['dad_data'], 'verbose_name': 'Dados', 'verbose_name_plural': 'Dados'},
        ),
    ]
