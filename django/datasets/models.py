from django.db import models
from django.utils.translation import gettext as _

from model_utils import Choices


class Author(models.Model):
    TYPE = Choices((0, 'person', _('person')),
                   (1, 'institution', _('institution')),
                   (2, 'corporate', _('corporate')))

    name = models.CharField(_('name'), max_length=255)
    type = models.IntegerField(_('type'), choices=TYPE, blank=True, null=True)
    url = models.URLField(_('url'), blank=True, null=True)


class DataSet(models.Model):
    name = models.CharField(_('name'), max_length=255)
    author = models.ForeignKey(_('author'), Author)
    license = models.CharField(_('license'), max_length=64)  # TODO: Use choices (or fk)
    is_public = models.NullBooleanField(_('is public'))  # TODO: Get from license
    description = models.TextField()

    published = models.DateField(_('publish date'), blank=True, null=True)
    url = models.DateField(_('url'), blank=True, null=True)

    # TODO: May add contenttype to link to a table inside this project.
