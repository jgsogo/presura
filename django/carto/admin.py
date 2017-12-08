from django.contrib.gis import admin

from .models import Layer, Map, MapLayer


class LayerAdmin(admin.ModelAdmin):
    list_display = ('name', 'basemap', 'data', 'category', 'period', 'per_area_unit')
    search_fields = ('name',)


admin.site.register(Layer, LayerAdmin)
admin.site.register(Map)
admin.site.register(MapLayer)
