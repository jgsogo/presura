# -*- coding: utf-8 -*-

import os
import logging
import configparser
import shapefile
import platform
from datetime import datetime

from django.contrib.gis.gdal import SpatialReference, CoordTransform
from django.contrib.gis.geos import Polygon, MultiPolygon

from datasets.models import Author, Map, Shape

log = logging.getLogger(__name__)

gcoord = SpatialReference(4326)  # WGS84
mycoord = SpatialReference(23030)  # Proyección UTM ED50 Huso 30 N
trans = CoordTransform(mycoord, gcoord)


def _to_str(name):
    return name if not isinstance(name, bytes) else name.decode('latin-1')


def _get_modification_date(filename):
    if platform.system() == 'Windows':
        return datetime.fromtimestamp(os.path.getmtime(filename))
    else:
        return None


def get_author():
    author, _ = Author.objects.get_or_create(name="INE",
                                             type=Author.TYPE.institution,
                                             url="http://www.ine.es/")
    return author


def import_map(map_filename, map):
    log.info("INE::import_map(map_filename='{}')".format(map_filename))
    sf = shapefile.Reader(map_filename)
    map.fields = [it[0] for it in sf.fields[1:]]
    map.save(skip_plot=True)  # Need it to be created to associate Shapes

    key_field_pos = map.fields.index(map.key_field)
    name_field_pos = map.fields.index(map.name_field)

    for shape in sf.shapeRecords():
        item = Shape()
        item.map = map
        item.key = shape.record[key_field_pos]
        item.name = _to_str(shape.record[name_field_pos])
        item.rawData = shape.record[:]

        parts = list(shape.shape.parts) + [len(shape.shape.points)]
        polygons = []
        for it in zip(parts[:-1], parts[1:]):
            polygons.append(Polygon(shape.shape.points[it[0]:it[1]]))
        item.polygons = MultiPolygon(polygons)
        item.polygons.transform(trans)
        item.save()

    return map


def import_resource(resource_path, db_obj_associated):
    log.info("INE::import_resource(resource_path='{}')".format(resource_path))

    # Try to get INI file from resource_path
    path = os.path.dirname(resource_path)
    id, _ = os.path.splitext(os.path.basename(resource_path))
    ini_file = os.path.join(path, id + ".ini")
    if not os.path.exists(ini_file):
        raise ValueError("INE importer requires a INI file. Cannot find or open '{}'".format(ini_file))

    config = configparser.ConfigParser()
    config.read(ini_file, encoding='latin-1')

    # Iterate through MAPS section
    maps = config["MAPS"]
    for it in range(1, 1 + int(maps['NumMaps'])):
        it_map = maps[str(it)].rsplit('\\', 1)[1]
        map_filename = os.path.join(path, it_map)
        map_section = config["FIELDS{}".format(str(it))]

        # Generate map
        map = Map(content_object=db_obj_associated)
        map.name = map_section["MapName"]
        map.author = get_author()
        map.key_field = map_section["KeyField"]
        map.key_field_name = map_section["KeyPField"]
        map.name_field = map_section["NameField"]
        map.name_field_name = map_section["NamePField"]
        map.published = _get_modification_date(map_filename)

        map = import_map(map_filename, map)
        map.save_plot()
        map.save()

