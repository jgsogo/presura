from django.contrib.gis import admin

from .models import Layer


class LayerAdmin(admin.ModelAdmin):
    list_display = ('name', 'basemap', 'data', 'category', 'period',)
    search_fields = ('name',)


admin.site.register(Layer, LayerAdmin)
