# -*- coding: utf-8 -*-

import logging
import uuid
from django.db import models
from django.conf import settings
from django.core.files.images import ImageFile

from datasets.utils.plottable import Plottable

log = logging.getLogger(__name__)


class PlottableCached(Plottable, models.Model):
    tgt_srid = 23030  # Proyección UTM ED50 Huso 30 N

    image = models.ImageField(upload_to='plotables/', blank=True, null=True)
    image_lw = models.FloatField(default=0.3)
    image_dpi = models.IntegerField(default=400)

    class Meta:
        abstract = True

    def __init__(self, *args, **kwargs):
        super(PlottableCached, self).__init__(*args, **kwargs)
        self.__original_image_line = self.image_lw
        self.__original_image_dpi = self.image_dpi

    def save(self, skip_plot=False, *args, **kwargs):
        if not skip_plot and (self.__original_image_dpi != self.image_dpi or self.__original_image_line != self.image_lw):
            self.__original_image_line = self.image_lw
            self.__original_image_dpi = self.image_dpi
            self.save_plot()
        super(PlottableCached, self).save(*args, **kwargs)

    def get_title(self):
        return None

    def save_plot(self):
        log.debug("PlottableCached::save_plot")
        figure = self.savefig(tgt_srid=23030, title=self.get_title(), dpi=self.image_dpi, lw=self.image_lw)
        self.image.delete()
        filename = "{}.png".format(self.name) if settings.DEBUG else str(uuid.uuid4())
        self.image.save(filename, ImageFile(figure))

