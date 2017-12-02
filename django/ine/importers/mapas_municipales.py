# -*- coding: utf-8 -*-

import re
import os
import shapefile
import logging
from collections import defaultdict
from .base import INEBaseImporter, ShapefileImporter
from django.conf import settings
from carto.models import Municipality

log = logging.getLogger(__name__)


class CCAA00Importer(ShapefileImporter):
    pattern = [re.compile(r"ccaa00c\d{2}.shp"),
               re.compile(r"prov00p\d{2}.shp"), ]
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
              ('PROVMUN', None), ]


class CCAA0103Importer(ShapefileImporter):
    pattern = [re.compile(r"ccaa0103c\d{2}.shp"), ]
    model = Municipality
    fields = [('OBJECTID', None),
              ('AREA', 'area'),
              ('PERIMETER', 'perimeter'),
              ('E20003_', None),
              ('E20003_ID', None),
              ('NOMBRE03', 'name'),
              ('PROV', None),
              ('MUN', None),
              ('Shape_Leng', None),
              ('Shape_Area', None),
              ('PROVMUN', None), ]


class COM99Importer(ShapefileImporter):
    pattern = [re.compile(r"com99p\d{2}.shp"),
               re.compile(r"com99c\d{2}.shp"),
               re.compile(r"esp_com_99.shp"), ]
    model = Municipality
    fields = [('OBJECTID', None),
              ('COMAGR', None),
              ('COMARCA99', None),
              ('Shape_Leng', None),
              ('Shape_Area', None), ]


class CCAA99Importer(ShapefileImporter):
    pattern = [re.compile(r"ccaa99c\d{2}.shp"),
               re.compile(r"prov99p\d{2}.shp"), ]
    model = Municipality
    fields = [('OBJECTID', None),
              ('AREA', 'area'),
              ('PERIMETER', 'perimeter'),
              ('E20099_', None),
              ('E20099_ID', None),
              ('NOMBRE99', 'name'),
              ('Shape_Leng', None),
              ('Shape_Area', None),
              ('PROVMUN', None),
              ('COM', None), ]


class PROV0104Importer(ShapefileImporter):
    pattern = [re.compile(r"prov0104p\d{2}.shp"),
               re.compile(r"esp_muni_0104.shp"), ]
    model = Municipality
    fields = [('OBJECTID', None),
              ('Shape_Leng', None),
              ('Shape_Area', None),
              ('COM', None),
              ('PROVMUN', None),
              ('NOMBRE04', 'name'), ]


class PROV0101Importer(ShapefileImporter):
    pattern = [re.compile(r"prov0101p\d{2}.shp"),
               re.compile(r"esp_muni_0101.shp"), ]
    model = Municipality
    fields = [('OBJECTID', None),
              ('AREA', 'area'),
              ('PERIMETER', 'perimeter'),
              ('E20001_', None),
              ('E20001_ID', None),
              ('Shape_Leng', None),
              ('Shape_Area', None),
              ('COM', None),
              ('PROVMUN', None),
              ('NOMBRE01', 'name'), ]


class CCAA0109Importer(ShapefileImporter):
    pattern = [re.compile(r"ccaa010(5|6|7|8|9)c\d{2}.shp"),
               re.compile(r"prov010(5|6|7|8|9)p\d{2}.shp"),
               re.compile(r"esp_muni_0109.shp"), ]
    model = Municipality
    fields = [('NOMBRE', None),
              ('PROVMUN', None)]


class PROV0102Importer(ShapefileImporter):
    pattern = [re.compile(r"prov0102p\d{2}.shp"),
               re.compile(r"esp_muni_0102.shp"), ]
    model = Municipality
    fields = [('OBJECTID', None),
              ('AREA', 'area'),
              ('PERIMETER', 'perimeter'),
              ('E20002_', None),
              ('E20002_ID', None),
              ('Shape_Leng', None),
              ('Shape_Area', None),
              ('COM', None),
              ('PROVMUN', None),
              ('NOMBRE02', 'name'), ]


class CCAA0101Importer(ShapefileImporter):
    pattern = [re.compile(r"ccaa0101c\d{2}.shp"), ]
    model = Municipality
    fields = [('OBJECTID', None),
              ('AREA', 'area'),
              ('PERIMETER', 'perimeter'),
              ('E20001_', None),
              ('E20001_ID', None),
              ('Shape_Leng', None),
              ('Shape_Area', None),
              ('PROVMUN', None),
              ('NOMBRE01', 'name'), ]


