import datetime

import collections
import pytz
from dateutil import relativedelta

from .models import *


class Pollutant:
    def __init__(self, value, stat, name, unit):
        self.value = value
        self.stat = stat
        self.name = name
        self.unit = unit

    def __add__(self, other):
        value = self.value + other.value
        stat = self.value
        name = self.value
        unit = self.value
        return Pollutant(value, stat, name, unit)

class Measurement:
    def __init__(self, date_time, values):
        self.date_time = date_time
        self.values = values


class MappedMeasurement:
    def __init__(self, date_time, values):
        self.date_time = date_time
        self.values = values


class Period:
    def __init__(self, id, start_date, end_date):
        self.id = id
        self.start_date = start_date
        self.end_date = end_date


def get_alerts(user):
    try:
        if user.is_staff:
            alerts = Historico_Alertas.objects.all()
        else:
            locations = Local.objects.filter(lcl_user=user.id).values_list('pk', flat=True)
            campaigns = Periodo_Campanha.objects.filter(lcl_id__in=locations).order_by('-cam_data_final')
            serialized_campaigns = []
            for campaign in campaigns:
                serialized_campaigns.append(str(campaign))
            alerts = Historico_Alertas.objects.filter(his_campanha__in=serialized_campaigns).filter(his_codigo=0).filter(his_disabled=False)
        return alerts
    except:
        return None


def get_campaigns(user):
    try:
        if user.is_staff:
            campaigns = Periodo_Campanha.objects.order_by('-cam_data_final')[:5]
        else:
            locations = Local.objects.filter(lcl_user=user.id).values_list('pk', flat=True)
            campaigns = Periodo_Campanha.objects.filter(lcl_id__in=locations).order_by('-cam_data_final')[:5]
        return campaigns
    except:
        return None


def get_background(campaign):
    try:
        campaign_id = campaign.lcl_id.pk

        image = Local.objects.get(pk=campaign_id)
        image = image.lcl_background
    except:
        image = None
    return image


def get_campaign_data(pollutant, campaign):
    try:
        start_date = campaign.cam_data_inicio
        end_date = campaign.cam_data_final

        data_raw = Dados.objects.filter(dad_data__range=[start_date, end_date]).order_by('dad_data').filter(
            dad_data__minute=0).latest('dad_data')
        data_raw = Dados.objects.filter(dad_data__range=[start_date + datetime.timedelta(days=1), end_date]).filter(dad_data__hour=data_raw.dad_data.hour).filter(
            dad_data__minute=0).order_by('dad_data')
        # measurements = data_to_pollutants(data_raw, campaign.cam_pm10)
        data_temp = []

        for measurement in data_raw:
            value = get_day_average(pollutant, measurement)
            # value = measurement.values[pollutant].value
            date = measurement.dad_data.isoformat().split("+")[0]  # Removes timezone
            date = date.split("T")[0] + " " + date.split("T")[1]  # Removes T between date and time
            date = date.split(":")[0] + ":" + date.split(":")[1]  # Removes Seconds
            data_temp.append([date, value])

        #data = divide_by_days(data_temp)

        return data_temp[::-1]
    except:
        return None


def get_latest_data():
    try:
        last_entry = Dados.objects.filter(dad_data__minute=0).latest('dad_data')
        #last_measurement = data_to_pollutants([last_entry], 1)

        start_date = last_entry.dad_data
        end_date = last_entry.dad_data + datetime.timedelta(minutes=45)

        update_hour_raw = Dados.objects.filter(dad_data__range=[start_date, end_date]).order_by('dad_data')
        measurements = data_to_pollutants(update_hour_raw, 1)
        last_measurement = measurements[0]

        for entry in measurements[1:]:
            for key, value in last_measurement.values.items():
                last_measurement.values[key].value += entry.values[key].value

        for key, value in last_measurement.values.items():
            if key == 'Prec':
                last_measurement.values[key].value = round(last_measurement.values[key].value, 2)
            else:
                last_measurement.values[key].value = round(last_measurement.values[key].value / len(measurements), 2)

        return last_measurement
    except:
        return None


