# -*- coding: utf-8 -*-
# Generated by Django 1.9.4 on 2016-05-19 08:45
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('labqar', '0024_alertas_concentracao'),
    ]

    operations = [
        migrations.CreateModel(
            name='Parametro_Local',
            fields=[
                ('par_id', models.AutoField(primary_key=True, serialize=False)),
                ('par_nome', models.CharField(blank=True, editable=False, max_length=20, null=True)),
                ('par_nome_completo', models.CharField(blank=True, max_length=50, null=True, verbose_name=b'Nome a apresentar')),
                ('par_unidade_apresent', models.CharField(choices=[(b'ppm', b'ppm'), (b'ppb', b'ppb'), (b'U+00B5g/m3', b'U+00B5g/m3')], default=b'U+00B5g/m3', editable=False, max_length=50, null=True, verbose_name=b'Unidade de apresentacao')),
            ],
            options={
                'verbose_name': 'Parametro',
                'verbose_name_plural': 'Parametros',
            },
        ),
    ]