class PROV0103Importer(ShapefileImporter):
    pattern = [re.compile(r"prov0103p\d{2}.shp"),
               re.compile(r"esp_muni_0103.shp"), ]
    model = Municipality
    fields = [('OBJECTID', None),
              ('AREA', 'area'),
              ('PERIMETER', 'perimeter'),
              ('E20003_', None),
              ('E20003_ID', None),
              ('NOMBRE03', 'name'),
              ('PROV', None),
              ('MUN', None),
              ('Shape_Leng', None),
              ('Shape_Area', None),
              ('PROVMUN', None),
              ('COM', None), ]


class CCAA0104Importer(ShapefileImporter):
    pattern = [re.compile(r"ccaa0104c\d{2}.shp"), ]
    model = Municipality
    fields = [('OBJECTID', None),
              ('Shape_Leng', None),
              ('Shape_Area', None),
              ('PROVMUN', None),
              ('NOMBRE04', 'name'), ]


class PROV1101Importer(ShapefileImporter):
    pattern = [re.compile(r"prov1101p\d{2}.shp"),
               re.compile(r"ccaa1101c\d{2}.shp"), ]
    model = Municipality
    fields = [('OBJECTID', None),
              ('AREA', 'area'),
              ('PERIMETER', 'perimeter'),
              ('E200NOV01_', None),
              ('E200NOV011', None),
              ('DEN01', None),
              ('NOMBRE02', 'name'),
              ('Shape_Leng', None),
              ('Shape_Area', None),
              ('PROVMUN', None), ]


class CCAA0102Importer(ShapefileImporter):
    pattern = [re.compile(r"ccaa0102c\d{2}.shp"), ]
    model = Municipality
    fields = [('OBJECTID', None),
              ('AREA', 'area'),
              ('PERIMETER', 'perimeter'),
              ('E20002_', None),
              ('E20002_ID', None),
              ('NOMBRE02', 'name'),
              ('Shape_Leng', None),
              ('Shape_Area', None),
              ('PROVMUN', None), ]


class SpainProvincesAg2Importer(ShapefileImporter):
    pattern = [re.compile(r"spain_provinces_ag_2.shp"), ]
    model = Municipality
    fields = [('OBJECTID', None),
              ('AREA', 'area'),
              ('PERIMETER', 'perimeter'),
              ('P20099_', None),
              ('P20099_ID', None),
              ('NOMBRE99', 'name'),
              ('SHAPE_LENG', None),
              ('SHAPE_AREA', None),
              ('PROV', None),
              ('COM', None), ]


class SpainProvincesInd4Importer(ShapefileImporter):
    pattern = [re.compile(r"spain_provinces_ind_4.shp"), ]
    model = Municipality
    fields = [('OBJECTID', None),
              ('AREA', 'area'),
              ('PERIMETER', 'perimeter'),
              ('P20099_', None),
              ('P20099_ID', None),
              ('NOMBRE99', 'name'),
              ('Shape_Leng', None),
              ('Shape_Area', None),
              ('PROV', None),
              ('COM', None),
              ('DPROV', None), ]


class SpainRegionsImporter(ShapefileImporter):
    pattern = [re.compile(r"spain_regions_ag.shp"),
               re.compile(r"spain_regions_ind.shp"),
               re.compile(r"spain_regions_ind_a.shp")]
    model = Municipality
    fields = [('OBJECTID', None),
              ('AREA', 'area'),
              ('PERIMETER', 'perimeter'),
              ('C20099_', None),
              ('C20099_ID', None),
              ('NOMBRE99', 'name'),
              ('SHAPE_LENG', None),
              ('SHAPE_AREA', None),
              ('COM', None)]


class SpainProvincesImporter(ShapefileImporter):
    pattern = [re.compile(r"spain_provinces_img_ag_2.shp"),
               re.compile(r"spain_provinces_img_ind_4.shp")]
    model = Municipality
    fields = [('OBJECTID', None),
              ('AREA', 'area'),
              ('PERIMETER', 'perimeter'),
              ('P00091_', None),
              ('P00091_ID', None),
              ('NOMBRE99', 'name'),
              ('SHAPE_LENG', None),
              ('SHAPE_AREA', None),
              ('PROV', None),
              ('COM', None), ]


