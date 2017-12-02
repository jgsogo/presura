from django.contrib import admin

from .models import Author, DataSet


class AuthorAdmin(admin.ModelAdmin):
    list_display = ('name', 'type',)
    list_filter = ('type',)


class DataSetAdmin(admin.ModelAdmin):
    list_display = ('author', 'name', 'license', 'is_public',)
    list_filter = ('license', 'is_public',)
    search_fields = ('name', 'author',)


admin.site.register(Author, AuthorAdmin)
admin.site.register(DataSet, DataSetAdmin)
