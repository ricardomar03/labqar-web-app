import base64

import pytz
from django.contrib.auth.decorators import login_required
import json
from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect, HttpResponse, Http404
from django.contrib import auth
from django.template.context_processors import csrf
from django.template.loader import render_to_string
from push_notifications.models import GCMDevice
from rest_framework.authentication import TokenAuthentication
from rest_framework.authtoken.models import Token
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.permissions import IsAuthenticated

from .serializers import *
from .data_interpreter import *

from Crypto.Cipher import AES

# API #
from django.http import Http404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.core import serializers


# ACCOUNT RELATED VIEWS
def login(request):
    context = {'invalid': False}
    context.update(csrf(request))
    return render(request, 'labqar/login.html', context)


def authView(request):
    username = request.POST.get('username', '')
    password = request.POST.get('password', '')
    user = auth.authenticate(username=username, password=password)

    if user is not None:
        auth.login(request, user)
        return HttpResponseRedirect('/')
    else:
        context = {'invalid': True}
        return render(request, 'labqar/login.html', context)


def loggedIn(request):
    context = {'full_name': request.user.username}
    return render(request, 'labqar/loggedin.html', context)


def logout(request):
    auth.logout(request)
    return HttpResponseRedirect('/accounts/login')


@login_required
def changeUserData(request):
    password = request.POST.get('password', '')
    username = request.POST.get('username')
    first_name = request.POST.get('name')

    if request.user.is_authenticated():
        user = request.user

    if user and first_name != None and first_name != '':
        user.first_name = first_name
        user.save()

    if user and username != None and username != '':
        user.username = username
        user.save()

    if user and password != None and password != '':
        user.set_password(password)
        auth.logout(request)
        user.save()
        return HttpResponseRedirect('/accounts/login')

    return HttpResponseRedirect('/')


# WEBSITE RELATED VIEWS
@login_required
def index_actual(request):
    if request.user.is_authenticated():

        if request.user.first_name is not None and request.user.first_name != '':
            username = request.user.first_name
        else:
            username = request.user.username

    selected_campaign = None
    campaigns = get_campaigns(request.user)

    last_update = None

    if request.user.is_superuser:
        last_update = get_latest_data()
    else:
        if campaigns:
            selected_campaign = campaigns[0]
            last_update = get_latest_data_in_campaign(selected_campaign)

    if last_update is not None:
        index = air_quality_index(last_update)
        results = air_quality_results(index)

        index_class = results['index_class']
        index_values = results['index_values']
        index_value = results['index_value']
        index_color = results['index_color']

    else:
        index_value = None
        index_color = None
        index_class = "Indisponivel"
        index_values = None

    background = get_background(selected_campaign)
    if background:
        background = request.build_absolute_uri(background.url)
    else:
        background = None
    context = {'last_update': last_update,
               'index_value': index_value,
               'index_color': index_color,
               'index': index_class,
               'index_values': index_values,
               'background': background,
               'selected_campaign': selected_campaign,
               'campaigns': campaigns,
               'username': username}
    return render(request, 'labqar/index.html', context)


@login_required
def index(request, id):
    if request.user.is_authenticated():

        if request.user.first_name is not None and request.user.first_name != '':
            username = request.user.first_name
        else:
            username = request.user.username

    try:
        selected_campaign = Periodo_Campanha.objects.get(pk=id)
    except:
        selected_campaign = None

    campaigns = get_campaigns(request.user)

    last_update = get_latest_data_in_campaign(selected_campaign)

    if last_update is not None:
        index = air_quality_index(last_update)
        results = air_quality_results(index)

        index_class = results['index_class']
        index_values = results['index_values']
        index_value = results['index_value']
        index_color = results['index_color']

    else:
        index_value = None
        index_color = None
        index_class = "Indisponivel"
        index_values = None

    background = get_background(selected_campaign)
    if background:
        background = request.build_absolute_uri(background.url)
    else:
        background = None

    context = {'last_update': last_update,
               'selected_campaign': selected_campaign,
               'campaigns': campaigns,
               'background': background,
               'index_value': index_value,
               'index_color': index_color,
               'index': index_class,
               'index_values': index_values,
               'username': username}
    return render(request, 'labqar/index.html', context)


