from django.contrib import admin
from django.utils.html import format_html

from .models import Author, DataSet


class AuthorAdmin(admin.ModelAdmin):
    list_display = ('name', 'type',)
    list_filter = ('type',)


class DataSetAdmin(admin.ModelAdmin):
    list_display = ('author', 'name', 'license', 'is_public',)
    list_filter = ('license', 'is_public',)
    search_fields = ('name', 'author',)
    readonly_fields = ('image_tag',)

    def image_tag(self, obj):
        return format_html('<img src="{}" width=800 title="{}"/>'.format(obj.image.url, obj.image.url))
    image_tag.short_description = 'ImageTag'


admin.site.register(Author, AuthorAdmin)
admin.site.register(DataSet, DataSetAdmin)
