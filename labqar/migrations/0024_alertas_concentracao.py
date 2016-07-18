# -*- coding: utf-8 -*-
# Generated by Django 1.9.4 on 2016-05-18 13:29
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('labqar', '0023_auto_20160518_1050'),
    ]

    operations = [
        migrations.CreateModel(
            name='Alertas_Concentracao',
            fields=[
                ('alr_id', models.AutoField(primary_key=True, serialize=False)),
                ('alr_valor_min', models.IntegerField(verbose_name=b'Valor Minimo')),
                ('alr_valor_max', models.IntegerField(verbose_name=b'Valor Maximo')),
                ('alr_parametro', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='labqar.Parametro', verbose_name=b'Parametro Associado')),
            ],
            options={
                'verbose_name_plural': 'Alertas Concentracoes',
            },
        ),
    ]
