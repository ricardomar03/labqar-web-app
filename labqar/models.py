# -*- coding: utf-8 -*-
import datetime

import pytz
from dateutil import relativedelta
from django.contrib.auth.models import User
from django.db import models

# Website/Mobile App support models
from django.db.models.signals import post_save
from django.forms import ModelForm, forms
from push_notifications.models import GCMDevice


class Pollutant:
    def __init__(self, value, stat, name, unit):
        self.value = value
        self.stat = stat
        self.name = name
        self.unit = unit


class Measurement:
    def __init__(self, date_time, values):
        self.date_time = date_time
        self.values = values


class Parametro_Local(models.Model):
    UNITY_CHOICES = (
        (u'µg/m3',u'µg/m3'),
        ('ppm', 'ppm'),
        ('ppb', 'ppb'),
        ('W/m2', 'W/m2'),
        ('mm', 'mm'),
        ('mBar', 'mBar'),
        ('m/s', 'm/s'),
        ('ºC', 'ºC'),
        ('ºN', 'ºN'),
        ('%', '%'),
    )
    class Meta:
        verbose_name = "Parametro"
        verbose_name_plural = "Parametros"

    par_id = models.AutoField(primary_key=True)
    par_nome = models.CharField(max_length=20, null=True, blank=True, editable=False)
    par_nome_completo = models.CharField(max_length=50, null=True, blank=True, verbose_name="Nome a apresentar")
    par_unidade_apresent = models.CharField(max_length=50, null=True, choices=UNITY_CHOICES, default=u'µg/m3', verbose_name="Unidade de apresentacao")
    par_disabled = models.BooleanField(default=False,verbose_name="Desativar Parametro")

    def __str__(self):
        return self.par_nome


class Local(models.Model):
    class Meta:
        verbose_name_plural = "Local"

    lcl_id = models.AutoField(primary_key=True)
    lcl_user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Utilizador Associado")
    lcl_nome = models.CharField(max_length=50, verbose_name="Nome")
    lcl_morada = models.CharField(max_length=255, null=True, blank=True, verbose_name="Morada")
    lcl_contacto = models.IntegerField(null=True, blank=True, verbose_name="Contacto")
    lcl_background = models.ImageField(null=True, blank=True, verbose_name="Imagem de Fundo", upload_to='labqar')

    def __str__(self):
        return self.lcl_nome

    def __unicode__(self):
        return self.lcl_nome


class Periodo_Campanha(models.Model):
    PM10_CHOICES = (
        (1, 'Outro'),
        (1.18, 'Trafego'),
        (1.11, 'Fundo'),
    )

    class Meta:
        verbose_name_plural = "Periodo Campanha"

    lcl_id = models.ForeignKey("Local", on_delete=models.CASCADE)
    cam_data_inicio = models.DateTimeField(verbose_name="Data Inicio")
    cam_data_final = models.DateTimeField(verbose_name="Data Fim")
    cam_notas = models.CharField(max_length=255, null=True, blank=True, verbose_name="Notas")
    cam_pm10 = models.FloatField(choices=PM10_CHOICES, default=1, verbose_name="Factor PM10")

    def __str__(self):
        start_date = str(self.cam_data_inicio).split("+")[0].split(":")[0] + ":" + \
                     str(self.cam_data_inicio).split("+")[0].split(":")[1]
        end_date = str(self.cam_data_final).split("+")[0].split(":")[0] + ":" + \
                   str(self.cam_data_final).split("+")[0].split(":")[1]
        return str(self.lcl_id) + " de " + start_date + " a " + end_date

    def __unicode__(self):
        start_date = str(self.cam_data_inicio).split("+")[0].split(":")[0] + ":" + \
                     str(self.cam_data_inicio).split("+")[0].split(":")[1]
        end_date = str(self.cam_data_final).split("+")[0].split(":")[0] + ":" + \
                   str(self.cam_data_final).split("+")[0].split(":")[1]
        return str(self.lcl_id) + " de " + start_date + " a " + end_date


class Historico_Alertas(models.Model):
    class Meta:
        verbose_name = "Alerta"
        verbose_name_plural = "Histórico Alertas"
        ordering = ['-his_data']

    his_id = models.AutoField(primary_key=True)
    his_alerta = models.CharField(max_length=255)
    his_campanha = models.CharField(max_length=255)
    his_data = models.CharField(max_length=255)
    his_codigo = models.IntegerField()
    his_disabled = models.BooleanField()

    def __str__(self):
        return str(self.his_data)

    def __unicode__(self):
        return str(self.his_data)

""" Used Atmis database Models """


class Canal(models.Model):
    class Meta:
        verbose_name = "Canal"
        verbose_name_plural = "Canais"

    can_id = models.AutoField(primary_key=True)
    uni_id = models.ForeignKey("Unidade", on_delete=models.CASCADE)
    par_id = models.ForeignKey("Parametro", on_delete=models.CASCADE)
    can_num_estacao = models.SmallIntegerField(null=True)
    can_num_unidade = models.SmallIntegerField(null=True)
    can_unidade_medida = models.CharField(max_length=6, null=True)
    can_conv_med_mul = models.FloatField(null=True)
    can_conv_med_add = models.FloatField(null=True)
    can_min_medida = models.FloatField(null=True)
    can_max_medida = models.FloatField(null=True)
    can_min_alarme = models.FloatField(null=True)
    can_max_alarme = models.FloatField(null=True)
    can_validacao = models.IntegerField(null=True)
    can_suspenso = models.NullBooleanField(null=True)
    can_background = models.FloatField(null=True)
    can_coeficiente = models.FloatField(null=True)
    can_num_monit = models.SmallIntegerField(null=True)
    ual_meteo = models.NullBooleanField(null=True)
    ual_sin_cmd = models.SmallIntegerField(null=True)
    ual_slope = models.FloatField(null=True)
    ual_y0 = models.FloatField(null=True)
    ual_nome = models.CharField(max_length=5, null=True)
    sam_ganho = models.SmallIntegerField(null=True)
    sam_sin_alarme = models.SmallIntegerField(null=True)
    sam_sin_zero = models.SmallIntegerField(null=True)
    sam_sin_max = models.SmallIntegerField(null=True)
    sam_cmd_zero = models.SmallIntegerField(null=True)
    sam_cmd_max = models.SmallIntegerField(null=True)
    vir_formula = models.CharField(max_length=255, null=True)
    uar_tipo = models.SmallIntegerField(null=True)
    uar_calculo = models.SmallIntegerField(null=True)
    uar_num_entrada = models.SmallIntegerField(null=True)
    can_reg_eventos = models.NullBooleanField(null=True)
    can_addr_eventos = models.SmallIntegerField(null=True)
    can_acumula_eventos = models.NullBooleanField(null=True)

    def __str__(self):
        return str(self.uni_id) + " - " + str(self.par_id)


