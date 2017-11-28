# -*- coding: utf-8 -*-

import re
import os
import shapefile
import logging
from collections import defaultdict
from .base import BaseImporter, ShapefileImporter
from carto.models import Municipality

log = logging.getLogger(__name__)


class CCAA00Importer(ShapefileImporter):
    pattern = re.compile(r"ccaa00c\d{2}.shp")
    model = Municipality
    fields = [('OBJECTID_1', None),
              ('AREA', 'area'),
              ('PERIMETER', 'perimeter'),
              ('E20000_12', None),
              ('E20000_ID_', None),
              ('MUNICIPIO0', 'name'),
              ('SHAPE_LE_1', None),
              ('Shape_Leng', None),
              ('Shape_Area', None),
              ('PROVMUN', None),]


class CCAA0103Importer(ShapefileImporter):
    pattern = re.compile(r"ccaa0103c\d{2}.shp")
    model = Municipality
    fields = [('OBJECTID', None),
              ('AREA', None),
              ('PERIMETER', None),
              ('E20003_', None),
              ('E20003_ID', None),
              ('NOMBRE03', None),
              ('PROV', None),
              ('MUN', None),
              ('Shape_Leng', None),
              ('Shape_Area', None),
              ('PROVMUN', None),]


class COM99Importer(ShapefileImporter):
    pattern = re.compile(r"com99p\d{2}.shp")
    model = Municipality
    fields = [('OBJECTID', None),
              ('COMAGR', None),
              ('COMARCA99', None),
              ('Shape_Leng', None),
              ('Shape_Area', None),]


class CCAA99Importer(ShapefileImporter):
    pattern = re.compile(r"ccaa99c\d{2}.shp")
    model = Municipality
    fields = [('OBJECTID', None),
              ('AREA', None),
              ('PERIMETER', None),
              ('E20099_', None),
              ('E20099_ID', None),
              ('NOMBRE99', None),
              ('Shape_Leng', None),
              ('Shape_Area', None),
              ('PROVMUN', None),
              ('COM', None),]


class PROV00Importer(ShapefileImporter):
    pattern = re.compile(r"prov00p\d{2}.shp")
    model = Municipality
    fields = [('OBJECTID_1', None),
              ('AREA', None),
              ('PERIMETER', None),
              ('E20000_12', None),
              ('E20000_ID_', None),
              ('MUNICIPIO0', None),
              ('SHAPE_LE_1', None),
              ('Shape_Leng', None),
              ('Shape_Area', None),
              ('PROVMUN', None),]


class MapasMunicipales(BaseImporter):
    id = 'mapas_municipales'
    file_importers = [CCAA00Importer, CCAA0103Importer, CCAA99Importer, COM99Importer,
                      PROV00Importer,]

    allit = defaultdict(list)

    def get_shapefile_importer(self, filename):
        basename = os.path.basename(filename)

        for file_importer in self.file_importers:
            if file_importer.pattern.match(basename):
                return file_importer(filename)

        # TODO: Remove code below (until raise)
        sf = shapefile.Reader(filename)
        fields = ', '.join([it[0] for it in sf.fields])
        self.allit[fields].append(filename)

        from pprint import pprint
        for it,v in self.allit.items():
            print(it)
            pprint(v)

        raise ValueError("MapasMunicipales::get_shapefile_importer for basename '{}' not found".format(basename))
