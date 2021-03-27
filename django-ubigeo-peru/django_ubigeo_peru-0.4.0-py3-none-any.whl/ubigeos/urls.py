from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^regiones/$', views.RegionListView.as_view(), name='list_region'),
    url(r'^provincias/$', views.ProvinciaListView.as_view(), name='list_provincia'),
    url(r'^distritos/$', views.DistritoListView.as_view(), name='list_distrito'),
    url(r'^regiones/(?P<coddpto>[0-9]{2})/$', views.RegionDetailView.as_view(), name='detail_region'),
    url(r'^provincias/(?P<idprov>[0-9]{4})/$', views.ProvinciaDetailView.as_view(), name='detail_provincia'),
    url(r'^distritos/(?P<iddist>[0-9]{6})/$', views.DistritoDetailView.as_view(), name='detail_distrito'),
    url(r'^regiones/(?P<coddpto>[0-9]{2})/provincias/$', views.RegionDetailView.as_view(), name='detail_region'),
    url(
        r'^regiones/(?P<coddpto>[0-9]{2})/provincias/(?P<idprov>[0-9]{4})/$',
        views.ProvinciaDetailView.as_view(),
        name='detail_region_provincias'
    ),
    url(
        r'^regiones/(?P<coddpto>[0-9]{2})/provincias/(?P<idprov>[0-9]{4})/distritos/$',
        views.ProvinciaDetailView.as_view(),
        name='detail_provincia_distritos'
    ),
    url(
        r'^regiones/(?P<coddpto>[0-9]{2})/provincias/(?P<idprov>[0-9]{4})/distritos/(?P<iddist>[0-9]{6})/$',
        views.DistritoDetailView.as_view(),
        name='detail_provincia_distrito'
    ),
]
