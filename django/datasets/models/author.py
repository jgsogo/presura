# -*- coding: utf-8 -*-
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

    def __str__(self):
        return self.name
