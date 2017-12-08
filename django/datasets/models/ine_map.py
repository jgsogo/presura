# -*- coding: utf-8 -*-

from django.db import models
from django.contrib.postgres.fields import ArrayField

from datasets.models._plottable import PlottableCached
from datasets.utils import plottable
from .dataset import Dataset


class INEMap(PlottableCached, Dataset):
    # Data raw
    fields = ArrayField(models.CharField(max_length=20))
    key_field = models.CharField(max_length=64)
    name_field = models.CharField(max_length=64)

    key_field_name = models.CharField(max_length=64)
    name_field_name = models.CharField(max_length=64)

    def __str__(self):
        return "{} ({})".format(self.name, self.dataset_key)

    def get_title(self):
        return str(self)

    def get_shapes(self):
        for shape in self.shape_set.all():
            yield plottable.Shape(srid=shape.polygons.srid, shape=shape.polygons)
