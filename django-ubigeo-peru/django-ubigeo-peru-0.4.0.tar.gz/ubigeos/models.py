from django.db import models


class Region(models.Model):
    coddpto = models.CharField('Código', max_length=2, primary_key=True)
    nom_dpto = models.CharField('Región', max_length=50)
    slug = models.SlugField(max_length=150)

    class Meta:
        ordering = ('nom_dpto', )

    def __str__(self):
        return self.nom_dpto

    @property
    def provincias(self):
        return Provincia.objects.filter(dpto=self)


class Provincia(models.Model):
    dpto = models.ForeignKey(Region, verbose_name='Región', on_delete=models.DO_NOTHING)
    idprov = models.CharField('IDProv', max_length=4, primary_key=True)
    codprov = models.CharField('Código Provincia', max_length=2)
    nom_prov = models.CharField('Provincia', max_length=50)
    slug = models.SlugField(max_length=150)

    class Meta:
        ordering = ('dpto__nom_dpto', 'nom_prov')

    def __str__(self):
        return self.nom_prov

    @property
    def coddpto(self):
        return self.dpto.coddpto

    @property
    def nom_dpto(self):
        return self.dpto.nom_dpto

    @property
    def distritos(self):
        return Distrito.objects.filter(prov=self)


class Distrito(models.Model):
    prov = models.ForeignKey(Provincia, verbose_name='Provincia', on_delete=models.DO_NOTHING)
    iddist = models.CharField('IDDist', max_length=6, primary_key=True)
    coddist = models.CharField('Código Distrito', max_length=2, db_index=True)
    nom_dist = models.CharField('Distrito', max_length=50)
    slug = models.SlugField(max_length=150)

    class Meta:
        ordering = ('prov__dpto__nom_dpto', 'prov__nom_prov', 'nom_dist')

    def __str__(self):
        return self.nom_dist

    @property
    def dpto(self):
        return self.prov.dpto

    @property
    def coddpto(self):
        return self.dpto.coddpto

    @property
    def nom_dpto(self):
        return self.dpto.nom_dpto

    @property
    def codprov(self):
        return self.prov.codprov

    @property
    def nom_prov(self):
        return self.prov.nom_prov
