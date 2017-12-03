# -*- coding: utf-8 -*-

from django.contrib.gis.db import models
from django.contrib.postgres.fields import ArrayField

from datasets.models.dataset import DataSet


class Shape(models.Model):
    dataset = models.ForeignKey(DataSet, on_delete=models.CASCADE)

    key = models.CharField(max_length=64)
    name = models.CharField(max_length=120)
    polygons = models.MultiPolygonField()  # Necesitamos un multipolygon para meter los condados de Treviño y similares

    rawData = ArrayField(models.CharField(max_length=120))

    def __str__(self):
        return self.name

