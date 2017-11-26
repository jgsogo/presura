from django.contrib.gis import admin

from .models import Country, CCAA, Province, Municipality


admin.site.register(Country)
admin.site.register(CCAA)
admin.site.register(Province)
admin.site.register(Municipality)
