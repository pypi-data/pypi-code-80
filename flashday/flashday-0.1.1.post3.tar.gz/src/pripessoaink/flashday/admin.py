from django.contrib import admin

from .models import Artist, Collection, Event, ExtraPicture, Product, ProductOption


class ArtistAdmin(admin.ModelAdmin):
    list_display = ['_picture', 'name']

    def _picture(self, artist):
        return f'<img src="{artist.picture}" title="{artist.name}" />'


admin.site.register(ArtistAdmin)
admin.site.register(Collection)
admin.site.register(Event)
admin.site.register(ExtraPicture)
admin.site.register(Product)
admin.site.register(ProductOption)
