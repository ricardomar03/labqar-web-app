# -*- coding: utf-8 -*-
# Generated by Django 1.9.4 on 2016-06-21 00:50
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('labqar', '0039_historico_alertas_his_campanha'),
    ]

    operations = [
        migrations.AlterField(
            model_name='historico_alertas',
            name='his_campanha',
            field=models.CharField(default='Nenhuma', max_length=255),
            preserve_default=False,
        ),
    ]