@login_required
def measurements_actual(request):
    if request.user.is_authenticated():

        if request.user.first_name is not None and request.user.first_name != '':
            username = request.user.first_name
        else:
            username = request.user.username

    selected_campaign = None
    campaigns = get_campaigns(request.user)

    last_update = None

    if request.user.is_superuser:
        last_update = get_latest_data()
    else:
        if campaigns:
            selected_campaign = campaigns[0]
            last_update = get_latest_data_in_campaign(selected_campaign)

    if last_update is not None:
        values = last_update.values
    else:
        values = None

    background = get_background(selected_campaign)
    if background:
        background = request.build_absolute_uri(background.url)
    else:
        background = None

    context = {'last_update': last_update,
               'values': values,
               'selected_campaign': selected_campaign,
               'background': background,
               'campaigns': campaigns,
               'username': username}

    return render(request, 'labqar/measurements.html', context)


@login_required
def measurements(request, id):
    if request.user.is_authenticated():

        if request.user.first_name is not None and request.user.first_name != '':
            username = request.user.first_name
        else:
            username = request.user.username

    try:
        selected_campaign = Periodo_Campanha.objects.get(pk=id)
    except:
        selected_campaign = None

    last_update = get_latest_data_in_campaign(selected_campaign)

    values = last_update.values

    campaigns = get_campaigns(request.user)

    background = get_background(selected_campaign)
    if background:
        background = request.build_absolute_uri(background.url)
    else:
        background = None

    context = {'last_update': last_update,
               'values': values,
               'selected_campaign': selected_campaign,
               'background': background,
               'campaigns': campaigns,
               'username': username}

    return render(request, 'labqar/measurements.html', context)


@login_required
def alerts_actual(request):
    if request.user.is_authenticated():
        if request.user.first_name is not None and request.user.first_name != '':
            username = request.user.first_name
        else:
            username = request.user.username

    selected_campaign = None
    campaigns = get_campaigns(request.user)

    if campaigns:
        if request.user.is_superuser:
            selected_campaign = None
        else:
            selected_campaign = campaigns[0]

    background = get_background(selected_campaign)
    if background:
        background = request.build_absolute_uri(background.url)
    else:
        background = None

    alerts = get_alerts(request.user)

    context = {'alerts': alerts,
                'selected_campaign': selected_campaign,
               'campaigns': campaigns,
               'background': background,
               'username': username}
    return render(request, 'labqar/alerts.html', context)


@login_required
def get_data(request):
    if request.is_ajax() and request.POST and 'pollutant' in request.POST:
        pollutant = request.POST['pollutant']

    if request.is_ajax() and request.POST and 'date' in request.POST:
        date = request.POST['date']

    if date is not None:
        date_time = datetime.datetime.strptime(date, '%Y-%m-%d %H:%M')
        utc = pytz.utc
        date_time = utc.localize(date_time)
        campaigns = get_campaigns(request.user)
        selected_campaign_id = -1
        for campaign in campaigns:
            if campaign.cam_data_inicio <= date_time <= campaign.cam_data_final:
                selected_campaign_id = campaign.id

        values = get_last_24h(pollutant, date_time, selected_campaign_id)

        values_tooltips = []

        for value in values:
            value.append(str(round(value[1], 4)))
            values_tooltips.append(value)

    context = {'values': values_tooltips,}

    return HttpResponse(json.dumps(context), content_type='application/javascript')


@login_required
def get_overview_24(request):
    if request.is_ajax() and request.POST and 'date' in request.POST:
        date = request.POST['date']

    if date is not None:
        date_time = datetime.datetime.strptime(date, '%Y-%m-%d %H:%M')
        utc = pytz.utc
        date_time = utc.localize(date_time)
        campaigns = get_campaigns(request.user)
        selected_campaign_id = -1
        for campaign in campaigns:
            if campaign.cam_data_inicio <= date_time <= campaign.cam_data_final:
                selected_campaign_id = campaign.id
        values = air_quality_index_24h(date_time, selected_campaign_id)

    context = {'values': values,}

    return HttpResponse(json.dumps(context), content_type='application/javascript')


@login_required
def get_data_campaign(request):
    if request.user.is_authenticated():
        if request.user.first_name is not None and request.user.first_name != '':
            username = request.user.first_name
        else:
            username = request.user.username

    if request.is_ajax() and request.POST and 'pollutant' in request.POST and 'campaign' in request.POST:
        pollutant = request.POST['pollutant']
        campaign_id = request.POST['campaign']

    try:
        selected_campaign = Periodo_Campanha.objects.get(pk=campaign_id)
    except:
        selected_campaign = None

    values = get_campaign_data(pollutant, selected_campaign);

    context = {'values': values,
               'username': username}

    return HttpResponse(json.dumps(context), content_type='application/javascript')


