from django.contrib import admin

from .models import Resource, DownloadLog


class ResourceAdmin(admin.ModelAdmin):
    list_display = ('name', 'type', 'available',)
    list_filter = ('type', 'available',)
    search_fields = ('name',)


class DownloadLogAdmin(admin.ModelAdmin):
    list_display = ('resource', 'timestamp', 'deleted', 'loaded',)
    list_filter = ('deleted', 'timestamp')
    search_fields = ('resource__name',)

    def loaded(self, obj):
        return obj.datasets.exists()
    loaded.boolean = True


admin.site.register(Resource, ResourceAdmin)
admin.site.register(DownloadLog, DownloadLogAdmin)
