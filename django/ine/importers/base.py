# -*- coding: utf-8 -*-

import os
import glob
import shapefile
import logging
import tempfile
import zipfile
import shutil
import json
from collections import defaultdict
from django.contrib.gis.geos import Point, Polygon, MultiPolygon
from django.contrib.gis.gdal import SpatialReference, CoordTransform
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
        # Credit: Sistemas de coordenadas usados en España: http://www.cartesia.org/foro/viewtopic.php?p=59091#59091
        gcoord = SpatialReference(4326)  # WGS84
        mycoord = SpatialReference(23030)  # Proyección UTM ED50 Huso 30 N
        trans = CoordTransform(mycoord, gcoord)
        # TODO: Do it in bulk way
        for shape in self.sf.shapeRecords():
            item = self.model()
            item.dataset = dataset
            for i, field in enumerate(self.fields, 0):
                ori, tgt = field
                if tgt:
                    if tgt == 'name':
                        name = shape.record[i]
                        name = name if not isinstance(name, bytes) else name.decode('latin-1')
                        setattr(item, tgt, name)
                    else:
                        setattr(item, tgt, shape.record[i])
            #item.bbox = Polygon(shapeRecs.shape.bbox)
            parts = list(shape.shape.parts) + [len(shape.shape.points)]
            polygons = []
            for it in zip(parts[:-1], parts[1:]):
                polygons.append(Polygon(shape.shape.points[it[0]:it[1]]))
            item.points = MultiPolygon(polygons)
            item.points.transform(trans)
            item.save()  # TODO: Uncomment

    def fields_sample(self, n=3):
        ret = defaultdict(list)
        for i, field in enumerate([it[0] for it in self.sf.fields[1:]], 0):
            for shape in self.sf.shapeRecords()[:n]:
                value = shape.record[i]
                value = value if not isinstance(value, bytes) else value.decode('latin-1')
                ret[field].append(value)
        return ret


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
        if not sf:
            return
        dataset_name = os.path.basename(filename)
        if not self.item.dataset.filter(name=dataset_name):
            dataset = DataSet(content_object=self.item)
            dataset.name = dataset_name
            dataset.author = self.author

            fields_sample = sf.fields_sample()
            txt = ""
            for key, values in fields_sample.items():
                txt += "{}: {}\n".format(key, ', '.join(map(str, values)))
            dataset.fields_sample = txt

            dataset.save(skip_img=True)
            try:
                sf.import_all(dataset)
            except Exception as e:
                log.exception("Importing filename '{}'".format(filename))
                dataset.delete()
        else:
            log.debug("Dataset for resource '{}' is already loaded".format(self.item))

    def get_shapefile_importer(self, filename):
        raise NotImplementedError

