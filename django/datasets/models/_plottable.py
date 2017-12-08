# -*- coding: utf-8 -*-

import logging
import uuid
from django.db import models
from django.conf import settings
from django.core.files.images import ImageFile
from django.utils.text import slugify

from datasets.utils.plottable import Plottable

log = logging.getLogger(__name__)


class PlottableCached(Plottable, models.Model):
    image = models.ImageField(upload_to='plotables/', blank=True, null=True)

    class Meta:
        abstract = True

    def save(self, skip_plot=False, *args, **kwargs):
        if not self.image and not skip_plot:
            self.save_plot()
        super(PlottableCached, self).save(*args, **kwargs)

    def save_plot(self):
        log.debug("PlottableCached::save_plot")
        name = str(self)
        tgt_srid = 23030  # Proyección UTM ED50 Huso 30 N

        figure = self.savefig(tgt_srid=tgt_srid, title=name, showcmap=False)
        self.image.delete()
        filename = "{}.png".format(slugify(name)) if settings.DEBUG else str(uuid.uuid4())
        self.image.save(filename, ImageFile(figure))
