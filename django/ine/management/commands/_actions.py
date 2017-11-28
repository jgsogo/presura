# -*- coding: utf-8 -*-

import os
import tempfile
import shutil
import zipfile
import glob
from django.conf import settings
from presura.utils import download, get_unique_filename
from ine.models import DownloadLog
from ine.importers import get_importer

DATA_DIR = getattr(settings, 'DATA_DIR', None)

import logging
log = logging.getLogger(__name__)


class DownloadAction:
    id = 'download'

    def __init__(self, stdout, stderr, override=True, *args, **kwargs):
        self.override = override
        self.stdout = stdout
        self.stderr = stderr

    def run(self, resource):
        # Is it already downloaded?
        qs = DownloadLog.objects.filter(resource=resource, deleted=False)
        if not self.override and qs.exists():
            self.stdout.write("\tUsing existing file '{}'".format(qs.latest('timestamp').filename))
        else:
            base_path = DownloadLog._meta.get_field('filename').path
            os.makedirs(base_path, exist_ok=False)
            filename = get_unique_filename(base_path)

            # Download
            try:
                self.stdout.write("\tDownload to '{}'".format(filename))
                logm = DownloadLog(resource=resource)
                logm.filename = filename
                download(resource.url, logm.filename)
                logm.save()
            except (Exception, KeyboardInterrupt) as e:
                self.stderr.write("Download interrupted, file '{}' will be deleted".format(filename))
                os.remove(filename)
                raise


class ImportAction:
    id = 'import'

    def __init__(self, stdout, stderr, *args, **kwargs):
        self.stdout = stdout
        self.stderr = stderr

    def run(self, resource):
        try:
            item = DownloadLog.objects.filter(resource=resource, deleted=False).latest('timestamp')
            self.stdout.write("\tUsing file for date {}".format(item.timestamp))
            importer = get_importer(resource, item)
            importer.run()
        except DownloadLog.DoesNotExist:
            self.stderr.write("\tDownload resource before importing it")


class Action:
    actions = [DownloadAction, ImportAction]  # Order here is important!

    @staticmethod
    def list():
        return [act.id for act in Action.actions]

    @staticmethod
    def choose_action(id):
        for act in Action.actions:
            if act.id == id:
                return act

    def __init__(self, id, *args, **kwargs):
        act = self.choose_action(id)
        self.action = act(*args, **kwargs)

    def run(self, resource):
        return self.action.run(resource)