class Dados(models.Model):
    class Meta:
        verbose_name = "Dados"
        verbose_name_plural = "Dados"
        ordering = ['-dad_data']

    dad_id = models.IntegerField(primary_key=True)
    est_id = models.ForeignKey("Estacao", on_delete=models.CASCADE, verbose_name="Estacao", null=True, blank=True)
    cam_id = models.IntegerField(null=True, verbose_name="Campanha", blank=True)
    dad_data = models.DateTimeField(null=True, verbose_name="Data Recolha", db_index=True, blank=True)
    dad_1med = models.FloatField(null=True, verbose_name="Valor SO2", blank=True)
    dad_1stat = models.SmallIntegerField(null=True, verbose_name="Estado SO2", blank=True)
    dad_2med = models.FloatField(null=True, verbose_name="Valor NO", blank=True)
    dad_2stat = models.SmallIntegerField(null=True, verbose_name="Estado NO", blank=True)
    dad_3med = models.FloatField(null=True, verbose_name="Valor NO2", blank=True)
    dad_3stat = models.SmallIntegerField(null=True, verbose_name="Estado NO2", blank=True)
    dad_4med = models.FloatField(null=True, verbose_name="Valor NOx", blank=True)
    dad_4stat = models.SmallIntegerField(null=True, verbose_name="Estado NOx", blank=True)
    dad_5med = models.FloatField(null=True, verbose_name="Valor CO", blank=True)
    dad_5stat = models.SmallIntegerField(null=True, verbose_name="Estado CO", blank=True)
    dad_6med = models.FloatField(null=True, verbose_name="Valor O3", blank=True)
    dad_6stat = models.SmallIntegerField(null=True, verbose_name="Estado O3", blank=True)
    dad_7med = models.FloatField(null=True, verbose_name="Valor Prec", blank=True)
    dad_7stat = models.SmallIntegerField(null=True, verbose_name="Estado Prec", blank=True)
    dad_8med = models.FloatField(null=True, verbose_name="Valor Benzeno", blank=True)
    dad_8stat = models.SmallIntegerField(null=True, verbose_name="Estado Benzeno", blank=True)
    dad_9med = models.FloatField(null=True, verbose_name="Valor Tolueno", blank=True)
    dad_9stat = models.SmallIntegerField(null=True, verbose_name="Estado Tolueno", blank=True)
    dad_10med = models.FloatField(null=True, verbose_name="Valor Etilbenzeno", blank=True)
    dad_10stat = models.SmallIntegerField(null=True, verbose_name="Estado Etilbenzeno", blank=True)
    dad_11med = models.FloatField(null=True, verbose_name="Valor MPXileno", blank=True)
    dad_11stat = models.SmallIntegerField(null=True, verbose_name="Estado MPXileno", blank=True)
    dad_12med = models.FloatField(null=True, verbose_name="Valor OXileno", blank=True)
    dad_12stat = models.SmallIntegerField(null=True, verbose_name="Estado OXileno", blank=True)
    dad_13med = models.FloatField(null=True, verbose_name="Valor partEnv", blank=True)
    dad_13stat = models.SmallIntegerField(null=True, verbose_name="Estado partEnv", blank=True)
    dad_14med = models.FloatField(null=True, verbose_name="Valor SO2offset", blank=True)
    dad_14stat = models.SmallIntegerField(null=True, verbose_name="Estado SO2offset", blank=True)
    dad_15med = models.FloatField(null=True, verbose_name="Valor Temp", blank=True)
    dad_15stat = models.SmallIntegerField(null=True, verbose_name="Estado Temp", blank=True)
    dad_16med = models.FloatField(null=True, verbose_name="Valor Hum %", blank=True)
    dad_16stat = models.SmallIntegerField(null=True, verbose_name="Estado Hum %", blank=True)
    dad_17med = models.FloatField(null=True, verbose_name="Valor Pressao", blank=True)
    dad_17stat = models.SmallIntegerField(null=True, verbose_name="Estado Pressao", blank=True)
    dad_18med = models.FloatField(null=True, verbose_name="Valor Rad", blank=True)
    dad_18stat = models.SmallIntegerField(null=True, verbose_name="Estado Rad", blank=True)
    dad_19med = models.FloatField(null=True, verbose_name="Valor Vel", blank=True)
    dad_19stat = models.SmallIntegerField(null=True, verbose_name="Estado Vel", blank=True)
    dad_20med = models.FloatField(null=True, verbose_name="Valor Dir", blank=True)
    dad_20stat = models.SmallIntegerField(null=True, verbose_name="Estado Dir", blank=True)
    dad_p_aquisicao = models.IntegerField(null=True, verbose_name="P Aquisicao", blank=True)

    def __str__(self):
        return "Dia " + self.dad_data.strftime("%d-%m-%Y às %H:%M")

    def __unicode__(self):
        return "Dia " + self.dad_data.strftime("%d-%m-%Y às %H:%M")


class Estacao(models.Model):
    class Meta:
        verbose_name = "Estacao"
        verbose_name_plural = "Estacoes"

    est_id = models.AutoField(primary_key=True)
    map_id = models.ForeignKey("Mapa", on_delete=models.CASCADE, null=True)
    red_id = models.ForeignKey("Rede", on_delete=models.CASCADE)
    est_nome = models.CharField(max_length=50, null=True)
    est_abreviatura = models.CharField(max_length=50, null=True)
    est_codigo = models.IntegerField(null=True)
    est_instituicao = models.CharField(max_length=5, null=True)
    est_pos_x = models.IntegerField(null=True)
    est_pos_y = models.IntegerField(null=True)
    est_local = models.CharField(max_length=50, null=True)
    est_data_instal = models.DateTimeField(null=True)
    est_tipo_ligacao = models.SmallIntegerField(null=True)
    est_telefone = models.CharField(max_length=30, null=True)
    est_central_telef = models.NullBooleanField(null=True)
    est_indicativo = models.CharField(max_length=5, null=True)
    est_ultima_revisao = models.DateTimeField(null=True)
    est_foto = models.ImageField(null=True)
    est_obs = models.CharField(max_length=50, null=True)
    est_alarme_a = models.CharField(max_length=30, null=True)
    est_tel_alarme_a = models.CharField(max_length=30, null=True)
    est_alarme_b = models.CharField(max_length=30, null=True)
    est_tel_alarme_b = models.CharField(max_length=30, null=True)
    est_alarme_c = models.CharField(max_length=30, null=True)
    est_tel_alarme_c = models.CharField(max_length=30, null=True)
    est_num_tent = models.SmallIntegerField(null=True)
    est_atraso_tent = models.IntegerField(null=True)
    est_p_aq_normal = models.IntegerField(null=True)
    est_p_aq_alarme = models.IntegerField(null=True)
    est_perc_validacao = models.SmallIntegerField(null=True)
    est_num_canais_activ = models.SmallIntegerField(null=True)
    est_mascara = models.IntegerField(null=True)
    est_data_validacao = models.DateTimeField(null=True)
    est_comunicacao = models.NullBooleanField(null=True)
    est_modem_init = models.CharField(max_length=32, null=True)
    est_modem_dial = models.CharField(max_length=32, null=True)
    est_template = models.NullBooleanField(null=True)
    est_relogio_sinc = models.NullBooleanField(null=True)
    est_autonomia = models.SmallIntegerField(null=True)
    est_meteo_est_id = models.IntegerField(null=True)
    est_meteo_vel_id = models.IntegerField(null=True)
    est_meteo_dir_id = models.IntegerField(null=True)
    est_meteo_used = models.NullBooleanField(null=True)
    est_auto_validacao = models.NullBooleanField(null=True)
    cam_id = models.IntegerField(null=True)
    est_porta_serie = models.CharField(max_length=6, null=True)
    est_tipo = models.IntegerField(null=True)
    est_activa = models.NullBooleanField(null=True)
    est_data_ult_act = models.DateTimeField(null=True)

    def __str__(self):
        return self.est_nome


