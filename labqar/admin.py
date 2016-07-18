from django.contrib import admin
from django.contrib.auth.models import Group
from django.forms import ModelForm, forms

from .models import *

class PeriodoForm(ModelForm):
    class Meta:
        model = Periodo_Campanha
        fields = ['lcl_id', 'cam_data_inicio', 'cam_data_final', 'cam_notas', 'cam_pm10']

    def clean(self):
        start_date = self.cleaned_data.get('cam_data_inicio')
        end_date = self.cleaned_data.get('cam_data_final')
        if start_date > end_date:
                raise forms.ValidationError("A data de inicio nao pode ser superior a de fim.")
        return self.cleaned_data


class PeriodoAdmin(admin.ModelAdmin):
    form = PeriodoForm


class ParametroAdmin(admin.ModelAdmin):
    def has_add_permission(self, request):
        return False

    def get_actions(self, request):
        # Disable delete
        actions = super(ParametroAdmin, self).get_actions(request)
        del actions['delete_selected']
        return actions

    def has_delete_permission(self, request, obj=None):
        # Disable delete
        return False

#admin.site.register(Canal)
admin.site.register(Dados)
#admin.site.register(Estacao)
#admin.site.register(Estado)
#admin.site.register(EstadoInterno)
#admin.site.register(Mapa)
#admin.site.register(Parametro)
#admin.site.register(Recolha)
#admin.site.register(Rede)
#admin.site.register(Unidade)

admin.site.register(Local)
admin.site.register(Periodo_Campanha, PeriodoAdmin)
admin.site.register(Alertas_Concentracao)
admin.site.register(Parametro_Local, ParametroAdmin)
admin.site.register(Historico_Alertas)

admin.site.unregister(Group)

""" Empty tables on the Labqar local database """
#admin.site.register(Alarmes)
#admin.site.register(AlarmesOperadores)
#admin.site.register(Alertas)
#admin.site.register(AlertasOperadores)
#admin.site.register(Area)
#admin.site.register(AreaEstacao)
#admin.site.register(Campanha)
#admin.site.register(Categoria)
#admin.site.register(Caudal)
#admin.site.register(Config)
#admin.site.register(DadosCaudal)
#admin.site.register(DadosOriginais)
#admin.site.register(Entrega)
#admin.site.register(Eventos)
#admin.site.register(Indice)
#admin.site.register(Invalidacao)
#admin.site.register(Limites)
#admin.site.register(LogAlarmes)
#admin.site.register(LogAlertas)
#admin.site.register(LogMsgsRxTx)
#admin.site.register(Operadores)
#admin.site.register(Relatorio)