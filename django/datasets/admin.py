from django.contrib import admin
from django.utils.html import format_html

from .models import Author, Map, Shape, Commandline, Padron, \
    PadronMunicipios, PadronCCAA


class AuthorAdmin(admin.ModelAdmin):
    list_display = ('name', 'type',)
    list_filter = ('type',)


class DataSetAdmin(admin.ModelAdmin):
    list_display = ('author', 'name', 'license', 'is_public', 'published')
    list_filter = ('license', 'is_public', 'published',)
    search_fields = ('name', 'author__name',)
    readonly_fields = ('image_tag',)

    def image_tag(self, obj):
        return format_html('<img src="{}" width=800 title="{}"/>'.format(obj.image.url, obj.image.url))
    image_tag.short_description = 'ImageTag'


class ShapeAdmin(admin.ModelAdmin):
    list_display = ('name', 'key',)
    search_fields = ('name', 'dataset__name')


class CommandlineAdmin(admin.ModelAdmin):
    list_display = ('user', 'hostname')
    list_filter = ('datetime',)


class PadronAdmin(admin.ModelAdmin):
    list_display = ('author', 'name', 'map_type', 'map', 'license', 'is_public', 'published')
    list_filter = ('map_type', 'license', 'is_public', 'published',)
    search_fields = ('name', 'author__name',)


class PadronItemAdmin(admin.ModelAdmin):
    list_display = ('name', 'total',)
    search_fields = ('padron__name',)


admin.site.register(Author, AuthorAdmin)
admin.site.register(Map, DataSetAdmin)
admin.site.register(Shape, ShapeAdmin)
admin.site.register(Commandline, CommandlineAdmin)
admin.site.register(Padron, PadronAdmin)
admin.site.register(PadronMunicipios, PadronItemAdmin)
admin.site.register(PadronCCAA, PadronItemAdmin)
