# -*- coding: utf-8 -*-

import os
import uuid
from django.conf import settings
from django.utils.text import slugify
from presura.utils import download
from ine.models import DownloadLog

DATA_DIR = getattr(settings, 'DATA_DIR', None)

import logging
log = logging.getLogger(__name__)


def get_unique_filename(base_path, ext=None):
    unique_id = uuid.uuid4().hex
    if ext:
        unique_id = unique_id + "." + ext
    filename = os.path.join(base_path, unique_id)
    assert not os.path.exists(filename)
    return filename


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
            filename = get_unique_filename(base_path, resource.ext)

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