class Estado(models.Model):
    class Meta:
        verbose_name = "Estado"
        verbose_name_plural = "Estados"

    est_id = models.ForeignKey("Estacao", on_delete=models.CASCADE, primary_key=True)
    est_data = models.DateTimeField(null=True)
    est_1med = models.FloatField(null=True)
    est_1mode = models.SmallIntegerField(null=True)
    est_1valido = models.NullBooleanField(null=True)
    est_1alarme = models.SmallIntegerField(null=True)
    est_2med = models.FloatField(null=True)
    est_2mode = models.SmallIntegerField(null=True)
    est_2valido = models.NullBooleanField(null=True)
    est_2alarme = models.SmallIntegerField(null=True)
    est_3med = models.FloatField(null=True)
    est_3mode = models.SmallIntegerField(null=True)
    est_3valido = models.NullBooleanField(null=True)
    est_3alarme = models.SmallIntegerField(null=True)
    est_4med = models.FloatField(null=True)
    est_4mode = models.SmallIntegerField(null=True)
    est_4valido = models.NullBooleanField(null=True)
    est_4alarme = models.SmallIntegerField(null=True)
    est_5med = models.FloatField(null=True)
    est_5mode = models.SmallIntegerField(null=True)
    est_5valido = models.NullBooleanField(null=True)
    est_5alarme = models.SmallIntegerField(null=True)
    est_6med = models.FloatField(null=True)
    est_6mode = models.SmallIntegerField(null=True)
    est_6valido = models.NullBooleanField(null=True)
    est_6alarme = models.SmallIntegerField(null=True)
    est_7med = models.FloatField(null=True)
    est_7mode = models.SmallIntegerField(null=True)
    est_7valido = models.NullBooleanField(null=True)
    est_7alarme = models.SmallIntegerField(null=True)
    est_8med = models.FloatField(null=True)
    est_8mode = models.SmallIntegerField(null=True)
    est_8valido = models.NullBooleanField(null=True)
    est_8alarme = models.SmallIntegerField(null=True)
    est_9med = models.FloatField(null=True)
    est_9mode = models.SmallIntegerField(null=True)
    est_9valido = models.NullBooleanField(null=True)
    est_9alarme = models.SmallIntegerField(null=True)
    est_10med = models.FloatField(null=True)
    est_10mode = models.SmallIntegerField(null=True)
    est_10valido = models.NullBooleanField(null=True)
    est_10alarme = models.SmallIntegerField(null=True)
    est_11med = models.FloatField(null=True)
    est_11mode = models.SmallIntegerField(null=True)
    est_11valido = models.NullBooleanField(null=True)
    est_11alarme = models.SmallIntegerField(null=True)
    est_12med = models.FloatField(null=True)
    est_12mode = models.SmallIntegerField(null=True)
    est_12valido = models.NullBooleanField(null=True)
    est_12alarme = models.SmallIntegerField(null=True)
    est_13med = models.FloatField(null=True)
    est_13mode = models.SmallIntegerField(null=True)
    est_13valido = models.NullBooleanField(null=True)
    est_13alarme = models.SmallIntegerField(null=True)
    est_14med = models.FloatField(null=True)
    est_14mode = models.SmallIntegerField(null=True)
    est_14valido = models.NullBooleanField(null=True)
    est_14alarme = models.SmallIntegerField(null=True)
    est_15med = models.FloatField(null=True)
    est_15mode = models.SmallIntegerField(null=True)
    est_15valido = models.NullBooleanField(null=True)
    est_15alarme = models.SmallIntegerField(null=True)
    est_16med = models.FloatField(null=True)
    est_16mode = models.SmallIntegerField(null=True)
    est_16valido = models.NullBooleanField(null=True)
    est_16alarme = models.SmallIntegerField(null=True)
    est_17med = models.FloatField(null=True)
    est_17mode = models.SmallIntegerField(null=True)
    est_17valido = models.NullBooleanField(null=True)
    est_17alarme = models.SmallIntegerField(null=True)
    est_18med = models.FloatField(null=True)
    est_18mode = models.SmallIntegerField(null=True)
    est_18valido = models.NullBooleanField(null=True)
    est_18alarme = models.SmallIntegerField(null=True)
    est_19med = models.FloatField(null=True)
    est_19mode = models.SmallIntegerField(null=True)
    est_19valido = models.NullBooleanField(null=True)
    est_19alarme = models.SmallIntegerField(null=True)
    est_20med = models.FloatField(null=True)
    est_20mode = models.SmallIntegerField(null=True)
    est_20valido = models.NullBooleanField(null=True)
    est_20alarme = models.SmallIntegerField(null=True)

    def __str__(self):
        return str(self.est_id) + " - " + str(self.est_data)


class EstadoInterno(models.Model):
    class Meta:
        verbose_name = "Estado Interno"
        verbose_name_plural = "Estados Internos"

    uni_id = models.ForeignKey("Unidade", on_delete=models.CASCADE, primary_key=True)
    est_data = models.DateTimeField(null=True)
    est_1nome = models.CharField(max_length=30, null=True)
    est_1unidadmed = models.CharField(max_length=10, null=True)
    est_1valor = models.FloatField(null=True)
    est_1modo = models.SmallIntegerField(null=True)
    est_1valido = models.NullBooleanField(null=True)
    est_2nome = models.CharField(max_length=30, null=True)
    est_2unidadmed = models.CharField(max_length=10, null=True)
    est_2valor = models.FloatField(null=True)
    est_2modo = models.SmallIntegerField(null=True)
    est_2valido = models.NullBooleanField(null=True)
    est_3nome = models.CharField(max_length=30, null=True)
    est_3unidadmed = models.CharField(max_length=10, null=True)
    est_3valor = models.FloatField(null=True)
    est_3modo = models.SmallIntegerField(null=True)
    est_3valido = models.NullBooleanField(null=True)
    est_4nome = models.CharField(max_length=30, null=True)
    est_4unidadmed = models.CharField(max_length=10, null=True)
    est_4valor = models.FloatField(null=True)
    est_4modo = models.SmallIntegerField(null=True)
    est_4valido = models.NullBooleanField(null=True)
    est_5nome = models.CharField(max_length=30, null=True)
    est_5unidadmed = models.CharField(max_length=10, null=True)
    est_5valor = models.FloatField(null=True)
    est_5modo = models.SmallIntegerField(null=True)
    est_5valido = models.NullBooleanField(null=True)
    est_6nome = models.CharField(max_length=30, null=True)
    est_6unidadmed = models.CharField(max_length=10, null=True)
    est_6valor = models.FloatField(null=True)
    est_6modo = models.SmallIntegerField(null=True)
    est_6valido = models.NullBooleanField(null=True)
    est_7nome = models.CharField(max_length=30, null=True)
    est_7unidadmed = models.CharField(max_length=10, null=True)
    est_7valor = models.FloatField(null=True)
    est_7modo = models.SmallIntegerField(null=True)
    est_7valido = models.NullBooleanField(null=True)
    est_8nome = models.CharField(max_length=30, null=True)
    est_8unidadmed = models.CharField(max_length=10, null=True)
    est_8valor = models.FloatField(null=True)
    est_8modo = models.SmallIntegerField(null=True)
    est_8valido = models.NullBooleanField(null=True)
    est_9nome = models.CharField(max_length=30, null=True)
    est_9unidadmed = models.CharField(max_length=10, null=True)
    est_9valor = models.FloatField(null=True)
    est_9modo = models.SmallIntegerField(null=True)
    est_9valido = models.NullBooleanField(null=True)
    est_10nome = models.CharField(max_length=30, null=True)
    est_10unidadmed = models.CharField(max_length=10, null=True)
    est_10valor = models.FloatField(null=True)
    est_10modo = models.SmallIntegerField(null=True)
    est_10valido = models.NullBooleanField(null=True)
    est_11nome = models.CharField(max_length=30, null=True)
    est_11unidadmed = models.CharField(max_length=10, null=True)
    est_11valor = models.FloatField(null=True)
    est_11modo = models.SmallIntegerField(null=True)
    est_11valido = models.NullBooleanField(null=True)
    est_12nome = models.CharField(max_length=30, null=True)
    est_12unidadmed = models.CharField(max_length=10, null=True)
    est_12valor = models.FloatField(null=True)
    est_12modo = models.SmallIntegerField(null=True)
    est_12valido = models.NullBooleanField(null=True)
    est_13nome = models.CharField(max_length=30, null=True)
    est_13unidadmed = models.CharField(max_length=10, null=True)
    est_13valor = models.FloatField(null=True)
    est_13modo = models.SmallIntegerField(null=True)
    est_13valido = models.NullBooleanField(null=True)
    est_14nome = models.CharField(max_length=30, null=True)
    est_14unidadmed = models.CharField(max_length=10, null=True)
    est_14valor = models.FloatField(null=True)
    est_14modo = models.SmallIntegerField(null=True)
    est_14valido = models.NullBooleanField(null=True)
    est_15nome = models.CharField(max_length=30, null=True)
    est_15unidadmed = models.CharField(max_length=10, null=True)
    est_15valor = models.FloatField(null=True)
    est_15modo = models.SmallIntegerField(null=True)
    est_15valido = models.NullBooleanField(null=True)
    est_16nome = models.CharField(max_length=30, null=True)
    est_16unidadmed = models.CharField(max_length=10, null=True)
    est_16valor = models.FloatField(null=True)
    est_16modo = models.SmallIntegerField(null=True)
    est_16valido = models.NullBooleanField(null=True)

    def __str__(self):
        return str(self.uni_id) + " - " + str(self.est_data)


