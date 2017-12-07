from django.contrib import admin
from django.utils.html import format_html
from django.utils.safestring import mark_safe

from .models import Author, INEMap, Shape, Commandline, INEPadron, PadronItem


class AuthorAdmin(admin.ModelAdmin):
    list_display = ('name', 'type',)
    list_filter = ('type',)


class MapAdmin(admin.ModelAdmin):
    list_display = ('author', 'name', 'dataset_key', 'license', 'is_public', 'published')
    list_filter = ('license', 'is_public', 'published',)
    search_fields = ('name', 'author__name', 'dataset_key',)
    readonly_fields = ('image_tag',)

    def image_tag(self, obj):
        return format_html('<img src="{}" width=800 title="{}"/>'.format(obj.image.url, obj.image.url))
    image_tag.short_description = 'ImageTag'


class ShapeAdmin(admin.ModelAdmin):
    list_display = ('name', 'key', 'map',)
    search_fields = ('name', 'map__name')


class CommandlineAdmin(admin.ModelAdmin):
    list_display = ('user', 'hostname')
    list_filter = ('datetime',)


class PadronAdmin(admin.ModelAdmin):
    list_display = ('author', 'name', 'ax1', 'ax2', 'license', 'is_public', 'published')
    list_filter = ('ax1', 'ax2', 'license', 'is_public', 'published',)
    search_fields = ('name', 'author__name',)
    readonly_fields = ('inemap',)


class PadronItemAdmin(admin.ModelAdmin):
    list_display = ('name', 'ax1', 'ax2',)
    readonly_fields = ('dataframe',)

    def ax1(self, obj):
        return obj.padron.ax1

    def ax2(self, obj):
        return obj.padron.ax2

    def dataframe(self, obj):
        return mark_safe(obj.as_dataframe().to_html())


admin.site.register(Author, AuthorAdmin)
admin.site.register(INEMap, MapAdmin)
admin.site.register(Shape, ShapeAdmin)
admin.site.register(Commandline, CommandlineAdmin)
admin.site.register(INEPadron, PadronAdmin)
admin.site.register(PadronItem, PadronItemAdmin)
