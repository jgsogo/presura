# -*- coding: utf-8 -*-

from django.contrib.gis.db import models
from django.contrib.postgres.fields import ArrayField

from datasets.models.dataset import DataSet
from datasets.utils import plottable


class Shape(plottable.Shape, models.Model):
    dataset = models.ForeignKey(DataSet, on_delete=models.CASCADE)

    key = models.CharField(max_length=64)
    name = models.CharField(max_length=120)
    polygons = models.MultiPolygonField()  # Necesitamos un multipolygon para meter los condados de Treviño y similares

    rawData = ArrayField(models.CharField(max_length=120))

    def __init__(self, *args, **kwargs):
        super(Shape, self).__init__(*args, **kwargs)
        if self.polygons:
            self.shape = self.polygons
            self.srid = self.polygons.srid

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        super(Shape, self).save(*args, **kwargs)
        if self.polygons:
            self.shape = self.polygons
            self.srid = self.polygons.srid
