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
    pattern = [re.compile(r"ccaa00c\d{2}.shp"), ]
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
    pattern = [re.compile(r"ccaa0103c\d{2}.shp"), ]
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
    pattern = [re.compile(r"com99p\d{2}.shp"), re.compile(r"com99c\d{2}.shp"),]
    model = Municipality
    fields = [('OBJECTID', None),
              ('COMAGR', None),
              ('COMARCA99', None),
              ('Shape_Leng', None),
              ('Shape_Area', None),]


class CCAA99Importer(ShapefileImporter):
    pattern = [re.compile(r"ccaa99c\d{2}.shp"), ]
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
    pattern = [re.compile(r"prov00p\d{2}.shp"), ]
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


class PROV0104Importer(ShapefileImporter):
    pattern = [re.compile(r"prov0104p\d{2}.shp"),
               re.compile(r"esp_muni_0104.shp"),]
    model = Municipality
    fields = [('OBJECTID', None),
              ('Shape_Leng', None),
              ('Shape_Area', None),
              ('COM', None),
              ('PROVMUN', None),
              ('NOMBRE04', None),]


class PROV0101Importer(ShapefileImporter):
    pattern = [re.compile(r"prov0101p\d{2}.shp"),]
    model = Municipality
    fields = [('OBJECTID', None),
              ('AREA', None),
              ('PERIMETER', None),
              ('E20001_', None),
              ('E20001_ID', None),
              ('Shape_Leng', None),
              ('Shape_Area', None),
              ('COM', None),
              ('PROVMUN', None),
              ('NOMBRE01', None),]


class PROV99Importer(ShapefileImporter):
    pattern = [re.compile(r"prov99p\d{2}.shp"),]
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


class CCAA0109Importer(ShapefileImporter):
    pattern = [re.compile(r"ccaa010(5|6|7|8|9)c\d{2}.shp"),
               re.compile(r"prov010(5|6|7|8|9)p\d{2}.shp"),]
    model = Municipality
    fields = [('NOMBRE', None),
              ('PROVMUN', None)]


class PROV0102Importer(ShapefileImporter):
    pattern = [re.compile(r"prov0102p\d{2}.shp"),]
    model = Municipality
    fields = [('OBJECTID', None),
              ('AREA', None),
              ('PERIMETER', None),
              ('E20002_', None),
              ('E20002_ID', None),
              ('Shape_Leng', None),
              ('Shape_Area', None),
              ('COM', None),
              ('PROVMUN', None),
              ('NOMBRE02', None),]


class CCAA0101Importer(ShapefileImporter):
    pattern = [re.compile(r"ccaa0101c\d{2}.shp"),]
    model = Municipality
    fields = [('OBJECTID', None),
              ('AREA', None),
              ('PERIMETER', None),
              ('E20001_', None),
              ('E20001_ID', None),
              ('Shape_Leng', None),
              ('Shape_Area', None),
              ('PROVMUN', None),
              ('NOMBRE01', None),]


class PROV0103Importer(ShapefileImporter):
    pattern = [re.compile(r"prov0103p\d{2}.shp"),]
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
              ('PROVMUN', None),
              ('COM', None),]


class CCAA0104Importer(ShapefileImporter):
    pattern = [re.compile(r"ccaa0104c\d{2}.shp"),]
    model = Municipality
    fields = [('OBJECTID', None),
              ('Shape_Leng', None),
              ('Shape_Area', None),
              ('PROVMUN', None),
              ('NOMBRE04', None),]


class PROV1101Importer(ShapefileImporter):
    pattern = [re.compile(r"prov1101p\d{2}.shp"),
               re.compile(r"ccaa1101c\d{2}.shp"),]
    model = Municipality
    fields = [('OBJECTID', None),
              ('AREA', None),
              ('PERIMETER', None),
              ('E200NOV01_', None),
              ('E200NOV011', None),
              ('DEN01', None),
              ('NOMBRE02', None),
              ('Shape_Leng', None),
              ('Shape_Area', None),
              ('PROVMUN', None),]


class CCAA0102Importer(ShapefileImporter):
    pattern = [re.compile(r"ccaa0102c\d{2}.shp"),]
    model = Municipality
    fields = [('OBJECTID', None),
              ('AREA', None),
              ('PERIMETER', None),
              ('E20002_', None),
              ('E20002_ID', None),
              ('NOMBRE02', None),
              ('Shape_Leng', None),
              ('Shape_Area', None),
              ('PROVMUN', None),]


class SpainProvincesAg2Importer(ShapefileImporter):
    pattern = [re.compile(r"spain_provinces_ag_2.shp"),]
    model = Municipality
    fields = [('OBJECTID', None),
              ('AREA', None),
              ('PERIMETER', None),
              ('P20099_', None),
              ('P20099_ID', None),
              ('NOMBRE99', None),
              ('SHAPE_LENG', None),
              ('SHAPE_AREA', None),
              ('PROV', None),
              ('COM', None),]


class MapasMunicipales(BaseImporter):
    id = 'mapas_municipales'
    file_importers = [CCAA00Importer, CCAA0103Importer, CCAA99Importer, COM99Importer,
                      PROV00Importer, PROV0104Importer, PROV0101Importer, PROV99Importer,
                      CCAA0109Importer, PROV0102Importer, CCAA0101Importer,
                      PROV0103Importer, CCAA0104Importer, PROV1101Importer,
                      CCAA0102Importer, SpainProvincesAg2Importer, ]

    allit = defaultdict(list)
    missed = defaultdict(list)

    def get_shapefile_importer(self, filename):
        basename = os.path.basename(filename)

        for file_importer in self.file_importers:
            if any(pattern.match(basename) for pattern in file_importer.pattern):
                return file_importer(filename)

        # TODO: Remove code below (until raise)
        sf = shapefile.Reader(filename)
        fields = ', '.join([it[0] for it in sf.fields[1:]])
        for ff in self.file_importers:
            ff_fields = set([it[0] for it in ff.fields])
            if ff_fields == set([it[0] for it in sf.fields[1:]]):
                self.missed[str(ff)].append(filename)

        self.allit[fields].append(filename)

        print("-"*40)
        from pprint import pprint
        for it,v in self.allit.items():
            print(it)
            pprint(v)

        print("*"*40)
        for it,v in self.missed.items():
            print(it)
            pprint(v)

        raise ValueError("MapasMunicipales::get_shapefile_importer for basename '{}' not found".format(basename))