def get_day_data(user, date):
    try:
        campaigns = get_campaigns(user)
        utc = pytz.utc
        date_time = utc.localize(datetime.datetime.strptime(date, '%Y-%m-%d'))
        not_in_campaign = True
        for campaign in campaigns:
            if campaign.cam_data_inicio <= date_time <= campaign.cam_data_final:
                not_in_campaign = False
                selected_campaign = campaign
        if not_in_campaign:
                date_time = date_time.replace(hour=23)
        else:
            date_time = date_time.replace(hour=selected_campaign.cam_data_final.hour)

        day_entry = Dados.objects.filter(dad_data__range=[date_time - datetime.timedelta(days=1), date_time]).filter(
            dad_data__minute=0).latest('dad_data')
        last_day_measurement = data_to_pollutants([day_entry], 1)
        return last_day_measurement[0]
    except:
        return None


def get_latest_data_in_campaign(campaign):
    start_date = campaign.cam_data_inicio
    end_date = campaign.cam_data_final

    try:
        last_entry = Dados.objects.filter(dad_data__range=[start_date, end_date]).filter(dad_data__minute=0).latest('dad_data')

        if last_entry is not None:
            #last_measurement = data_to_pollutants([last_entry], campaign.cam_pm10)
            #update = last_measurement[0]

            start_date = last_entry.dad_data
            end_date = last_entry.dad_data + datetime.timedelta(minutes=45)

            update_hour_raw = Dados.objects.filter(dad_data__range=[start_date, end_date]).order_by('dad_data')
            measurements = data_to_pollutants(update_hour_raw, campaign.cam_pm10)
            last_measurement = measurements[0]

            for entry in measurements[1:]:
                for key, value in last_measurement.values.items():
                    last_measurement.values[key].value += entry.values[key].value

            for key, value in last_measurement.values.items():
                if key == 'Prec':
                    last_measurement.values[key].value = round(last_measurement.values[key].value, 2)
                else:
                    last_measurement.values[key].value = round(last_measurement.values[key].value / len(measurements),2)

    except:
        last_measurement = None
    return last_measurement


def get_last_24h(pollutant, date, campaign_id):
    try:
        if campaign_id != -1:
            campaign = Periodo_Campanha.objects.get(pk=campaign_id)
            pm10_factor = campaign.cam_pm10
        else:
            pm10_factor = 1

        if date is not None:
            update = Dados.objects.filter(dad_data__range=[date - datetime.timedelta(days=1), date]).latest('dad_data')

            start_date = update.dad_data - datetime.timedelta(hours=24)
            end_date = update.dad_data + datetime.timedelta(minutes=45)

            update_24h_raw = Dados.objects.filter(dad_data__range=[start_date, end_date]).order_by('dad_data')

            measurements = data_to_pollutants(update_24h_raw, pm10_factor)

            update_24h_temp = []

            for measurement in measurements:
                value = measurement.values[pollutant].value
                update_24h_temp.append([measurement.date_time, value]);

            if pollutant == "Prec":
                update_24h = divide_by_hours_sum(update_24h_temp)[::-1]
            else:
                update_24h = divide_by_hours(update_24h_temp)[::-1]

            update_24h = update_24h
    except:
        update_24h = None

    return update_24h


def get_day_average(pollutant, update):
    try:
        selected_day = Dados.objects.filter(
            dad_data__range=[update.dad_data - datetime.timedelta(hours=23, minutes=45), update.dad_data]).order_by(
            'dad_data')
        measurements = data_to_pollutants(selected_day, 1)

        sum = 0
        count = 0

        for measurement in measurements:
            sum += measurement.values[pollutant].value
            count += 1

        if count != 0:
            return sum / count
    except:
        return 0