@login_required
def get_day(request):
    if request.user.is_authenticated():
        if request.user.first_name is not None and request.user.first_name != '':
            username = request.user.first_name
        else:
            username = request.user.username

    day_update = None
    selected_campaign = None

    campaigns = get_campaigns(request.user)

    if request.POST and 'datepicker' in request.POST:
        date = request.POST['datepicker']
        day_update = get_day_data(request.user, date)

        if day_update is not None:

            utc = pytz.utc

            for campaign in campaigns:
                if campaign.cam_data_inicio <= utc.localize(
                        datetime.datetime.strptime(day_update.date_time, "%Y-%m-%d %H:%M")) <= campaign.cam_data_final:
                    selected_campaign = campaign

            index = air_quality_index(day_update)
            results = air_quality_results(index)

            index_class = results['index_class']
            index_values = results['index_values']
            index_value = results['index_value']
            index_color = results['index_color']

        else:
            index_value = None
            index_color = None
            index_class = "Indisponivel"
            index_values = None

    background = get_background(selected_campaign)
    if background:
        background = request.build_absolute_uri(background.url)
    else:
        background = None


    context = {'last_update': day_update,
               'background': background,
               'index_value': index_value,
               'index_color': index_color,
               'index': index_class,
               'index_values': index_values,
               'selected_campaign': selected_campaign,
               'campaigns': campaigns,
               'username': username
               }
    return render(request, 'labqar/index.html', context)


@login_required
def get_day_measurements(request):
    if request.user.is_authenticated():
        if request.user.first_name is not None and request.user.first_name != '':
            username = request.user.first_name
        else:
            username = request.user.username

    day_update = None
    selected_campaign = None

    campaigns = get_campaigns(request.user)

    if request.POST and 'datepicker' in request.POST:
        date = request.POST['datepicker']
        day_update = get_day_data(request.user, date)

    if day_update is not None:
        utc = pytz.utc

        for campaign in campaigns:
            if campaign.cam_data_inicio <= utc.localize(datetime.datetime.strptime(day_update.date_time,
                                                                                   "%Y-%m-%d %H:%M")) <= campaign.cam_data_final:
                selected_campaign = campaign
        values = day_update.values
    else:
        values = None

    background = get_background(selected_campaign)
    if background:
        background = request.build_absolute_uri(background.url)
    else:
        background = None

    context = {'last_update': day_update,
               'values': values,
               'selected_campaign': selected_campaign,
               'background': background,
               'campaigns': campaigns,
               'username': username}

    return render(request, 'labqar/measurements.html', context)

@login_required
def get_day_alerts(request):
    if request.user.is_authenticated():
        if request.user.first_name is not None and request.user.first_name != '':
            username = request.user.first_name
        else:
            username = request.user.username

    day_update = None
    selected_campaign = None

    campaigns = get_campaigns(request.user)

    if request.POST and 'datepicker' in request.POST:
        date = request.POST['datepicker']
        day_update = get_day_data(request.user, date)

    if day_update is not None:
        utc = pytz.utc

        for campaign in campaigns:
            if campaign.cam_data_inicio <= utc.localize(datetime.datetime.strptime(day_update.date_time,
                                                                                   "%Y-%m-%d %H:%M")) <= campaign.cam_data_final:
                selected_campaign = campaign
        values = day_update.values
    else:
        values = None

    background = get_background(selected_campaign)
    if background:
        background = request.build_absolute_uri(background.url)
    else:
        background = None

    context = {'last_update': day_update,
               'values': values,
               'selected_campaign': selected_campaign,
               'background': background,
               'campaigns': campaigns,
               'username': username}

    return render(request, 'labqar/alerts.html', context)

def overview(request, id):
    return render(request, 'labqar/index.html', None)


def unpad(s):
    return s[:-ord(s[len(s) - 1:])]


