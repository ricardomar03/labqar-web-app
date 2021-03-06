# -*- coding: utf-8 -*-
# Generated by Django 1.9.4 on 2016-04-25 15:12
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('labqar', '0009_auto_20160423_2124'),
    ]

    operations = [
        migrations.AlterField(
            model_name='dados',
            name='cam_id',
            field=models.IntegerField(blank=True, null=True, verbose_name=b'Campanha'),
        ),
        migrations.AlterField(
            model_name='dados',
            name='dad_10med',
            field=models.FloatField(blank=True, null=True, verbose_name=b'Valor Etilbenzeno'),
        ),
        migrations.AlterField(
            model_name='dados',
            name='dad_10stat',
            field=models.SmallIntegerField(blank=True, null=True, verbose_name=b'Estado Etilbenzeno'),
        ),
        migrations.AlterField(
            model_name='dados',
            name='dad_11med',
            field=models.FloatField(blank=True, null=True, verbose_name=b'Valor MPXileno'),
        ),
        migrations.AlterField(
            model_name='dados',
            name='dad_11stat',
            field=models.SmallIntegerField(blank=True, null=True, verbose_name=b'Estado MPXileno'),
        ),
        migrations.AlterField(
            model_name='dados',
            name='dad_12med',
            field=models.FloatField(blank=True, null=True, verbose_name=b'Valor OXileno'),
        ),
        migrations.AlterField(
            model_name='dados',
            name='dad_12stat',
            field=models.SmallIntegerField(blank=True, null=True, verbose_name=b'Estado OXileno'),
        ),
        migrations.AlterField(
            model_name='dados',
            name='dad_13med',
            field=models.FloatField(blank=True, null=True, verbose_name=b'Valor partEnv'),
        ),
        migrations.AlterField(
            model_name='dados',
            name='dad_13stat',
            field=models.SmallIntegerField(blank=True, null=True, verbose_name=b'Estado partEnv'),
        ),
        migrations.AlterField(
            model_name='dados',
            name='dad_14med',
            field=models.FloatField(blank=True, null=True, verbose_name=b'Valor SO2offset'),
        ),
        migrations.AlterField(
            model_name='dados',
            name='dad_14stat',
            field=models.SmallIntegerField(blank=True, null=True, verbose_name=b'Estado SO2offset'),
        ),
        migrations.AlterField(
            model_name='dados',
            name='dad_15med',
            field=models.FloatField(blank=True, null=True, verbose_name=b'Valor Temp'),
        ),
        migrations.AlterField(
            model_name='dados',
            name='dad_15stat',
            field=models.SmallIntegerField(blank=True, null=True, verbose_name=b'Estado Temp'),
        ),
        migrations.AlterField(
            model_name='dados',
            name='dad_16med',
            field=models.FloatField(blank=True, null=True, verbose_name=b'Valor Hum %'),
        ),
        migrations.AlterField(
            model_name='dados',
            name='dad_16stat',
            field=models.SmallIntegerField(blank=True, null=True, verbose_name=b'Estado Hum %'),
        ),
        migrations.AlterField(
            model_name='dados',
            name='dad_17med',
            field=models.FloatField(blank=True, null=True, verbose_name=b'Valor Pressao'),
        ),
        migrations.AlterField(
            model_name='dados',
            name='dad_17stat',
            field=models.SmallIntegerField(blank=True, null=True, verbose_name=b'Estado Pressao'),
        ),
        migrations.AlterField(
            model_name='dados',
            name='dad_18med',
            field=models.FloatField(blank=True, null=True, verbose_name=b'Valor Rad'),
        ),
        migrations.AlterField(
            model_name='dados',
            name='dad_18stat',
            field=models.SmallIntegerField(blank=True, null=True, verbose_name=b'Estado Rad'),
        ),
        migrations.AlterField(
            model_name='dados',
            name='dad_19med',
            field=models.FloatField(blank=True, null=True, verbose_name=b'Valor Vel'),
        ),
        migrations.AlterField(
            model_name='dados',
            name='dad_19stat',
            field=models.SmallIntegerField(blank=True, null=True, verbose_name=b'Estado Vel'),
        ),
        migrations.AlterField(
            model_name='dados',
            name='dad_1med',
            field=models.FloatField(blank=True, null=True, verbose_name=b'Valor SO2'),
        ),
        migrations.AlterField(
            model_name='dados',
            name='dad_1stat',
            field=models.SmallIntegerField(blank=True, null=True, verbose_name=b'Estado SO2'),
        ),
        migrations.AlterField(
            model_name='dados',
            name='dad_20med',
            field=models.FloatField(blank=True, null=True, verbose_name=b'Valor Dir'),
        ),
        migrations.AlterField(
            model_name='dados',
            name='dad_20stat',
            field=models.SmallIntegerField(blank=True, null=True, verbose_name=b'Estado Dir'),
        ),
        migrations.AlterField(
            model_name='dados',
            name='dad_2med',
            field=models.FloatField(blank=True, null=True, verbose_name=b'Valor NO'),
        ),
        migrations.AlterField(
            model_name='dados',
            name='dad_2stat',
            field=models.SmallIntegerField(blank=True, null=True, verbose_name=b'Estado NO'),
        ),
        migrations.AlterField(
            model_name='dados',
            name='dad_3med',
            field=models.FloatField(blank=True, null=True, verbose_name=b'Valor NO2'),
        ),
        migrations.AlterField(
            model_name='dados',
            name='dad_3stat',
            field=models.SmallIntegerField(blank=True, null=True, verbose_name=b'Estado NO2'),
        ),
        migrations.AlterField(
            model_name='dados',
            name='dad_4med',
            field=models.FloatField(blank=True, null=True, verbose_name=b'Valor NOx'),
        ),
        migrations.AlterField(
            model_name='dados',
            name='dad_4stat',
            field=models.SmallIntegerField(blank=True, null=True, verbose_name=b'Estado NOx'),
        ),
        migrations.AlterField(
            model_name='dados',
            name='dad_5med',
            field=models.FloatField(blank=True, null=True, verbose_name=b'Valor CO'),
        ),
        migrations.AlterField(
            model_name='dados',
            name='dad_5stat',
            field=models.SmallIntegerField(blank=True, null=True, verbose_name=b'Estado CO'),
        ),
        migrations.AlterField(
            model_name='dados',
            name='dad_6med',
            field=models.FloatField(blank=True, null=True, verbose_name=b'Valor O3'),
        ),
        migrations.AlterField(
            model_name='dados',
            name='dad_6stat',
            field=models.SmallIntegerField(blank=True, null=True, verbose_name=b'Estado O3'),
        ),
        migrations.AlterField(
            model_name='dados',
            name='dad_7med',
            field=models.FloatField(blank=True, null=True, verbose_name=b'Valor Prec'),
        ),
        migrations.AlterField(
            model_name='dados',
            name='dad_7stat',
            field=models.SmallIntegerField(blank=True, null=True, verbose_name=b'Estado Prec'),
        ),
        migrations.AlterField(
            model_name='dados',
            name='dad_8med',
            field=models.FloatField(blank=True, null=True, verbose_name=b'Valor Benzeno'),
        ),
        migrations.AlterField(
            model_name='dados',
            name='dad_8stat',
            field=models.SmallIntegerField(blank=True, null=True, verbose_name=b'Estado Benzeno'),
        ),
        migrations.AlterField(
            model_name='dados',
            name='dad_9med',
            field=models.FloatField(blank=True, null=True, verbose_name=b'Valor Tolueno'),
        ),
        migrations.AlterField(
            model_name='dados',
            name='dad_9stat',
            field=models.SmallIntegerField(blank=True, null=True, verbose_name=b'Estado Tolueno'),
        ),
        migrations.AlterField(
            model_name='dados',
            name='dad_data',
            field=models.DateTimeField(blank=True, db_index=True, null=True, verbose_name=b'Data Recolha'),
        ),
        migrations.AlterField(
            model_name='dados',
            name='dad_p_aquisicao',
            field=models.IntegerField(blank=True, null=True, verbose_name=b'P Aquisicao'),
        ),
        migrations.AlterField(
            model_name='dados',
            name='est_id',
            field=models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, to='labqar.Estacao', verbose_name=b'Estacao'),
        ),
        migrations.AlterField(
            model_name='parametro',
            name='cat_id',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='labqar.Categoria'),
        ),
        migrations.AlterField(
            model_name='parametro',
            name='par_casas_decimais',
            field=models.SmallIntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='parametro',
            name='par_codigo',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='parametro',
            name='par_conv_add',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='parametro',
            name='par_conv_mul',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='parametro',
            name='par_limiar',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='parametro',
            name='par_limite',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='parametro',
            name='par_limite_media',
            field=models.SmallIntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='parametro',
            name='par_max_alarme',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='parametro',
            name='par_media_intervalo',
            field=models.SmallIntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='parametro',
            name='par_media_tipo',
            field=models.SmallIntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='parametro',
            name='par_min_alarme',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='parametro',
            name='par_nome',
            field=models.CharField(blank=True, max_length=20, null=True),
        ),
        migrations.AlterField(
            model_name='parametro',
            name='par_nome_completo',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='parametro',
            name='par_perc_validacao_dia',
            field=models.SmallIntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='parametro',
            name='par_perc_validacao_hora',
            field=models.SmallIntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='parametro',
            name='par_tipo',
            field=models.SmallIntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='parametro',
            name='par_unidade_apresent',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='parametro',
            name='par_unidade_armaz',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
    ]