def divide_by_hours(measurements):
    hour_average = []

    while len(measurements) > 0:
        hour_start = datetime.datetime.strptime(measurements[0][0], "%Y-%m-%d %H:%M")
        if hour_start.minute == 0:
            if len(measurements) > 1 and relativedelta.relativedelta(
                    datetime.datetime.strptime(measurements[0][0], "%Y-%m-%d %H:%M"), hour_start).minutes == 45:
                hour_average.append([measurements[1][0], (measurements[0][1] + measurements[1][1]) / 2])
                del measurements[:2]
            elif len(measurements) > 2 and relativedelta.relativedelta(
                    datetime.datetime.strptime(measurements[0][0], "%Y-%m-%d %H:%M"), hour_start).minutes == 45:
                hour_average.append(
                    [measurements[2][0], (measurements[0][1] + measurements[1][1] + measurements[2][1]) / 3])
                del measurements[:3]
            elif len(measurements) > 3 and relativedelta.relativedelta(
                    datetime.datetime.strptime(measurements[3][0], "%Y-%m-%d %H:%M"), hour_start).minutes == 45:
                hour_average.append([measurements[0][0], (
                    measurements[0][1] + measurements[1][1] + measurements[2][1] + measurements[3][1]) / 4])
                del measurements[:4]
            else:
                hour_average.append([measurements[0][0], measurements[0][1]])
                del measurements[:1]
        else:
            del measurements[0]

    return hour_average


def divide_by_hours_sum(measurements):
    hour_sum = []

    while len(measurements) > 0:
        hour_start = datetime.datetime.strptime(measurements[0][0], "%Y-%m-%d %H:%M")
        if hour_start.minute == 0:
            if len(measurements) > 1 and relativedelta.relativedelta(
                    datetime.datetime.strptime(measurements[0][0], "%Y-%m-%d %H:%M"), hour_start).minutes == 45:
                hour_sum.append([measurements[1][0], (measurements[0][1] + measurements[1][1])])
                del measurements[:2]
            elif len(measurements) > 2 and relativedelta.relativedelta(
                    datetime.datetime.strptime(measurements[0][0], "%Y-%m-%d %H:%M"), hour_start).minutes == 45:
                hour_sum.append(
                    [measurements[2][0], (measurements[0][1] + measurements[1][1] + measurements[2][1])])
                del measurements[:3]
            elif len(measurements) > 3 and relativedelta.relativedelta(
                    datetime.datetime.strptime(measurements[3][0], "%Y-%m-%d %H:%M"), hour_start).minutes == 45:
                hour_sum.append([measurements[0][0], (
                    measurements[0][1] + measurements[1][1] + measurements[2][1] + measurements[3][1])])
                del measurements[:4]
            else:
                hour_sum.append([measurements[0][0], measurements[0][1]])
                del measurements[:1]
        else:
            del measurements[0]

    return hour_sum


def co_quality_index(last_update):
    date = last_update.date_time
    utc = pytz.utc
    date = utc.localize(datetime.datetime.strptime(date, '%Y-%m-%d %H:%M'))

    if date is not None:
        start_date = date - datetime.timedelta(hours=8)
        end_date = date + datetime.timedelta(minutes=45)

        try:
            update_24h_raw = Dados.objects.filter(dad_data__range=[start_date, end_date]).order_by('dad_data')

            measurements = data_to_pollutants(update_24h_raw, 1)

            update_24h_temp = []

            for measurement in measurements:
                value = measurement.values['CO'].value
                update_24h_temp.append([measurement.date_time, value]);

            update_24h = divide_by_hours(update_24h_temp)[::-1]

            update_24h = update_24h

            count = 0
            sum = 0
            for update in update_24h:
                sum += update[1]
                count += 1

            average = sum / count
            return average
        except:
            return -1


