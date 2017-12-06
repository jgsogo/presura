# -*- coding: utf-8 -*-

from django.db import models
from django.contrib.postgres.fields import ArrayField
from django.utils.translation import gettext as _

from model_utils import Choices

from ._dataset_meta import DatasetMeta


class Padron(DatasetMeta):
    map_type = models.CharField(max_length=128)
    map = models.CharField(max_length=64, help_text=_("Matching map, must correspond to a Map::dataset_key"))

    units = models.CharField(max_length=64)
    headings = ArrayField(models.CharField(max_length=64))

    years = ArrayField(models.SmallIntegerField())

    def __str__(self):
        return "{} ({})".format(self.name, self.dataset_key)

    @property
    def creation_date(self):
        return self.published


class PadronItem(models.Model):
    padron = models.ForeignKey(Padron, on_delete=models.CASCADE)
    total = ArrayField(models.PositiveIntegerField(blank=True, null=True))

    class Meta:
        abstract = True

    def name(self):
        raise NotImplementedError

    def set_key(self, value):
        raise NotImplementedError


class PadronMunicipios(PadronItem):
    municipio = models.CharField(max_length=120, help_text=_("Usually postal code and name"))

    # Drill down
    men = ArrayField(models.PositiveIntegerField(blank=True, null=True))
    women = ArrayField(models.PositiveIntegerField(blank=True, null=True))

    def __str__(self):
        return "{} - {}".format(self.municipio, self.year)

    def name(self):
        return self.municipio

    def set_key(self, value):
        self.municipio = value


class PadronCCAA(PadronItem):
    ccaa = models.CharField(max_length=120)

    # Drill down
    # TODO: Add fields for 'Menos de 101 ', 'De 101 a 500 ',...

    def name(self):
        return self.ccaa

    def set_key(self, value):
        self.ccaa = value