class Mapa(models.Model):
    class Meta:
        verbose_name = "Mapa"
        verbose_name_plural = "Mapas"

    map_id = models.AutoField(primary_key=True)
    map_nome = models.CharField(max_length=50, null=True)
    map_ficheiro = models.CharField(max_length=255, null=True)

    def __str__(self):
        return self.map_nome


class Parametro(models.Model):
    class Meta:
        verbose_name = "Parametro"
        verbose_name_plural = "Parametros"

    par_id = models.AutoField(primary_key=True)
    cat_id = models.ForeignKey("Categoria", on_delete=models.CASCADE, null=True, blank=True, editable=False)
    par_nome = models.CharField(max_length=20, null=True, blank=True, editable=False)
    par_nome_completo = models.CharField(max_length=50, null=True, blank=True, verbose_name="Nome a apresentar")
    par_codigo = models.IntegerField(null=True, blank=True, editable=False)
    par_unidade_armaz = models.CharField(max_length=50, null=True, blank=True, editable=False)
    par_unidade_apresent = models.CharField(max_length=50, null=True, blank=True, verbose_name="Unidade de medicao")
    par_conv_mul = models.FloatField(null=True, blank=True, editable=False)
    par_conv_add = models.FloatField(null=True, blank=True, editable=False)
    par_casas_decimais = models.SmallIntegerField(null=True, blank=True, editable=False)
    par_limiar = models.FloatField(null=True, blank=True, editable=False)
    par_limite = models.FloatField(null=True, blank=True, editable=False)
    par_perc_validacao_hora = models.SmallIntegerField(null=True, blank=True, editable=False)
    par_perc_validacao_dia = models.SmallIntegerField(null=True, blank=True, editable=False)
    par_media_tipo = models.SmallIntegerField(null=True, blank=True, editable=False)
    par_media_intervalo = models.SmallIntegerField(null=True, blank=True, editable=False)
    par_visivel = models.NullBooleanField(null=True, blank=True, editable=False)
    par_min_alarme = models.FloatField(null=True, blank=True, editable=False)
    par_max_alarme = models.FloatField(null=True, blank=True, editable=False)
    par_limite_media = models.SmallIntegerField(null=True, blank=True, editable=False)
    par_tipo = models.SmallIntegerField(null=True, blank=True, editable=False)

    def __str__(self):
        return self.par_nome


class Recolha(models.Model):
    class Meta:
        verbose_name = "Recolha"
        verbose_name_plural = "Recolhas"

    rec_id = models.AutoField(primary_key=True)
    est_id = models.ForeignKey("Estacao", on_delete=models.CASCADE)
    rec_hora = models.SmallIntegerField(null=True)
    rec_dias_semana = models.SmallIntegerField(null=True)

    def __str__(self):
        return str(self.est_id) + " - " + str(self.rec_hora) + " - " + str(self.rec_dias_semana)


class Rede(models.Model):
    class Meta:
        verbose_name = "Rede"
        verbose_name_plural = "Redes"

    red_id = models.AutoField(primary_key=True)
    red_descricao = models.CharField(max_length=40, null=True)

    def __str__(self):
        return self.red_descricao


class Unidade(models.Model):
    class Meta:
        verbose_name = "Unidade"
        verbose_name_plural = "Unidades"

    uni_id = models.AutoField(primary_key=True)
    est_id = models.ForeignKey("Estacao", on_delete=models.CASCADE)
    uni_tipo = models.CharField(max_length=12, null=True)
    uni_num_serie = models.CharField(max_length=8, null=True)
    uni_nome = models.CharField(max_length=30, null=True)
    uni_ual_lres = models.IntegerField(null=True)
    uni_ual_hres = models.IntegerField(null=True)
    uni_dt_programa = models.DateTimeField(null=True)
    uni_ual_prodid = models.CharField(max_length=15, null=True)
    uni_ual_majver = models.SmallIntegerField(null=True)
    uni_ual_minver = models.SmallIntegerField(null=True)
    uni_ual_revver = models.SmallIntegerField(null=True)
    uni_sam_calib_zero = models.IntegerField(null=True)
    uni_sam_calib_max = models.IntegerField(null=True)
    uni_sam_sinc_calibh = models.SmallIntegerField(null=True)
    uni_sam_sinc_calibm = models.SmallIntegerField(null=True)
    uni_sam_ciclo_calib = models.SmallIntegerField(null=True)
    uni_asm_endereco = models.CharField(max_length=4, null=True)
    uni_asm_offset = models.IntegerField(null=True)
    uni_asm_gama = models.SmallIntegerField(null=True)
    uni_asm_tempo_resp = models.SmallIntegerField(null=True)
    uni_asm_unidade = models.SmallIntegerField(null=True)
    uni_asm_calib_zero_ref = models.SmallIntegerField(null=True)
    uni_asm_calib_zero = models.SmallIntegerField(null=True)
    uni_asm_calib_auto = models.SmallIntegerField(null=True)
    uni_asm_calib_max = models.SmallIntegerField(null=True)
    uni_asm_dur_zero = models.IntegerField(null=True)
    uni_asm_dur_max = models.IntegerField(null=True)
    uni_asm_span = models.IntegerField(null=True)
    uni_asm_banco = models.SmallIntegerField(null=True)
    uni_versao = models.CharField(max_length=30, null=True)
    uni_modelo = models.CharField(max_length=30, null=True)
    uni_suspenso = models.NullBooleanField(null=True)
    uni_dt_recolha = models.DateTimeField(null=True)
    uni_tea_tavrg = models.SmallIntegerField(null=True)
    uni_tea_ctemp = models.NullBooleanField(null=True)
    uni_tea_cpres = models.NullBooleanField(null=True)
    uni_asm_modo = models.SmallIntegerField(null=True)
    uni_ccr_nloca_amostra = models.IntegerField(null=True)
    uni_ccr_nloca_total = models.IntegerField(null=True)
    uni_dtl_password = models.CharField(max_length=16, null=True)
    uni_obs_intervalo_s = models.IntegerField(null=True)
    uni_obs_intervalo_p = models.IntegerField(null=True)
    uni_obs_intervalo_q = models.IntegerField(null=True)
    uni_obs_bateria = models.NullBooleanField(null=True)
    uni_obs_cartridge = models.SmallIntegerField(null=True)
    uni_obs_apaga_dados = models.NullBooleanField(null=True)
    uni_ccr_nloca_eventos = models.IntegerField(null=True)
    uni_ccr_nloca_total_eventos = models.IntegerField(null=True)

    def __str__(self):
        return self.uni_nome


class Alertas_Concentracao(models.Model):
    class Meta:
        verbose_name_plural = "Alertas Concentracoes"

    alr_id = models.AutoField(primary_key=True)
    alr_parametro = models.ForeignKey(Parametro_Local, on_delete=models.CASCADE, verbose_name="Parametro Associado")
    alr_valor_max = models.IntegerField(verbose_name="Valor Maximo")
    alr_disabled = models.BooleanField(default=False, verbose_name="Desativar notificações para clientes")

    def __str__(self):
        return str(self.alr_parametro)

    def __unicode__(self):
        return str(self.alr_parametro)


