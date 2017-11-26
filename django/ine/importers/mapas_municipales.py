# -*- coding: utf-8 -*-

import re
import os
from .base import BaseImporter, ShapefileImporter
from carto.models import Municipality


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
              ('PROVMUN', None),
              ]

class MapasMunicipales(BaseImporter):
    id = 'mapas_municipales'

    def get_shapefile_importer(self, filename):
        basename = os.path.basename(filename)

        if CCAA00Importer.pattern.match(basename):
            return CCAA00Importer(filename)

        raise ValueError("MapasMunicipales::get_shapefile_importer for basename '{}' not found".format(basename))
