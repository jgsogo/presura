# -*- coding: utf-8 -*-

from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.utils.translation import gettext as _

from datasets.models.author import Author


class Dataset(models.Model):
    # Basic information
    name = models.CharField(_('name'), max_length=255)
    author = models.ForeignKey(_('author'), Author, blank=True, null=True)
    license = models.CharField(_('license'), max_length=64, blank=True, null=True)  # TODO: Use choices (or fk)
    is_public = models.NullBooleanField(_('is public'))  # TODO: Get from license
    description = models.TextField(blank=True, null=True)
    published = models.DateField(_('publish date'), blank=True, null=True)
    url = models.URLField(_('url'), blank=True, null=True)

    # Link to resource/download-log: required?
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')

    dataset_key = models.CharField(max_length=64, blank=True, null=True,
                                   help_text=_("Identification of this dataset inside the resource"))

    class Meta:
        ordering = ['dataset_key',]

    def __str__(self):
        return "({}) {}".format(self.dataset_key, self.name)