def data_to_pollutants(entries, partEnv_factor):
    measurements = []
    try:
        parameters = Parametro_Local.objects.all()
    except:
        return []

    for parameter in parameters:
        if parameter.par_nome == 'SO2':
            so2_parameters = parameter
        elif parameter.par_nome == 'NO':
            no_parameters = parameter
        elif parameter.par_nome == 'NO2':
            no2_parameters = parameter
        elif parameter.par_nome == 'NOx':
            nox_parameters = parameter
        elif parameter.par_nome == 'CO':
            co_parameters = parameter
        elif parameter.par_nome == 'O3':
            o3_parameters = parameter
        elif parameter.par_nome == 'Prec':
            prec_parameters = parameter
        elif parameter.par_nome == 'Benzeno':
            benzeno_parameters = parameter
        elif parameter.par_nome == 'Tolueno':
            tolueno_parameters = parameter
        elif parameter.par_nome == 'Etilbenzeno':
            etilbenzeno_parameters = parameter
        elif parameter.par_nome == 'MPXileno':
            mpxileno_parameters = parameter
        elif parameter.par_nome == 'OXileno':
            oxileno_parameters = parameter
        elif parameter.par_nome == 'SO2offset':
            so2offset_parameters = parameter
        elif parameter.par_nome == 'TEMP':
            temp_parameters = parameter
        elif parameter.par_nome == 'Hum':
            hum_parameters = parameter
        elif parameter.par_nome == 'PM10':
            partEnv_parameters = parameter
        elif parameter.par_nome == 'Pressao':
            pressao_parameters = parameter
        elif parameter.par_nome == 'Rad':
            rad_parameters = parameter
        elif parameter.par_nome == 'Vel':
            vel_parameters = parameter
        elif parameter.par_nome == 'Dir':
            dir_parameters = parameter

    for entry in entries:
        pollutants = {}

        if entry.dad_1med is None or entry.dad_1med == "" or entry.dad_1med == -32768:
            so2_value = 0.0
        else:
            so2_value = round(entry.dad_1med * 2.66, 2)
        if entry.dad_1stat is None or entry.dad_1stat == "" or entry.dad_1stat == -32768:
            so2_stat = -1
        else:
            so2_stat = entry.dad_1stat
        so2 = Pollutant(so2_value, so2_stat, so2_parameters.par_nome_completo,
                        partEnv_parameters.par_unidade_apresent)
        pollutants["SO2"] = so2

        if entry.dad_2med is None or entry.dad_2med == "" or entry.dad_2med == -32768:
            no_value = 0.0
        else:
            no_value = round(entry.dad_2med * 1.247, 2)
        if entry.dad_2stat is None or entry.dad_2stat == "" or entry.dad_2stat == -32768:
            no_stat = -1
        else:
            no_stat = entry.dad_2stat
        no = Pollutant(no_value, no_stat, no_parameters.par_nome_completo,
                       partEnv_parameters.par_unidade_apresent)
        pollutants["NO"] = no

        if entry.dad_3med is None or entry.dad_3med == "" or entry.dad_3med == -32768:
            no2_value = 0.0
        else:
            no2_value = round(entry.dad_3med * 1.912, 2)
        if entry.dad_3stat is None or entry.dad_3stat == "" or entry.dad_3stat == -32768:
            no2_stat = -1
        else:
            no2_stat = entry.dad_3stat
        no2 = Pollutant(no2_value, no2_stat, no2_parameters.par_nome_completo,
                        partEnv_parameters.par_unidade_apresent)
        pollutants["NO2"] = no2

        if entry.dad_4med is None or entry.dad_4med == "" or entry.dad_4med == -32768:
            nox_value = 0.0
        else:
            nox_value = round(entry.dad_4med * 1.912, 2)
        if entry.dad_4stat is None or entry.dad_4stat == "" or entry.dad_4stat == -32768:
            nox_stat = -1
        else:
            nox_stat = entry.dad_3stat
        nox = Pollutant(nox_value, nox_stat, nox_parameters.par_nome_completo,
                        partEnv_parameters.par_unidade_apresent)
        pollutants["NOx"] = nox

        if entry.dad_5med is None or entry.dad_5med == "" or entry.dad_5med == -32768:
            co_value = 0.0
        else:
            co_value = round((entry.dad_5med - 10) * 1.16 * 1000, 2)
        if entry.dad_5stat is None or entry.dad_5stat == "" or entry.dad_5stat == -32768:
            co_stat = -1
        else:
            co_stat = entry.dad_5stat
        co = Pollutant(co_value, co_stat, co_parameters.par_nome_completo,
                       partEnv_parameters.par_unidade_apresent)
        pollutants["CO"] = co

        if entry.dad_6med is None or entry.dad_6med == "" or entry.dad_6med == -32768:
            o3_value = 0.0
        else:
            o3_value = round(entry.dad_6med * 2, 2)
        if entry.dad_6stat is None or entry.dad_6stat == "" or entry.dad_6stat == -32768:
            o3_stat = -1
        else:
            o3_stat = entry.dad_6stat
        o3 = Pollutant(o3_value, o3_stat, o3_parameters.par_nome_completo,
                       o3_parameters.par_unidade_apresent)
        pollutants["O3"] = o3

        if entry.dad_7med is None or entry.dad_7med == "" or entry.dad_7med == -32768:
            prec_value = 0.0
        else:
            prec_value = round(entry.dad_7med, 2)
        if entry.dad_7stat is None or entry.dad_7stat == "" or entry.dad_7stat == -32768:
            prec_stat = -1
        else:
            prec_stat = entry.dad_7stat
        prec = Pollutant(prec_value, prec_stat, prec_parameters.par_nome_completo,
                         prec_parameters.par_unidade_apresent)
        pollutants["Prec"] = prec

        if entry.dad_8med is None or entry.dad_8med == "" or entry.dad_8med == -32768:
            benzeno_value = 0.0
        else:
            benzeno_value = round(entry.dad_8med * 3.24, 2)
        if entry.dad_8stat is None or entry.dad_8stat == "" or entry.dad_8stat == -32768:
            benzeno_stat = -1
        else:
            benzeno_stat = entry.dad_8stat
        benzeno = Pollutant(benzeno_value, benzeno_stat, benzeno_parameters.par_nome_completo,
                            partEnv_parameters.par_unidade_apresent)
        pollutants["Benzeno"] = benzeno

        if entry.dad_9med is None or entry.dad_9med == "" or entry.dad_9med == -32768:
            tolueno_value = 0.0
        else:
            tolueno_value = round(entry.dad_9med, 2)
        if entry.dad_9stat is None or entry.dad_9stat == "" or entry.dad_9stat == -32768:
            tolueno_stat = -1
        else:
            tolueno_stat = entry.dad_9stat
        tolueno = Pollutant(tolueno_value, tolueno_stat, tolueno_parameters.par_nome_completo,
                            tolueno_parameters.par_unidade_apresent)
        pollutants["Tolueno"] = tolueno

        if entry.dad_10med is None or entry.dad_10med == "" or entry.dad_10med == -32768:
            etilbenzeno_value = 0.0
        else:
            etilbenzeno_value = round(entry.dad_10med, 2)
        if entry.dad_10stat is None or entry.dad_10stat == "" or entry.dad_10stat == -32768:
            etilbenzeno_stat = -1
        else:
            etilbenzeno_stat = entry.dad_10stat
        etilbenzeno = Pollutant(etilbenzeno_value, etilbenzeno_stat, etilbenzeno_parameters.par_nome_completo,
                                etilbenzeno_parameters.par_unidade_apresent)
        pollutants["Etilbenzeno"] = etilbenzeno

        if entry.dad_11med is None or entry.dad_11med == "" or entry.dad_11med == -32768:
            mpxileno_value = 0.0
        else:
            mpxileno_value = round(entry.dad_11med, 2)
        if entry.dad_11stat is None or entry.dad_11stat == "" or entry.dad_11stat == -32768:
            mpxileno_stat = -1
        else:
            mpxileno_stat = entry.dad_11stat
        mpxileno = Pollutant(mpxileno_value, mpxileno_stat, mpxileno_parameters.par_nome_completo,
                             mpxileno_parameters.par_unidade_apresent)
        pollutants["MPXileno"] = mpxileno

        if entry.dad_12med is None or entry.dad_12med == "" or entry.dad_12med == -32768:
            oxileno_value = 0.0
        else:
            oxileno_value = round(entry.dad_12med, 2)
        if entry.dad_12stat is None or entry.dad_12stat == "" or entry.dad_12stat == -32768:
            oxileno_stat = -1
        else:
            oxileno_stat = entry.dad_12stat
        oxileno = Pollutant(oxileno_value, oxileno_stat, oxileno_parameters.par_nome_completo,
                            oxileno_parameters.par_unidade_apresent)
        pollutants["OXileno"] = oxileno

        if entry.dad_13med is None or entry.dad_13med == "" or entry.dad_13med == -32768:
            partEnv_value = 0.0
        else:
            partEnv_value = round(entry.dad_13med * partEnv_factor, 2)
        if entry.dad_13stat is None or entry.dad_13stat == "" or entry.dad_13stat == -32768:
            partEnv_stat = -1
        else:
            partEnv_stat = entry.dad_13stat
        partEnv = Pollutant(partEnv_value, partEnv_stat, partEnv_parameters.par_nome_completo,
                            partEnv_parameters.par_unidade_apresent)
        pollutants["PM10"] = partEnv

        if entry.dad_14med is None or entry.dad_14med == "" or entry.dad_14med == -32768:
            so2offset_value = 0.0
        else:
            so2offset_value = round(entry.dad_14med, 2)
        if entry.dad_14stat is None or entry.dad_14stat == "" or entry.dad_14stat == -32768:
            so2offset_stat = -1
        else:
            so2offset_stat = entry.dad_14stat
        so2offset = Pollutant(so2offset_value, so2offset_stat, so2offset_parameters.par_nome_completo,
                              so2offset_parameters.par_unidade_apresent)
        pollutants["SO2offset"] = so2offset

        if entry.dad_15med is None or entry.dad_15med == "" or entry.dad_15med == -32768:
            temp_value = 0.0
        else:
            temp_value = round(entry.dad_15med, 2)
        if entry.dad_15stat is None or entry.dad_15stat == "" or entry.dad_15stat == -32768:
            temp_stat = -1
        else:
            temp_stat = entry.dad_15stat
        temp = Pollutant(temp_value, temp_stat, temp_parameters.par_nome_completo,
                         temp_parameters.par_unidade_apresent)
        pollutants["TEMP"] = temp

        if entry.dad_16med is None or entry.dad_16med == "" or entry.dad_16med == -32768:
            hum_value = 0.0
        else:
            hum_value = round(entry.dad_16med, 2)
        if entry.dad_16stat is None or entry.dad_16stat == "" or entry.dad_16stat == -32768:
            hum_stat = -1
        else:
            hum_stat = entry.dad_16stat
        hum = Pollutant(hum_value, hum_stat, hum_parameters.par_nome_completo,
                        hum_parameters.par_unidade_apresent)
        pollutants["Hum"] = hum

        if entry.dad_17med is None or entry.dad_17med == "" or entry.dad_17med == -32768:
            pressao_value = 0.0
        else:
            pressao_value = round(entry.dad_17med, 2)
        if entry.dad_17stat is None or entry.dad_17stat == "" or entry.dad_17stat == -32768:
            pressao_stat = -1
        else:
            pressao_stat = entry.dad_17stat
        pressao = Pollutant(pressao_value, pressao_stat, pressao_parameters.par_nome_completo,
                            pressao_parameters.par_unidade_apresent)
        pollutants["Pressao"] = pressao

        if entry.dad_18med is None or entry.dad_18med == "" or entry.dad_18med == -32768:
            rad_value = 0.0
        else:
            rad_value = round(entry.dad_18med, 2)
        if entry.dad_18stat is None or entry.dad_18stat == "" or entry.dad_18stat == -32768:
            rad_stat = -1
        else:
            rad_stat = entry.dad_18stat
        rad = Pollutant(rad_value, rad_stat, rad_parameters.par_nome_completo,
                        rad_parameters.par_unidade_apresent)
        pollutants["Rad"] = rad

        if entry.dad_19med is None or entry.dad_19med == "" or entry.dad_19med == -32768:
            vel_value = 0.0
        else:
            vel_value = round(entry.dad_19med, 2)
        if entry.dad_19stat is None or entry.dad_19stat == "" or entry.dad_19stat == -32768:
            vel_stat = -1
        else:
            vel_stat = entry.dad_19stat
        vel = Pollutant(vel_value, vel_stat, vel_parameters.par_nome_completo,
                        vel_parameters.par_unidade_apresent)
        pollutants["Vel"] = vel

        if entry.dad_20med is None or entry.dad_20med == "" or entry.dad_20med == -32768:
            dir_value = 0.0
        else:
            dir_value = round(entry.dad_20med, 2)
        if entry.dad_20stat is None or entry.dad_20stat == "" or entry.dad_20stat == -32768:
            dir_stat = -1
        else:
            dir_stat = entry.dad_20stat
        dir = Pollutant(dir_value, dir_stat, dir_parameters.par_nome_completo,
                        dir_parameters.par_unidade_apresent)
        pollutants["Dir"] = dir

        date = entry.dad_data.isoformat().split("+")[0]  # Removes timezone
        date = date.split("T")[0] + " " + date.split("T")[1]  # Removes T between date and time
        date = date.split(":")[0] + ":" + date.split(":")[1]  # Removes Seconds

        measurements.append(Measurement(date, pollutants))

    return measurements


