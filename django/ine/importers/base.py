# -*- coding: utf-8 -*-

import os
import glob
import shapefile
import logging
import tempfile
import zipfile
import shutil
from ine.models import DownloadLog
from django.contrib.gis.geos import Point, Polygon

log = logging.getLogger(__name__)


class ShapefileImporter:
    model = None
    fields = None
    pattern = None

    def __init__(self, filename):
        self.sf = shapefile.Reader(filename)

    def check_fields(self):
        for it, i in enumerate(self.sf.fields[1:], 0):
            assert it[0] == self.fields[i], "Fields in file and those defined mismatch"

    def import_all(self):
        # TODO: Do it in bulk way
        for shapeRecs in self.sf.shapeRecords():
            item = self.model()
            for i, field in enumerate(self.fields, 1):
                ori, tgt = field
                if tgt:
                    setattr(item, tgt, shapeRecs.record[i])
            #item.bbox = Polygon(shapeRecs.shape.bbox)
            # item.points = Polygon(shapeRecs.shape.points)
            # item.save() # TODO: Uncomment


class BaseImporter:
    id = None

    def __init__(self, download_log):
        self.item = download_log

    def run(self):
        # Extract
        tmp_folder = tempfile.mkdtemp()
        log.debug("Extract '{}' to temporary folder '{}'".format(self.item.filename, tmp_folder))
        try:
            assert zipfile.is_zipfile(self.item.filename)
            with zipfile.ZipFile(self.item.filename) as f:
                if not os.path.exists(tmp_folder):
                    os.makedirs(tmp_folder)
                f.extractall(path=tmp_folder)

            files = glob.glob(os.path.join(tmp_folder, "*.shp"))
            nfiles = len(files)
            for i, file in enumerate(files, 1):
                try:
                    log.debug("[{}/{}] Import file '{}'".format(i, nfiles, file))
                    self.import_shp_file(file)
                except Exception as e:
                    log.error(e)
        except Exception:
            raise
        finally:
            import time
            time.sleep(1)
            shutil.rmtree(tmp_folder)

    def import_shp_file(self, filename):
        sf = self.get_shapefile_importer(filename)
        sf.import_all()

    def get_shapefile_importer(self, filename):
        raise NotImplementedError

