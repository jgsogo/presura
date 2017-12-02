from django.contrib.gis import admin

from .models import Country, CCAA, Province, Municipality


class MunicipalityAdmin(admin.ModelAdmin):
    list_display = ('name', 'province', 'ccaa', 'dataset',)
    search_fields = ('name',)


admin.site.register(Country)
admin.site.register(CCAA)
admin.site.register(Province)
admin.site.register(Municipality, MunicipalityAdmin)