def on_data_save(sender, instance, **kwargs):
    if kwargs['created']:  # just on creation (not update)
        measurements = data_to_pollutants([instance], 1)

        utc = pytz.utc
        date_time = utc.localize(datetime.datetime.strptime(measurements[0].date_time, '%Y-%m-%d %H:%M'))
        if date_time.minute == 0:
            previous_update = Dados.objects.filter(dad_data__lt=date_time).filter(dad_data__minute=0).latest("dad_data")

            if relativedelta.relativedelta(date_time, previous_update.dad_data).hours >= 3:
                campaigns = Periodo_Campanha.objects.filter(cam_data_final__gte=date_time)
                if campaigns:
                    for campaign in campaigns:
                        alert_history = Historico_Alertas(
                            his_alerta="Verificar medições",
                            his_campanha=campaign,
                            his_data=measurements[0].date_time,
                            his_codigo=0,
                            his_disabled=True)
                        alert_history.save()
                else:
                    alert_history = Historico_Alertas(
                        his_alerta="Verificar medições",
                        his_campanha="Nenhuma",
                        his_data=measurements[0].date_time,
                        his_codigo=0,
                        his_disabled=True)
                    alert_history.save()
                try:
                    devices = GCMDevice.objects.filter(user__is_staff=True)
                    devices.send_message(
                        "Verificar medições")
                except Exception as e:
                    print(str(e))

        for value in measurements[0].values:
            if measurements[0].values[value].stat > 0 and datetime.datetime.strptime(measurements[0].date_time, "%Y-%m-%d %H:%M").minute == 0:
                date = datetime.datetime.strptime(measurements[0].date_time, "%Y-%m-%d %H:%M")
                campaigns = Periodo_Campanha.objects.filter(cam_data_final__gte=date)
                if campaigns:
                    for campaign in campaigns:
                        alert_history = Historico_Alertas(his_alerta="Verificar medição de " + measurements[0].values[value].name,
                                                          his_campanha=campaign,
                                                          his_data=measurements[0].date_time,
                                                          his_codigo=measurements[0].values[value].stat,
                                                          his_disabled=True)
                        alert_history.save()
                else:
                    alert_history = Historico_Alertas(
                        his_alerta="Verificar medição de " + measurements[0].values[value].name,
                        his_campanha="Nenhuma",
                        his_data=measurements[0].date_time,
                        his_codigo=measurements[0].values[value].stat,
                        his_disabled=True)
                    alert_history.save()
                try:
                    devices = GCMDevice.objects.filter(user__is_staff=True)
                    devices.send_message(
                        "Verificar medição de " + measurements[0].values[value].name)
                except Exception as e:
                    print(str(e))

        try:
            alerts = Alertas_Concentracao.objects.all()
        except:
            pass

        if alerts is not None:
            for alert in alerts:
                lim_max = alert.alr_valor_max
                par = alert.alr_parametro
                if measurements[0].values[par.par_nome].value > lim_max and\
                        datetime.datetime.strptime(measurements[0].date_time, "%Y-%m-%d %H:%M").minute == 0:
                    try:
                        devices = GCMDevice.objects.filter(user__is_staff=True)
                        devices.send_message(
                            "A concentracao de " + par.par_nome_completo + " ultrapassou o valor limite!")
                    except Exception as e:
                        date = datetime.datetime.strptime(measurements[0].date_time, "%Y-%m-%d %H:%M")

                        campaigns = Periodo_Campanha.objects.filter(cam_data_final__gte=date)
                        if campaigns:
                            for campaign in campaigns:
                                alert_history = Historico_Alertas(his_alerta=
                                                                  "A concentracao de " + par.par_nome_completo + " ultrapassou o valor limite!",
                                                                  his_campanha=campaign,
                                                                  his_data=measurements[0].date_time,
                                                                  his_codigo=0,
                                                                  his_disabled=alert.alr_disabled)
                                alert_history.save()
                                try:
                                    if alert.alr_disabled is False:
                                        devices_campaign = GCMDevice.objects.filter(user=campaign.lcl_id.lcl_user)
                                        devices_campaign.send_message(
                                        "A concentracao de " + par.par_nome_completo + " ultrapassou o valor limite!")
                                except Exception as e:
                                    print(str(e))
                        else:
                            alert_history = Historico_Alertas(his_alerta=
                                                              "A concentracao de " + par.par_nome_completo + " ultrapassou o valor limite!",
                                                              his_campanha="Nenhuma",
                                                              his_data=measurements[0].date_time,
                                                              his_codigo=0,
                                                                  his_disabled=alert.alr_disabled)
                            alert_history.save()
                    else:
                        date = datetime.datetime.strptime(measurements[0].date_time, "%Y-%m-%d %H:%M")

                        campaigns = Periodo_Campanha.objects.filter(cam_data_final__gte=date)
                        if campaigns:
                            for campaign in campaigns:
                                alert_history = Historico_Alertas(his_alerta=
                                                                  "A concentracao de " + par.par_nome_completo + " ultrapassou o valor limite!",
                                                                  his_campanha=campaign,
                                                                  his_data=measurements[0].date_time,
                                                                  his_codigo=0,
                                                                  his_disabled=alert.alr_disabled)
                                alert_history.save()
                                try:
                                    if alert.alr_disabled is False:
                                        devices_campaign = GCMDevice.objects.filter(user=campaign.lcl_id.lcl_user)
                                        devices_campaign.send_message(
                                        "A concentracao de " + par.par_nome_completo + " ultrapassou o valor limite!")
                                except Exception as e:
                                    print(str(e))
                        else:
                            alert_history = Historico_Alertas(his_alerta=
                                                              "A concentracao de " + par.par_nome_completo + " ultrapassou o valor limite!",
                                                              his_campanha="Nenhuma",
                                                              his_data=measurements[0].date_time,
                                                              his_codigo=0,
                                                                  his_disabled=alert.alr_disabled)
                            alert_history.save()



