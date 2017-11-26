import os
import logging
from urllib import parse

from django.db import models
from django.utils.translation import gettext as _
from django.conf import settings
from django.utils.text import slugify

from model_utils import Choices

log = logging.getLogger(__name__)


class ResourceManager(models.Manager):
    def available(self):
        return self.filter(available=True)


class Resource(models.Model):
    TYPE = Choices((0, 'carto', _('Cartographic')),
                   (1, 'demo', _('Demographic')),)

    name = models.CharField(max_length=255)
    type = models.IntegerField(choices=TYPE)
    url = models.URLField()
    available = models.BooleanField(default=True)
    ext = models.CharField(_('extension'), max_length=12)

    objects = ResourceManager()

    def __str__(self):
        return self.name


class DownloadLog(models.Model):
    resource = models.ForeignKey(Resource, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)
    filename = models.FilePathField(path=settings.INE_RESOURCES, editable=False)
    deleted = models.BooleanField(default=False)

    class Meta:
        ordering = ['-timestamp']

    def delete(self, *args, **kwargs):
        self.delete_file(commit=False)
        super(DownloadLog, self).delete(*args, **kwargs)

    def delete_file(self, commit=True):
        if not self.deleted:
            log.info("Resource '{}' file '{}' will be deleted".format(self.resource, self.filename))
            os.remove(str(self.filename))
            if commit:
                self.deleted = True
                self.save()
