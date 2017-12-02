# -*- coding: utf-8 -*-

import os
import glob
import shapefile
import logging
import tempfile
import zipfile
import shutil
from django.contrib.gis.geos import Point, Polygon
from datasets.models import Author, DataSet

log = logging.getLogger(__name__)


class ShapefileImporter:
    model = None
    fields = None
    pattern = None

    def __init__(self, filename):
        self.sf = shapefile.Reader(filename)
        self.check_fields()

    def check_fields(self):
        original_fields = [it[0] for it in self.sf.fields[1:]]
        importer_fields = [it[0] for it in self.fields]
        assert set(original_fields) == set(importer_fields), \
            "Fields in file '{}' and those defined '{}' mismatch".format(','.join(list(set(original_fields))),
                                                                         ','.join(list(set(importer_fields))))

    def import_all(self, dataset):
        # TODO: Do it in bulk way
        for shapeRecs in self.sf.shapeRecords():
            item = self.model()
            for i, field in enumerate(self.fields, 1):
                ori, tgt = field
                if tgt:
                    setattr(item, tgt, shapeRecs.record[i])
            item.dataset = dataset
            #item.bbox = Polygon(shapeRecs.shape.bbox)
            item.points = Polygon(shapeRecs.shape.points)
            item.save()  # TODO: Uncomment


class INEBaseImporter:
    id = None

    def __init__(self, download_log):
        self.item = download_log
        self.author, _ = Author.objects.get_or_create(name="INE",
                                                      type=Author.TYPE.institution,
                                                      url="http://www.ine.es/")

    def run(self):
        # Extract
        tmp_folder = tempfile.mkdtemp()
        try:
            log.debug("Extract '{}' to temporary folder '{}'".format(self.item.filename, tmp_folder))
            assert zipfile.is_zipfile(self.item.filename)
            with zipfile.ZipFile(self.item.filename) as f:
                if not os.path.exists(tmp_folder):
                    os.makedirs(tmp_folder)
                f.extractall(path=tmp_folder)

            files = glob.glob(os.path.join(tmp_folder, "*.shp"))
            nfiles = len(files)
            for i, file in enumerate(files, 1):
                log.debug("[{}/{}] Import file '{}'".format(i, nfiles, file))
                self.import_shp_file(file)
        except Exception as e:
            raise
        finally:
            import time
            time.sleep(1)
            log.debug("Remove tmp folder '{}'".format(tmp_folder))
            shutil.rmtree(tmp_folder)

    def import_shp_file(self, filename):
        sf = self.get_shapefile_importer(filename)
        if sf and not self.item.dataset:
            dataset = DataSet(content_object=self.item)
            dataset.name = os.path.basename(filename)
            dataset.author = self.author
            dataset.save()
            try:
                sf.import_all(dataset)
            except Exception as e:
                log.exception("Importing filename '{}'".format(filename))
                dataset.delete()

    def get_shapefile_importer(self, filename):
        raise NotImplementedError