post_save.connect(on_data_save, sender=Dados)

""" Unused Atmis database Models """


class Alarmes(models.Model):
    class Meta:
        verbose_name_plural = "Alarmes"

    alr_id = models.AutoField(primary_key=True)
    can_id = models.ForeignKey("Canal", on_delete=models.CASCADE)
    alr_nome = models.CharField(max_length=50)
    alr_enable = models.NullBooleanField(null=True)
    alr_tipo = models.SmallIntegerField(null=True)
    alr_rede = models.NullBooleanField(null=True)
    alr_limite_min = models.FloatField(null=True)
    alr_limite_max = models.FloatField(null=True)
    alr_estado = models.IntegerField(null=True)
    alr_intervalo_validade = models.SmallIntegerField(null=True)
    alr_log_only = models.NullBooleanField(null=True)
    est_id = models.IntegerField(null=True)

    def __str__(self):
        return self.alr_nome


class AlarmesOperadores(models.Model):
    class Meta:
        verbose_name_plural = "Alarmes Operadores"

    alr_id = models.ForeignKey("Alarmes", on_delete=models.CASCADE)
    ope_id = models.ForeignKey("Operadores", on_delete=models.CASCADE)
    alr_prioridade = models.SmallIntegerField(null=True)


class Alertas(models.Model):
    class Meta:
        verbose_name_plural = "Alertas"

    ale_id = models.AutoField(primary_key=True)
    can_id = models.ForeignKey("Canal", on_delete=models.CASCADE)
    ale_limite = models.FloatField(null=True)
    ale_enable = models.NullBooleanField(null=True)
    ale_mensagem = models.CharField(max_length=50, null=True)
    ale_intervale_validade = models.SmallIntegerField(null=True)
    ale_tipo_media = models.IntegerField(null=True)
    ale_log_only = models.NullBooleanField(null=True)


class AlertasOperadores(models.Model):
    class Meta:
        verbose_name_plural = "Alertas Operadores"

    ale_id = models.ForeignKey("Alertas", on_delete=models.CASCADE)
    ope_id = models.ForeignKey("Operadores", on_delete=models.CASCADE)


class Area(models.Model):
    class Meta:
        verbose_name_plural = "Areas"

    are_id = models.AutoField(primary_key=True)
    are_nome = models.CharField(max_length=50, null=True)
    are_url = models.CharField(max_length=255, null=True)
    are_login = models.CharField(max_length=20, null=True)
    are_password = models.CharField(max_length=20, null=True)
    are_area_id = models.IntegerField(null=True)
    are_dias_semana = models.SmallIntegerField(null=True)
    are_hora_actl = models.DateTimeField(null=True)
    are_hora_calc = models.DateTimeField(null=True)
    are_perc_validacao = models.SmallIntegerField(null=True)
    are_data_indentr = models.DateTimeField(null=True)
    are_data_dadentr = models.DateTimeField(null=True)
    are_tipo = models.NullBooleanField(null=True)
    are_entr_dados = models.NullBooleanField(null=True)
    are_entr_dados_val = models.NullBooleanField(null=True)
    are_entr_indices = models.NullBooleanField(null=True)
    are_entr_ciclica = models.NullBooleanField(null=True)
    are_entr_hora = models.DateTimeField(null=True)
    are_entr_intervalo = models.IntegerField(null=True)

    def __str__(self):
        return self.are_nome


class AreaEstacao(models.Model):
    class Meta:
        verbose_name_plural = "Area Estacoes"

    are_id = models.ForeignKey("Area", on_delete=models.CASCADE)
    est_id = models.ForeignKey("Estacao", on_delete=models.CASCADE)


class Campanha(models.Model):
    class Meta:
        verbose_name_plural = "Campanhas"

    cam_id = models.AutoField(primary_key=True)
    est_id = models.ForeignKey("Estacao", on_delete=models.CASCADE)
    cam_nome = models.CharField(max_length=50, null=True)
    cam_local = models.CharField(max_length=50, null=True)
    cam_coord_lat = models.FloatField(null=True)
    cam_coord_long = models.FloatField(null=True)
    cam_coord_alt = models.IntegerField(null=True)
    cam_data_inicio = models.DateTimeField(null=True)
    cam_data_fim = models.DateTimeField(null=True)
    cam_foto1 = models.ImageField(null=True)
    cam_foto1_cx = models.IntegerField(null=True)
    cam_foto1_cy = models.IntegerField(null=True)
    cam_foto2 = models.ImageField(null=True)
    cam_foto2_cx = models.IntegerField(null=True)
    cam_foto2_cy = models.IntegerField(null=True)
    cam_projecto = models.CharField(max_length=50, null=True)
    cam_observacoes = models.CharField(max_length=50, null=True)

    def __str__(self):
        return self.cam_nome


