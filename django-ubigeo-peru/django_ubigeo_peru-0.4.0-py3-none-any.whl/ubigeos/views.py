from rest_framework import generics
from django_filters.rest_framework import DjangoFilterBackend

from .models import Region, Distrito, Provincia
from .serializers import (
    RegionSerializer, DistritoSerializer, ProvinciaSerializer, RegionDetailSerializer, DistritoDetailSerializer,
    ProvinciaDetailSerializer,
)


class RegionListView(generics.ListAPIView):
    queryset = Region.objects.all()
    serializer_class = RegionSerializer
    filter_backends = (DjangoFilterBackend, )
    filter_fields = ('coddpto', 'nom_dpto')


class ProvinciaListView(generics.ListAPIView):
    queryset = Provincia.objects.select_related('dpto').all()
    serializer_class = ProvinciaSerializer
    filter_backends = (DjangoFilterBackend, )
    filter_fields = ('dpto__coddpto', 'dpto__nom_dpto', 'idprov', 'nom_prov')


class DistritoListView(generics.ListAPIView):
    queryset = Distrito.objects.select_related('prov__dpto', 'prov').all()
    serializer_class = DistritoSerializer
    filter_backends = (DjangoFilterBackend, )
    filter_fields = ('prov__dpto__coddpto', 'prov__idprov', 'prov__nom_prov', 'iddist', 'nom_dist')


class RegionDetailView(generics.RetrieveAPIView):
    queryset = Region.objects.all()
    serializer_class = RegionDetailSerializer
    lookup_field = 'coddpto'


class ProvinciaDetailView(generics.RetrieveAPIView):
    queryset = Provincia.objects.select_related('dpto').all()
    serializer_class = ProvinciaDetailSerializer
    lookup_field = 'idprov'


class DistritoDetailView(generics.RetrieveAPIView):
    queryset = Distrito.objects.select_related('prov__dpto', 'prov').all()
    serializer_class = DistritoDetailSerializer
    lookup_field = 'iddist'
