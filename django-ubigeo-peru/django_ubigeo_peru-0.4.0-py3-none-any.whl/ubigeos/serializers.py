from rest_framework import serializers

from .models import Region, Distrito, Provincia


class RegionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Region
        exclude = []


class ProvinciaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Provincia
        exclude = []


class DistritoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Distrito
        exclude = []


class DistritoDetailSerializer(serializers.ModelSerializer):

    dpto = RegionSerializer()
    prov = ProvinciaSerializer()

    class Meta:
        model = Distrito
        fields = ('iddist', 'coddist', 'nom_dist', 'dpto', 'prov')


class ProvinciasDetailSerializer(serializers.ModelSerializer):

    distritos = DistritoSerializer(many=True)

    class Meta:
        model = Provincia
        fields = ('idprov', 'codprov', 'nom_prov', 'dpto', 'distritos')


class ProvinciaDetailSerializer(serializers.ModelSerializer):

    dpto = RegionSerializer()
    distritos = DistritoSerializer(many=True)

    class Meta:
        model = Provincia
        fields = ('idprov', 'codprov', 'nom_prov', 'dpto', 'distritos')


class RegionDetailSerializer(serializers.ModelSerializer):

    provincias = ProvinciasDetailSerializer(many=True)

    class Meta:
        model = Region
        fields = ('coddpto', 'nom_dpto', 'provincias')
