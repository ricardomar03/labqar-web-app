from django.contrib.auth.models import User, Group
from rest_framework import serializers

from .models import *


class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ('url', 'username', 'email', 'groups')


class GroupSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Group
        fields = ('url', 'name')


class PeriodoCampanhaSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Periodo_Campanha
        fields = ('lcl_id', 'cam_data_inicio', 'cam_data_final', 'lcl_morada')


class DadosSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Dados
        fiels = (
        'dad_id', 'dad_data', 'dad_1med', 'dad_1stat', 'dad_2med', 'dad_2stat', 'dad_3med', 'dad_3stat', 'dad_4med',
        'dad_4stat'
        , 'dad_5med', 'dad_5stat', 'dad_6med', 'dad_6stat', 'dad_7med', 'dad_7stat', 'dad_8med', 'dad_8stat',
        'dad_9med', 'dad_9stat'
        , 'dad_10med', 'dad_10stat', 'dad_11med', 'dad_11stat', 'dad_12med', 'dad_12stat', 'dad_13med', 'dad_13stat',
        'dad_14med', 'dad_14stat'
        , 'dad_15med', 'dad_15stat', 'dad_16med', 'dad_16stat', 'dad_17med', 'dad_17stat', 'dad_18med', 'dad_18stat',
        'dad_19med', 'dad_19stat'
        , 'dad_20med', 'dad_20stat')


class ParametroSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Parametro
        fields = ('par_id', 'par_nome', 'par_nome_completo')


class PollutantSerializer(serializers.Serializer):
    value = serializers.FloatField()
    stat = serializers.IntegerField()
    name = serializers.CharField()
    unit = serializers.CharField()
