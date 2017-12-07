# -*- coding: utf-8 -*-

import itertools
from django.db import models
from django.contrib.postgres.fields import ArrayField
from django.utils.translation import gettext as _

import re
import pandas as pd

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

    def get(self, category, period):
        cat_idx = self.padron.ax2_values.index(category)
        period_idx = self.padron.periods.index(period)
        return self.values[period_idx + cat_idx*len(self.padron.ax2_values)]

    def as_dataframe(self):
        it_data = iter(self.values)
        all_data = []
        columns = [self.padron.ax2] + self.padron.periods
        for it1 in self.padron.ax2_values:
            all_data.append([it1] + list(itertools.islice(it_data, len(self.padron.periods))))

        df = pd.DataFrame.from_records(all_data, columns=columns)
        df.set_index(self.padron.ax2, inplace=True)
        df.index.name = None  # Remove index name
        return df

    def key_name(self):
        m = re.match(r"(\d+)\s(\w+)", self.name)
        if m:
            return m.groups()
        return None, None
