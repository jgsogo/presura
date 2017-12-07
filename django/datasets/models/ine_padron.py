# -*- coding: utf-8 -*-

from django.db import models
from django.contrib.postgres.fields import ArrayField
from django.utils.translation import gettext as _

from model_utils import Choices

from .ine_map import INEMap
from .dataset import Dataset


class INEPadron(Dataset):
    units = models.CharField(max_length=64)
    headings = ArrayField(models.CharField(max_length=64))

    # Reference data
    _inemap_dataset_key = models.CharField(max_length=64, help_text=_("Matching map, must correspond to a Map::dataset_key"))

    # Data axis
    ax1 = models.CharField(max_length=128, help_text=_("First dimension, relate to PadronItems"))

    ax2 = models.CharField(max_length=128, help_text=_("Second dimension, type of data"))
    ax2_values = ArrayField(models.CharField(max_length=120))

    # ax3 = models.CharField(max_length=128, help_text=_("Third dimension, periods"))
    periods = ArrayField(models.SmallIntegerField())

    @property
    def creation_date(self):
        return self.published

    @property
    def inemap(self):
        return INEMap.objects.get(dataset_key=self._inemap_dataset_key)

    @property
    def ax1_values(self):
        return self.padronitem_set.all().list_values('name', flat=True)


class PadronItem(models.Model):
    padron = models.ForeignKey(INEPadron, on_delete=models.CASCADE)
    name = models.CharField(max_length=120, help_text=_("Usually postal code and name"))
    values = ArrayField(models.FloatField(blank=True, null=True))

    def __str__(self):
        return self.name


"""
class PadronMunicipios(PadronItem):
    municipio = models.CharField(max_length=120, help_text=_("Usually postal code and name"))

    # Drill down
    men = ArrayField(models.PositiveIntegerField(blank=True, null=True))
    women = ArrayField(models.PositiveIntegerField(blank=True, null=True))

    def __str__(self):
        return self.municipio

    def name(self):
        return self.municipio

    def set_key(self, value):
        self.municipio = value


class PadronProvincias(PadronItem):
    provincia = models.CharField(max_length=120)

    # Drill down
    men = ArrayField(models.PositiveIntegerField(blank=True, null=True))
    women = ArrayField(models.PositiveIntegerField(blank=True, null=True))

    def __str__(self):
        return self.provincia

    def name(self):
        return self.provincia

    def set_key(self, value):
        self.provincia = value


class PadronIslas(PadronItem):
    isla = models.CharField(max_length=120)

    # Drill down
    men = ArrayField(models.PositiveIntegerField(blank=True, null=True))
    women = ArrayField(models.PositiveIntegerField(blank=True, null=True))

    def __str__(self):
        return self.isla

    def name(self):
        return self.isla

    def set_key(self, value):
        self.isla = value


class PadronCapitalProvincia(PadronItem):
    ciudad = models.CharField(max_length=120)

    # Drill down
    men = ArrayField(models.PositiveIntegerField(blank=True, null=True))
    women = ArrayField(models.PositiveIntegerField(blank=True, null=True))

    def __str__(self):
        return self.ciudad

    def name(self):
        return self.ciudad

    def set_key(self, value):
        self.ciudad = value


class PadronCCAA(PadronItem):
    ccaa = models.CharField(max_length=120)

    # Drill down
    # TODO: Add fields for 'Menos de 101 ', 'De 101 a 500 ',...

    def name(self):
        return self.ccaa

    def set_key(self, value):
        self.ccaa = value
"""
