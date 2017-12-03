# -*- coding: utf-8 -*-

import os
import logging
import tempfile
import zipfile
import glob
import shutil

from datasets.utils.importers import ine

log = logging.getLogger(__name__)


class MapasMunicipales:
    id = 'mapas_municipales'

    def __init__(self, download_log):
        self.item = download_log

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
        except Exception as e:
            raise

        files = glob.glob(os.path.join(tmp_folder, "*.ini"))
        nfiles = len(files)
        for i, file in enumerate(files, 1):
            log.debug("[{}/{}] Import file '{}'".format(i, nfiles, file))
            try:
                ine.import_resource(file, self.item)
            except Exception as e:
                log.error("Error importing resource '{}'".format(file))

        log.debug("Remove tmp folder '{}'".format(tmp_folder))
        shutil.rmtree(tmp_folder)

