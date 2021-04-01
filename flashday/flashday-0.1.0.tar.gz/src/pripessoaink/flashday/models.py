from django.db.models import Model, CharField, ImageField, ForeignKey, CASCADE
from django.db.models.fields import *


class Event(Model):
    title = CharField(max_length=50)
    description = TextField()
    image = ImageField(upload_to='product')


class Artist(Model):
    name = CharField(max_length=50)
    description = TextField()
    instagram = CharField(max_length=50)
    telephone = CharField(max_length=10)
    picture = ImageField(upload_to='artist')


class Collection(Model):
    artist = ForeignKey(Artist, on_delete=CASCADE)


class Product(Model):
    collection = ForeignKey(Collection, on_delete=CASCADE)
    title = CharField(max_length=50)
    description = TextField()
    picture = ImageField(upload_to='product')


class ProductOption(Model):
    reference = ForeignKey(Product, on_delete=CASCADE)
    key = CharField(max_length=50),
    value = CharField(max_length=50)


class ExtraPicture(Model):
    reference = ForeignKey(Product, on_delete=CASCADE)
    image = ImageField(upload_to='product')
