# -*- coding: utf-8 -*-

import os
import logging
import itertools
from datetime import datetime
import datasets.utils.importers.px_reader as px_reader
from datasets.models import Padron, Author, PadronMunicipios, PadronCCAA

log = logging.getLogger(__name__)


def _str_to_int(s):
    try:
        return int(s)
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


def _import_padron(padron, px_obj, categories, PadronItemModel):
    codes = px_obj.codes[padron.map_type]
    municipios = px_obj.values[padron.map_type]
    assert len(codes) == len(municipios)

    # Get data to iterate
    data = px_obj._data.split(' ')
    assert len(data) == len(categories) * len(padron.years) * len(codes)
    it_data = iter(data)

    for it_code in municipios:
        item = PadronItemModel(padron=padron)
        item.set_key(it_code)
        for i_cat, it_cat in enumerate(categories):
            if it_cat:
                setattr(item, it_cat, [_str_to_int(it) for it in itertools.islice(it_data, len(padron.years))])
        item.save()


def import_padron_municipal(padron, px_obj):
    # Get items to iterate data
    cat_axis = list(px_obj.values.keys())[1]
    sexos = ['total', 'men', 'women']
    assert px_obj.values[cat_axis] == ['Total', 'Hombres', 'Mujeres']
    _import_padron(padron, px_obj, sexos, PadronMunicipios)


def import_padron_ccaa(padron, px_obj):
    cat_axis = list(px_obj.values.keys())[1]
    categories = ['total', ] + [None]*13
    print(px_obj.values[cat_axis])
    assert px_obj.values[cat_axis] == ['Total', 'Menos de 101 ', 'De 101 a 500 ', 'De 501 a 1.000', 'De 1.001 a 2.000 ', 'De 2.001 a 3.000 ', 'De 3.001 a 5.000 ', 'De 5.001 a 10.000 ', 'De 10.001 a 20.000 ', 'De 20.001 a 30.000 ', 'De 30.001 a 50.000 ', 'De 50.001 a 100.000 ', 'De 100.001 a 500.000 ', 'Más de 500.000 ']
    _import_padron(padron, px_obj, categories, PadronCCAA)


def import_pcaxis(resource_path, db_obj_associated):
    log.info("INE::import_pcaxis(resource_path='{}')".format(resource_path))

    px_obj = px_reader.Px(resource_path)
    padron = Padron(content_object=db_obj_associated)
    padron.name = px_obj.title
    padron.author = get_author()
    padron.published = _get_modification_date(getattr(px_obj, "creation-date"))
    padron.dataset_key = os.path.basename(resource_path)

    padron.map_type = list(px_obj.map.keys())[0]
    padron.map = list(px_obj.map.values())[0]
    padron.units = px_obj.units
    padron.headings = px_obj.heading
    padron.years = [int(y) for y in px_obj.values["Periodo"]]
    padron.save()

    if padron.map_type == "Municipios":
        import_padron_municipal(padron, px_obj)
    elif padron.map_type == "Comunidades y Ciudades Autónomas":
        import_padron_ccaa(padron, px_obj)
    else:
        log.error("Map_type '{}' not handled".format(padron.map_type))
