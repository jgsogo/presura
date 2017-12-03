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
    lw = 0.3
    dpi = 300

    image = models.ImageField(upload_to='plotables/', blank=True, null=True)

    class Meta:
        abstract = True

    def save(self, skip_plot=False, *args, **kwargs):
        if not self.image and not skip_plot:
            self.save_plot()
        super(PlottableCached, self).save(*args, **kwargs)

    def get_title(self):
        return None

    def save_plot(self):
        log.debug("PlottableCached::save_plot")
        figure = self.savefig(tgt_srid=self.tgt_srid, title=self.get_title(), dpi=self.dpi, lw=self.lw)
        self.image.delete()
        filename = "{}.png".format(self.name) if settings.DEBUG else str(uuid.uuid4())
        self.image.save(filename, ImageFile(figure))