def air_quality_index(last_update):
    co_value = last_update.values['CO'].value
    #co_value = co_quality_index(last_update)
    # co_converted = (co_value - 10) * 1.16 * 1000
    if co_value >= 10000:
        co_index = 1
    elif 8500 <= co_value <= 9999:
        co_index = 2
    elif 7000 <= co_value <= 8499:
        co_index = 3
    elif 5000 <= co_value <= 6999:
        co_index = 4
    elif 0 <= co_value <= 4999:
        co_index = 5
    else:
        co_index = 6

    so2_value = last_update.values['SO2'].value
    #so2_converted = so2_value * 2.66
    if so2_value >= 500:
        so2_index = 1
    elif 350 <= so2_value <= 499:
        so2_index = 2
    elif 210 <= so2_value <= 349:
        so2_index = 3
    elif 140 <= so2_value <= 209:
        so2_index = 4
    elif 0 <= so2_value <= 139:
        so2_index = 5
    else:
        so2_index = 6

    no2_value = last_update.values['NO2'].value
    #no2_converted = no2_value * 1.912
    if no2_value >= 400:
        no2_index = 1
    elif 200 <= no2_value <= 399:
        no2_index = 2
    elif 140 <= no2_value <= 199:
        no2_index = 3
    elif 100 <= no2_value <= 139:
        no2_index = 4
    elif 0 <= no2_value <= 99:
        no2_index = 5
    else:
        no2_index = 6

    o3_value = last_update.values['O3'].value
    #o3_converted = o3_value
    if o3_value >= 240:
        o3_index = 1
    elif 180 <= o3_value <= 239:
        o3_index = 2
    elif 120 <= o3_value <= 179:
        o3_index = 3
    elif 60 <= o3_value <= 119:
        o3_index = 4
    elif 0 <= o3_value <= 59:
        o3_index = 5
    else:
        o3_index = 6

    pm10_value = last_update.values['PM10'].value
    if pm10_value >= 120:
        pm10_index = 1
    elif 50 <= pm10_value <= 119:
        pm10_index = 2
    elif 35 <= pm10_value <= 49:
        pm10_index = 3
    elif 20 <= pm10_value <= 34:
        pm10_index = 4
    elif 0 <= pm10_value <= 19:
        pm10_index = 5
    else:
        pm10_index = 6

    index = min([co_index, so2_index, no2_index, o3_index, pm10_index])
    if index == 1:
        return [1, "red", "Mau", co_index, so2_index, no2_index, o3_index, pm10_index]
    elif index == 2:
        return [0.80, "orange", "Fraco", co_index, so2_index, no2_index, o3_index, pm10_index]
    elif index == 3:
        return [.60, "yellow", "Médio", co_index, so2_index, no2_index, o3_index, pm10_index]
    elif index == 4:
        return [.40, "darkgreen", "Bom", co_index, so2_index, no2_index, o3_index, pm10_index]
    elif index == 5:
        return [.20, "green", "Muito Bom", co_index, so2_index, no2_index, o3_index, pm10_index]
    else:
        return [0, "grey", "Nao Medido", co_index, so2_index, no2_index, o3_index, pm10_index]


def air_quality_index_24h(date, campaign_id):
    colors = []
    values = []
    worst_index_value = -1
    worst_color = ""
    worst_annotation = ""
    worst_indexes = []

    try:
        if campaign_id != -1:
            campaign = Periodo_Campanha.objects.get(pk=campaign_id)
            pm10_factor = campaign.cam_pm10
        else:
            pm10_factor = 1
    except:
        pm10_factor = 1

    if date is not None:
        try:
            update = Dados.objects.filter(dad_data__range=[date - datetime.timedelta(days=1), date]).latest('dad_data')
        except:
            return None

        start_date = update.dad_data - datetime.timedelta(hours=24)
        end_date = update.dad_data

        try:
            last_24h_raw = Dados.objects.filter(dad_data__range=[start_date, end_date]).order_by('-dad_data')
        except:
            last_24h_raw = None

        if last_24h_raw is not None:
            measurements = data_to_pollutants(last_24h_raw, pm10_factor)

            hour_start = datetime.datetime.strptime(measurements[0].date_time, "%Y-%m-%d %H:%M")

            for measurement in measurements:
                worst_annotation = ""
                values = []
                colors = []
                worst_index_value = -1

                current_hour = datetime.datetime.strptime(measurement.date_time, "%Y-%m-%d %H:%M")

                if relativedelta.relativedelta(current_hour, hour_start).minutes == 0:
                    index = air_quality_index(measurement)

                    for value in index[3:]:
                        if value == 1:
                            colors.append("#FF0000")
                            values.append(1)
                            if worst_index_value < 1:
                                worst_index_value = 1
                                worst_color = "#FF0000"
                        elif value == 2:
                            colors.append("#ffa500")
                            values.append(0.8)
                            if worst_index_value < 0.8:
                                worst_index_value = 0.8
                                worst_color = "#ffa500"
                        elif value == 3:
                            colors.append("#FFFF00")
                            values.append(0.6)
                            if worst_index_value < 0.6:
                                worst_index_value = 0.6
                                worst_color = "#FFFF00"
                        elif value == 4:
                            colors.append("#008000")
                            values.append(0.4)
                            if worst_index_value < 0.4:
                                worst_index_value = 0.4
                                worst_color = "#008000"
                        elif value == 5:
                            colors.append("#02dd02")
                            values.append(0.2)
                            if worst_index_value < 0.2:
                                worst_index_value = 0.2
                                worst_color = "#02dd02"
                        elif value == 6:
                            colors.append("#808080")
                            if worst_index_value == -1:
                                worst_index_value = 0
                                worst_color = "#808080"
                            values.append(0)

                    if values[0] == worst_index_value:
                        worst_annotation += "CO "
                    if values[1] == worst_index_value:
                        worst_annotation += "SO2 "
                    if values[2] == worst_index_value:
                        worst_annotation += "NO2 "
                    if values[3] == worst_index_value:
                        worst_annotation += "O3 "
                    if values[4] == worst_index_value:
                        worst_annotation += "PM10 "

                    worst_indexes.append(
                        [measurement.date_time, worst_index_value, 'color:' + worst_color, worst_annotation])
                    hour_start = current_hour

            return worst_indexes
    else:
        return None


