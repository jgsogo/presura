from django.contrib.gis import admin
from django.utils.html import format_html
from django.utils.safestring import mark_safe

from .models import Layer, Map, MapLayer


class LayerAdmin(admin.ModelAdmin):
    list_display = ('name', 'basemap', 'data', 'category', 'period', 'per_area_unit')
    search_fields = ('name',)


class MapAdmin(admin.ModelAdmin):
    readonly_fields = ('image_tag',)

    def image_tag(self, obj):
        return format_html('<img src="{}" width=800 title="{}"/>'.format(obj.image.url, obj.image.url))
    image_tag.short_description = 'ImageTag'


class MapLayerAdmin(admin.ModelAdmin):
    list_display = ('map', 'layer',)


admin.site.register(Layer, LayerAdmin)
admin.site.register(Map, MapAdmin)
admin.site.register(MapLayer, MapLayerAdmin)
