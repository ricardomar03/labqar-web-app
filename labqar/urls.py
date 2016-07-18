from django.conf.urls import url, include
from rest_framework import routers
from rest_framework.authtoken import views as authviews

from . import views
"""
router = routers.DefaultRouter()
router.register(r'users', views.UserViewSet)
router.register(r'groups', views.GroupViewSet)
router.register(r'dados', views.DadosViewSet)
router.register(r'parametros', views.ParametrosViewSet)
router.register(r'periodos', views.PeriodoCampanhaViewSet)
"""

urlpatterns = [
    url(r'^$', views.index_actual, name='index_actual'),
    url(r'^(?P<id>[0-9]+)/$', views.index, name='index'),
    url(r'^medicoes/$', views.measurements_actual, name='detail_actual'),
    url(r'^medicoes/(?P<id>[0-9]+)/$', views.measurements, name='details'),
    url(r'^alerts/$', views.alerts_actual, name='alerts_actual'),
    url(r'^charts_24/$', views.get_data, name='charts_24'),
    url(r'^charts_campaign/$', views.get_data_campaign, name='charts_campaign'),
    url(r'^campaigns/$', views.get_campaigns, name='campaigns'),
    url(r'^overview/(?P<id>[0-9]+)/$', views.overview, name='overview'),
    url(r'^overview_24/$', views.get_overview_24, name='overview_24h'),
    url(r'^day/$', views.get_day, name='day'),
    url(r'^day/measurements/$', views.get_day_measurements, name='day_measurements'),
    url(r'^day/alerts/$', views.get_day_alerts, name='day_alerts'),

        # user auth urls
    url(r'^accounts/login/$', views.login),
    url(r'^accounts/auth/$', views.authView),
    url(r'^accounts/logout/$', views.logout),
    url(r'^accounts/loggedin/$', views.loggedIn),
    url(r'^accounts/change_user_data/$', views.changeUserData),

    #API
    url(r'^api-token-auth/', authviews.obtain_auth_token),
    url(r'^rest/login/(?P<username>[\w]+)/(?P<password>[\w]+)/$', views.rest_login),
    url(r'^rest/logout/$', views.rest_logout),
    url(r'^rest/latestupdate/(?P<id>[0-9]+)/$', views.get_latest_update),
    url(r'^rest/latestupdate/(?P<id>[0-9]+)/airindex$', views.get_air_index),
    url(r'^rest/latestupdate/(?P<id>[0-9]+)/chart/airindex/$', views.get_index_24h),
    url(r'^rest/latestupdate/(?P<id>[0-9]+)/chart/(?P<pollutant_name>[\w]+)/$', views.get_chart_24h),
    url(r'^rest/editsettings/$', views.edit_settings),
    url(r'^rest/alerts/(?P<id>[0-9]+)/$', views.get_alerts_mobile),
    url(r'^rest/savetoken/$', views.save_gcm_token),
]

"""
url(r'^', include(router.urls)),
url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
"""