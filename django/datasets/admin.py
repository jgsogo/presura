from django.contrib import admin

from .models import Author, DataSet


admin.site.register(Author, DataSet)
