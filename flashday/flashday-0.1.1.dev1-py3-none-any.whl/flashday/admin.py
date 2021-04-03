import inspect
import sys
from django.contrib import admin
from django.db.models import Model

from .models import Artist, Collection, Event, ExtraPicture, Product, ProductOption

admin.site.register(Artist)
admin.site.register(Collection)
admin.site.register(Event)
admin.site.register(ExtraPicture)
admin.site.register(Product)
admin.site.register(ProductOption)