def air_quality_results(index):
    index_value = index[0]
    index_color = index[1]
    index_class = index[2]

    colors = []
    values = []

    for value in index[3:]:
        if value == 1:
            colors.append("#FF0000")
            values.append(1)
        elif value == 2:
            colors.append("#ffa500")
            values.append(0.8)
        elif value == 3:
            colors.append("#FFFF00")
            values.append(0.6)
        elif value == 4:
            colors.append("#008000")
            values.append(0.4)
        elif value == 5:
            colors.append("#02dd02")
            values.append(0.2)
        elif value == 6:
            colors.append("#808080")
            values.append(0)

    index_values = [["CO", values[0], 'color:' + colors[0]],
                    ["SO2", values[1], 'color:' + colors[1]],
                    ["NO2", values[2], 'color:' + colors[2]],
                    ["O3", values[3], 'color:' + colors[3]],
                    ["PM10", values[4], 'color:' + colors[4]]]

    return (
        {'index_values': index_values, 'index_color': index_color, 'index_value': index_value,
         'index_class': index_class})


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
        pollutants = collections.OrderedDict()

        # PM10
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
        if partEnv_parameters.par_disabled is False:
            pollutants["PM10"] = partEnv

        # O3
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
        if o3_parameters.par_disabled is False:
            pollutants["O3"] = o3

        # NO2
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
        if no2_parameters.par_disabled is False:
            pollutants["NO2"] = no2

        # SO2
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
        if so2_parameters.par_disabled is False:
            pollutants["SO2"] = so2

        # CO
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
        if co_parameters.par_disabled is False:
            pollutants["CO"] = co

        # Benzeno
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
        if benzeno_parameters.par_disabled is False:
            pollutants["Benzeno"] = benzeno

        # Temp
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
        if temp_parameters.par_disabled is False:
            pollutants["TEMP"] = temp

        # Humidity
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
        if hum_parameters.par_disabled is False:
            pollutants["Hum"] = hum

        # Vel
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
        if vel_parameters.par_disabled is False:
            pollutants["Vel"] = vel

        # Dir
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
        if dir_parameters.par_disabled is False:
            pollutants["Dir"] = dir

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
        if no_parameters.par_disabled is False:
            pollutants["NO"] = no

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
        if nox_parameters.par_disabled is False:
            pollutants["NOx"] = nox

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
        if prec_parameters.par_disabled is False:
            pollutants["Prec"] = prec

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
        if tolueno_parameters.par_disabled is False:
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
        if etilbenzeno_parameters.par_disabled is False:
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
        if mpxileno_parameters.par_disabled is False:
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
        if oxileno_parameters.par_disabled is False:
            pollutants["OXileno"] = oxileno

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
        if so2offset_parameters.par_disabled is False:
            pollutants["SO2offset"] = so2offset

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
        if pressao_parameters.par_disabled is False:
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
        if rad_parameters.par_disabled is False:
            pollutants["Rad"] = rad

        date = entry.dad_data.isoformat().split("+")[0]  # Removes timezone
        date = date.split("T")[0] + " " + date.split("T")[1]  # Removes T between date and time
        date = date.split(":")[0] + ":" + date.split(":")[1]  # Removes Seconds

        measurements.append(Measurement(date, pollutants))

    return measurements
