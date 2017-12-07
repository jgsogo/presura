# -*- coding: utf-8 -*-

import os
import logging
import itertools
from datetime import datetime
import datasets.utils.importers.px_reader as px_reader
from datasets.models import INEPadron, Author, PadronItem

log = logging.getLogger(__name__)


def _str_to_float(s):
    try:
        return float(s.strip())
    except ValueError:
        return None

def _str_to_int(s):
    try:
        return int(float(s.strip()))
    except ValueError:
        return None


def _get_modification_date(date):
    return datetime.strptime(date, '%Y%M%d')


def get_author():
    # TODO: Join with the same function for maps
    author, _ = Author.objects.get_or_create(name="INE",
                                             type=Author.TYPE.institution,
                                             url="http://www.ine.es/")
    return author


def import_pcaxis(resource_path, db_obj_associated):
    log.info("INE::import_pcaxis(resource_path='{}')".format(resource_path))
    px_obj = px_reader.Px(resource_path)

    # Padron model
    padron = INEPadron(content_object=db_obj_associated)
    padron.name = px_obj.title
    padron.author = get_author()
    padron.published = _get_modification_date(getattr(px_obj, "creation-date"))
    padron.dataset_key = os.path.basename(resource_path)

    padron.units = px_obj.units
    padron.headings = px_obj.heading
    padron._inemap_dataset_key = list(px_obj.map.values())[0]

    # Axis
    values_keys = list(px_obj.values.keys())
    values_values = list(px_obj.values.values())
    assert values_keys[2] == "Periodo", "Expected 'Periodo' at keys[2] but found '{}'".format(values_keys)
    padron.ax1 = values_keys[0]
    padron.ax2 = values_keys[1]
    padron.ax2_values = values_values[1]
    padron.periods = [_str_to_int(y) for y in values_values[2]]
    padron.save()

    # Import DATA
    ax1_values = values_values[0]
    data = px_obj._data.split(' ')
    assert len(data) == len(ax1_values) * len(padron.ax2_values) * len(padron.periods)
    it_data = iter(data)

    for it_code in ax1_values:
        item = PadronItem(padron=padron)
        item.name = it_code
        item.values = [_str_to_float(it) for it in itertools.islice(it_data, len(padron.periods)*len(padron.ax2_values))]
        item.save()