@api_view(['GET'])
def rest_login(request, username, password):
    key = '0425446769511161'
    enc = base64.b64decode(
        'W+zVZhDT6azNXXJjVxPXmU7WO6KhQUBSYKnXB/+6iAq2tIVXoN1LmwUfFP9OqTyJelmy9FquM72/bTVMKae96t+YWola3z/92Po5ztONCsw=')

    iv = enc[-16:]

    str2 = "".join(str(x) + " " for x in iv)
    cipher = AES.new(key, AES.MODE_CBC, iv)

    plaintext = cipher.decrypt(enc[:-16])

    user = auth.authenticate(username=username, password=password)

    if user is not None:
        try:
            token = Token.objects.get_or_create(user=user)
        except:
            return Response(status=status.HTTP_400_BAD_REQUEST)

        serialized_token = str(token).split()[1].split(">")[0]
        return Response(status=status.HTTP_200_OK,
                        data={'username': user.username, 'name': user.first_name, 'superuser': user.is_superuser,
                              'id': user.id, 'token': serialized_token})
    else:
        return Response(status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
@authentication_classes((TokenAuthentication,))
@permission_classes((IsAuthenticated,))
def rest_logout(request):
    id = request.POST.get('id')
    try:
        user = User.objects.get(pk=id)
        registration_id = request.POST.get('registration_id')

        device = GCMDevice.objects.get(user=user, registration_id=registration_id)
        device.active = False
        device.save()
        return Response(status=status.HTTP_200_OK)
    except:
        return Response(status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
@authentication_classes((TokenAuthentication,))
@permission_classes((IsAuthenticated,))
def get_alerts_mobile(request,id):
    try:
        user = User.objects.get(pk=id)
        alerts = get_alerts(user)

        serialized_alerts = []

        for alert in alerts[:24]:
            serialized_alerts.append([alert.his_alerta, alert.his_campanha, alert.his_data, alert.his_codigo])

        return Response(status=status.HTTP_200_OK, data={'alerts':serialized_alerts})
    except:
        return Response(status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@authentication_classes((TokenAuthentication,))
@permission_classes((IsAuthenticated,))
def save_gcm_token(request):
    id = request.POST.get('id')
    try:
        user = User.objects.get(pk=id)
        registration_id = request.POST.get('registration_id')

        repeated = False
        new = False
        if user is not None and registration_id is not None:
            devices = GCMDevice.objects.filter(user=user)

            if not devices:
                new = True
                device = GCMDevice(user=user, registration_id=registration_id)
                device.save()
            else:
                new_device = True
                repeated = True
                for device in devices:
                    if device.registration_id == registration_id:
                        new_device = False
                        device.active = True
                        device.save()

                if new_device:
                    device = GCMDevice(user=user, registration_id=registration_id)
                    device.save()

            return Response(status=status.HTTP_200_OK)
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)
    except:
        return Response(status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
@authentication_classes((TokenAuthentication,))
@permission_classes((IsAuthenticated,))
def get_latest_update(request, id):
    try:
        user = User.objects.get(pk=id)
        campaign = None
    except:
        return Response(status=status.HTTP_400_BAD_REQUEST)

    if user.is_superuser:
        last_update = get_latest_data()
    else:
        campaigns = get_campaigns(user)
        campaign = campaigns[0]
        last_update = get_latest_data_in_campaign(campaign)

    if last_update is not None:
        date_time = last_update.date_time
        values = last_update.values

        serialized_values = collections.OrderedDict()
        for key in values:
            pollutant = PollutantSerializer(values[key])
            serialized_values[key] = pollutant.data

        if campaign is not None:

            date_start = campaign.cam_data_inicio.isoformat().split("+")[0]  # Removes timezone
            date_start = date_start.split("T")[0] + " " + date_start.split("T")[1]  # Removes T between date and time
            date_start = date_start.split(":")[0] + ":" + date_start.split(":")[1]  # Removes Seconds

            date_end = campaign.cam_data_final.isoformat().split("+")[0]  # Removes timezone
            date_end = date_end.split("T")[0] + " " + date_end.split("T")[1]  # Removes T between date and time
            date_end = date_end.split(":")[0] + ":" + date_end.split(":")[1]  # Removes Seconds

            serialized_campaign = "Campanha de " + date_start + " a " + date_end
        else:
            serialized_campaign = "current"

        return Response(status=status.HTTP_200_OK,
                        data={'date_time': date_time, 'values': serialized_values, 'campaign': serialized_campaign})
    else:
        return Response(status=status.HTTP_204_NO_CONTENT)


@api_view(['GET'])
@authentication_classes((TokenAuthentication,))
@permission_classes((IsAuthenticated,))
def get_air_index(request, id):
    try:
        user = User.objects.get(pk=id)
        campaign = None
    except:
        return Response(status=status.HTTP_400_BAD_REQUEST)
    if user.is_superuser:
        last_update = get_latest_data()
    else:
        campaigns = get_campaigns(request.user)
        campaign = campaigns[0]
        last_update = get_latest_data_in_campaign(campaign)

    if last_update is not None:
        date_time = last_update.date_time
        index = air_quality_index(last_update)

        if campaign is not None:

            date_start = campaign.cam_data_inicio.isoformat().split("+")[0]  # Removes timezone
            date_start = date_start.split("T")[0] + " " + date_start.split("T")[1]  # Removes T between date and time
            date_start = date_start.split(":")[0] + ":" + date_start.split(":")[1]  # Removes Seconds

            date_end = campaign.cam_data_final.isoformat().split("+")[0]  # Removes timezone
            date_end = date_end.split("T")[0] + " " + date_end.split("T")[1]  # Removes T between date and time
            date_end = date_end.split(":")[0] + ":" + date_end.split(":")[1]  # Removes Seconds

            serialized_campaign = "Campanha de " + date_start + " a " + date_end
        else:
            serialized_campaign = "current"

        return Response(status=status.HTTP_200_OK,
                        data={'date_time': date_time, 'index': index, 'campaign': serialized_campaign})
    else:
        return Response(status=status.HTTP_204_NO_CONTENT)


@api_view(['GET'])
@authentication_classes((TokenAuthentication,))
@permission_classes((IsAuthenticated,))
def get_index_24h(request, id):
    try:
        user = User.objects.get(pk=id)
    except:
        return Response(status=status.HTTP_400_BAD_REQUEST)
    utc = pytz.utc
    if user.is_superuser:
        last_update = get_latest_data()
        date = utc.localize(
            datetime.datetime.strptime(last_update.date_time, "%Y-%m-%d %H:%M"))
        index_chart = air_quality_index_24h(date,-1)
    else:
        campaigns = get_campaigns(user)
        campaign = campaigns[0]
        last_update = get_latest_data_in_campaign(campaign)
        date = utc.localize(
            datetime.datetime.strptime(last_update.date_time, "%Y-%m-%d %H:%M"))
        index_chart = air_quality_index_24h(date, campaign.id)

    if index_chart is not None:
        return Response(status=status.HTTP_200_OK,
                        data={'index_chart': index_chart[::-1]})
    else:
        return Response(status=status.HTTP_204_NO_CONTENT)


@api_view(['GET'])
@authentication_classes((TokenAuthentication,))
@permission_classes((IsAuthenticated,))
def get_chart_24h(request, id, pollutant_name):
    try:
        user = User.objects.get(pk=id)
    except:
        return Response(status=status.HTTP_400_BAD_REQUEST)

    if user.is_superuser:
        last_update = get_latest_data()
    else:
        campaigns = get_campaigns(user)
        campaign = campaigns[0]
        last_update = get_latest_data_in_campaign(campaign)

    if last_update is not None:
        utc = pytz.utc
        date = utc.localize(
            datetime.datetime.strptime(last_update.date_time, "%Y-%m-%d %H:%M"))
        if user.is_superuser:
            values = get_last_24h(pollutant_name,date, -1)
        else:
            campaigns = get_campaigns(request.user)
            values = get_last_24h(pollutant_name,date, campaigns[0].id)

        if values is not None:
            return Response(status=status.HTTP_200_OK, data={'value': values[::-1]})

    return Response(status=status.HTTP_204_NO_CONTENT)


@api_view(['POST'])
@authentication_classes((TokenAuthentication,))
@permission_classes((IsAuthenticated,))
def edit_settings(request):
    id = request.POST.get('id')
    password = request.POST.get('password', '')
    username = request.POST.get('username', '')
    first_name = request.POST.get('name', '')

    name_changed = False
    username_changed = False
    password_changed = False

    try:
        user = User.objects.get(pk=id)
    except:
        return Response(status=status.HTTP_400_BAD_REQUEST)

    if user and first_name is not None and first_name != '':
        user.first_name = first_name
        user.save()
        name_changed = True

    if user and username is not None and username != '':
        user.username = username
        user.save()
        username_changed = True

    if user and password is not None and password != '':
        user.set_password(password)
        auth.logout(request)
        user.save()
        password_changed = True

    return Response(status=status.HTTP_200_OK,
                    data={"name_changed": name_changed, "name": user.first_name, "username_changed": username_changed,
                          "username": user.username, "password_changed": password_changed})