class Categoria(models.Model):
    class Meta:
        verbose_name_plural = "Categorias"

    cat_id = models.AutoField(primary_key=True)
    cat_nome = models.CharField(max_length=10, null=True)

    def __str__(self):
        return self.cat_nome


class Caudal(models.Model):
    class Meta:
        verbose_name_plural = "Caudais"

    cdl_id = models.AutoField(primary_key=True)
    can_id = models.ForeignKey("Canal", on_delete=models.CASCADE)
    cdl_nivel = models.FloatField(null=True)
    cdl_caudal = models.FloatField(null=True)


class Config(models.Model):
    class Meta:
        verbose_name_plural = "Configs"

    cfg_nome = models.CharField(max_length=50, primary_key=True)
    cfg_valor = models.CharField(max_length=100, null=True)

    def __str__(self):
        return self.cfg_nome


class DadosCaudal(models.Model):
    class Meta:
        verbose_name_plural = "Modelos"

    dc_id = models.AutoField(primary_key=True)
    dad_id = models.ForeignKey("Dados", on_delete=models.CASCADE)
    dc_canal = models.SmallIntegerField
    dc_haste = models.TextField
    dc_distancias = models.TextField
    dc_alturas = models.TextField
    dc_velocidades = models.TextField


class DadosOriginais(models.Model):
    class Meta:
        verbose_name_plural = "Dados Originais"

    do_id = models.AutoField(primary_key=True)
    est_id = models.ForeignKey("Estacao", on_delete=models.CASCADE)
    do_data = models.DateTimeField(null=True)
    do_canal = models.SmallIntegerField(null=True)
    do_valor = models.FloatField(null=True)
    do_estado = models.SmallIntegerField(null=True)


class Entrega(models.Model):
    class Meta:
        verbose_name_plural = "Entregas"

    ent_id = models.AutoField(primary_key=True)
    are_id = models.ForeignKey("Area", on_delete=models.CASCADE)
    ent_hora = models.SmallIntegerField(null=True)
    ent_dias_semana = models.SmallIntegerField(null=True)


class Eventos(models.Model):
    class Meta:
        verbose_name_plural = "Eventos"

    evt_id = models.AutoField(primary_key=True)
    est_id = models.ForeignKey("Estacao", on_delete=models.CASCADE)
    evt_canal = models.SmallIntegerField(null=True)
    evt_data = models.DateTimeField(null=True)
    evt_val = models.FloatField(null=True)
    evt_stat = models.SmallIntegerField(null=True)


class Indice(models.Model):
    class Meta:
        verbose_name_plural = "Indices"

    ind_id = models.AutoField(primary_key=True)
    are_id = models.ForeignKey("Area", on_delete=models.CASCADE)
    ind_data = models.DateTimeField(null=True)
    ind_indice = models.SmallIntegerField(null=True)
    ind_co = models.SmallIntegerField(null=True)
    ind_co_val = models.FloatField(null=True)
    ind_no2 = models.SmallIntegerField(null=True)
    ind_no2_val = models.FloatField(null=True)
    ind_o3 = models.SmallIntegerField(null=True)
    ind_o3_val = models.FloatField(null=True)
    ind_pm10 = models.SmallIntegerField(null=True)
    ind_pm10_val = models.FloatField(null=True)
    ind_s02 = models.SmallIntegerField(null=True)
    ind_s02_val = models.FloatField(null=True)
    ind_val = models.FloatField(null=True)
    ind_poluente = models.SmallIntegerField(null=True)


class Invalidacao(models.Model):
    class Meta:
        verbose_name_plural = "Invalidacoes"

    inv_id = models.AutoField(primary_key=True)
    est_id = models.ForeignKey("Estacao", on_delete=models.CASCADE)
    ope_id = models.ForeignKey("Operadores", on_delete=models.CASCADE)
    inv_data = models.SmallIntegerField(null=True)
    inv_canal = models.IntegerField(null=True)
    inv_razao = models.IntegerField(null=True)
    inv_intervalo_inicio = models.DateTimeField(null=True)
    inv_intervalo_fim = models.DateTimeField(null=True)
    inv_obs = models.CharField(max_length=100, null=True)


class Limites(models.Model):
    class Meta:
        verbose_name_plural = "Limites"

    lim_id = models.AutoField(primary_key=True)
    par_id = models.ForeignKey("Parametro", on_delete=models.CASCADE)
    lim_ano = models.SmallIntegerField(null=True)
    lim_mau_min = models.FloatField(null=True)
    lim_fraco_min = models.FloatField(null=True)
    lim_faco_max = models.FloatField(null=True)
    lim_medio_min = models.FloatField(null=True)
    lim_medio_max = models.FloatField(null=True)
    lim_bom_min = models.FloatField(null=True)
    lim_bom_max = models.FloatField(null=True)
    lim_mtobom_min = models.FloatField(null=True)
    lim_mtobom_max = models.FloatField(null=True)


class LogAlarmes(models.Model):
    class Meta:
        verbose_name_plural = "Log Alarmes"

    lalr_id = models.AutoField(primary_key=True)
    alr_id = models.ForeignKey("Alarmes", on_delete=models.CASCADE)
    ope_id = models.ForeignKey("Operadores", on_delete=models.CASCADE)
    lalr_data = models.DateTimeField(null=True)
    lalr_valor = models.FloatField(null=True)
    lalr_aceite = models.DateTimeField(null=True)
    lalr_obs = models.CharField(max_length=256, null=True)
    lalr_resolvido = models.DateTimeField(null=True)
    lalr_expirado = models.NullBooleanField(null=True)
    lalr_recebido = models.DateTimeField(null=True)


class LogAlertas(models.Model):
    class Meta:
        verbose_name_plural = "Log Alertas"

    lale_id = models.AutoField(primary_key=True)
    ale = models.ForeignKey("Alertas", on_delete=models.CASCADE)
    lale_data = models.DateTimeField(null=True)
    lale_limite_configurado = models.FloatField(null=True)
    lale_valor_encontrado = models.FloatField(null=True)


class LogMsgsRxTx(models.Model):
    class Meta:
        verbose_name_plural = "Log Msgs RxTx"

    msg_id = models.AutoField(primary_key=True)
    ope_id = models.ForeignKey("Operadores", on_delete=models.CASCADE)
    msg_data = models.DateTimeField(null=True)
    msg_tipo = models.SmallIntegerField(null=True)
    msg_mensagem = models.TextField(null=True)

    def __str__(self):
        return self.msg_mensagem


class Operadores(models.Model):
    class Meta:
        verbose_name_plural = "Operadores"

    ope_id = models.AutoField(primary_key=True)
    ope_nome = models.CharField(max_length=30, null=True)
    ope_nome_completo = models.CharField(max_length=60, null=True)
    ope_telemovel = models.CharField(max_length=30, null=True)
    ope_observacoes = models.CharField(max_length=50, null=True)
    ope_atraso = models.SmallIntegerField(null=True)
    ope_email = models.CharField(max_length=50, null=True)
    ope_dias_semana = models.SmallIntegerField(null=True)
    ope_telemovel_on = models.NullBooleanField(null=True)
    ope_email_on = models.NullBooleanField(null=True)
    ope_password = models.CharField(max_length=20, null=True)
    ope_permissoes = models.IntegerField(null=True)

    def __str__(self):
        return self.ope_nome


class Relatorio(models.Model):
    class Meta:
        verbose_name_plural = "Relatorios"

    rel_id = models.AutoField(primary_key=True)
    est_id = models.ForeignKey("Estacao", on_delete=models.CASCADE)
    rel_registo = models.SmallIntegerField(null=True)
    rel_data = models.DateTimeField(null=True)
    rel_tipo = models.SmallIntegerField(null=True)
    rel_info = models.SmallIntegerField(null=True)
    rel_dado = models.FloatField(null=True)
