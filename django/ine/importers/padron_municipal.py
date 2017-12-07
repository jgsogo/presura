# -*- coding: utf-8 -*-

import os
import logging
import tempfile
import zipfile
import glob
import shutil

from datasets.utils.importers import ine

log = logging.getLogger(__name__)


class PadronMunicipal:
    id = 'padron_municipal'

    def __init__(self, download_log):
        self.item = download_log

    def run(self):
        # Check if it has been already imported
        if self.item.datasets.exists():
            log.info("Download log '{}' for resource '{}' has already been imported".format(self.item.timestamp, self.item.resource))
            return

        # Extract
        tmp_folder = tempfile.mkdtemp()
        try:
            try:
                log.debug("Extract '{}' to temporary folder '{}'".format(self.item.filename, tmp_folder))
                assert zipfile.is_zipfile(self.item.filename)
                with zipfile.ZipFile(self.item.filename) as f:
                    if not os.path.exists(tmp_folder):
                        os.makedirs(tmp_folder)
                    f.extractall(path=tmp_folder)
            except Exception as e:
                raise

            path_to_search = os.path.join(tmp_folder, "DATOS", "padron", "**", "*.px")
            log.debug("Search for '.px' files using '{}'".format(path_to_search))
            files = glob.glob(path_to_search, recursive=True)
            nfiles = len(files)
            for i, file in enumerate(files, 1):
                log.debug("[{}/{}] Import file '{}'".format(i, nfiles, file))
                try:
                    ine.import_pcaxis(file, self.item)
                except Exception as e:
                    log.exception("Error importing resource '{}'".format(file))

        except Exception:
            raise
        except KeyboardInterrupt:
            pass
        finally:
            log.debug("Remove tmp folder '{}'".format(tmp_folder))
            shutil.rmtree(tmp_folder)

