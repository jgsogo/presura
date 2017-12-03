# -*- coding: utf-8 -*-

from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.utils.translation import gettext as _
from django.contrib.postgres.fields import ArrayField

from datasets.models.author import Author
from datasets.models._plottable import PlottableCached


class DataSet(PlottableCached):
    # Basic information
    name = models.CharField(_('name'), max_length=255)
    author = models.ForeignKey(_('author'), Author, blank=True, null=True)
    license = models.CharField(_('license'), max_length=64, blank=True, null=True)  # TODO: Use choices (or fk)
    is_public = models.NullBooleanField(_('is public'))  # TODO: Get from license
    description = models.TextField(blank=True, null=True)
    published = models.DateField(_('publish date'), blank=True, null=True)
    url = models.URLField(_('url'), blank=True, null=True)

    # Link to resource: required?
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')

    # Data raw
    fields = ArrayField(models.CharField(max_length=20))
    key_field = models.CharField(max_length=64)
    name_field = models.CharField(max_length=64)

    key_field_name = models.CharField(max_length=64)
    name_field_name = models.CharField(max_length=64)

    def __str__(self):
        return self.name

    def get_title(self):
        return str(self)

    def get_shapes(self):
        return self.shape_set.all()
