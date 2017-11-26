from django.contrib import admin

from .models import Resource, DownloadLog


class ResourceAdmin(admin.ModelAdmin):
    list_display = ('name', 'type', 'available',)
    list_filter = ('type', 'available',)
    search_fields = ('name',)


admin.site.register(Resource, ResourceAdmin)
admin.site.register(DownloadLog)