class SpainMuniImporter(ShapefileImporter):
    pattern = [re.compile(r"esp_muni_00.shp"), ]
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
              ('COM', None), ]


class SpainRegions91Importer(ShapefileImporter):
    pattern = [re.compile(r"spain_regions_img_ag.shp"),
               re.compile(r"spain_regions_img_ind.shp"), ]
    model = Municipality
    fields = [('OBJECTID', None),
              ('AREA', 'area'),
              ('PERIMETER', 'perimeter'),
              ('C00091_', None),
              ('C00091_ID', None),
              ('NOMBRE', 'name'),
              ('SHAPE_LENG', None),
              ('SHAPE_AREA', None),
              ('COM', None), ]


class SpainMuni99Importer(ShapefileImporter):
    pattern = [re.compile(r"esp_muni_99.shp"), ]
    model = Municipality
    fields = [('OBJECTID', None),
              ('AREA', 'area'),
              ('PERIMETER', 'perimeter'),
              ('E20099_', None),
              ('E20099_ID', None),
              ('NOMBRE99', 'name'),
              ('Shape_Leng', None),
              ('Shape_Area', None),
              ('PROVMUN', None), ]


class SpainProvinces2Importer(ShapefileImporter):
    pattern = [re.compile(r"spain_provinces_ind_2.shp"), ]
    model = Municipality
    fields = [('OBJECTID', None),
              ('AREA', 'area'),
              ('PERIMETER', 'perimeter'),
              ('P20099_', None),
              ('P20099_ID', None),
              ('NOMBRE99', 'name'),
              ('Shape_Leng', None),
              ('Shape_Area', None),
              ('PROV', None),
              ('COM', None), ]


class SpainProvincesImg2Importer(ShapefileImporter):
    pattern = [re.compile(r"spain_provinces_img_ind_2.shp"), ]
    model = Municipality
    fields = [('OBJECTID', None),
              ('AREA', 'area'),
              ('PERIMETER', 'perimeter'),
              ('P00091_', None),
              ('P00091_ID', None),
              ('NOMBRE99', 'name'),
              ('Shape_Leng', None),
              ('Shape_Area', None),
              ('PROV', None),
              ('COM', None), ]


class MapasMunicipales(INEBaseImporter):
    id = 'mapas_municipales'
    file_importers = [CCAA00Importer, CCAA0103Importer, CCAA99Importer, COM99Importer,
                      PROV0104Importer, PROV0101Importer,
                      CCAA0109Importer, PROV0102Importer, CCAA0101Importer,
                      PROV0103Importer, CCAA0104Importer, PROV1101Importer,
                      CCAA0102Importer, SpainProvincesAg2Importer, SpainProvincesInd4Importer,
                      SpainRegionsImporter, SpainProvincesImporter, SpainMuniImporter,
                      SpainRegions91Importer, SpainMuni99Importer, SpainProvinces2Importer,
                      SpainProvincesImg2Importer
                      ]

    def get_shapefile_importer(self, filename):
        basename = os.path.basename(filename)

        for file_importer in self.file_importers:
            if any(pattern.match(basename) for pattern in file_importer.pattern):
                return file_importer(filename)

        if getattr(settings, 'DEBUG', False):
            try:
                # Try to look a matching importer
                sf = shapefile.Reader(filename)
                fields = ', '.join([it[0] for it in sf.fields[1:]])
                for ff in self.file_importers:
                    ff_fields = set([it[0] for it in ff.fields])
                    if ff_fields == fields:
                        log.info("File '{}' matched against fields in '{}'".format(filename, str(ff)))
            except Exception as e:
                log.warning("Unhandled exception: {}".format(e))

        log.warning("MapasMunicipales::get_shapefile_importer for basename '{}' not found".format(basename))
        return None


if getattr(settings, 'DEBUG', False):
    # Check that there are no repeated importers
    for ff1 in MapasMunicipales.file_importers:
        fields1 = set([it[0] for it in ff1.fields])
        for ff2 in MapasMunicipales.file_importers:
            if ff1 == ff2: continue
            fields2 = set([it[0] for it in ff2.fields])
            if fields1 == fields2:
                log.error("Equal specification '{}' <=> '{}'".format(str(ff1), str(ff2)))
