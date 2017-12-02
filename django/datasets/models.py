
import io
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import uuid
import logging
from django.db import models
from django.core.files.images import ImageFile
from django.utils.translation import gettext as _
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.contrib.gis.gdal import SpatialReference, CoordTransform
from django.conf import settings


from model_utils import Choices

log = logging.getLogger(__name__)


class Author(models.Model):
    TYPE = Choices((0, 'person', _('person')),
                   (1, 'institution', _('institution')),
                   (2, 'corporate', _('corporate')))

    name = models.CharField(_('name'), max_length=255)
    type = models.IntegerField(_('type'), choices=TYPE, blank=True, null=True)
    url = models.URLField(_('url'), blank=True, null=True)

    def __str__(self):
        return self.name


class DataSet(models.Model):
    name = models.CharField(_('name'), max_length=255)
    author = models.ForeignKey(_('author'), Author)
    license = models.CharField(_('license'), max_length=64, blank=True, null=True)  # TODO: Use choices (or fk)
    is_public = models.NullBooleanField(_('is public'))  # TODO: Get from license
    description = models.TextField(blank=True, null=True)

    image = models.ImageField(upload_to='datasets/', blank=True, null=True)
    image_line = models.FloatField(default=0.3)
    image_dpi = models.IntegerField(default=400)

    published = models.DateField(_('publish date'), blank=True, null=True)
    url = models.DateField(_('url'), blank=True, null=True)

    fields_sample = models.TextField(blank=True, null=True, help_text=_("Fields in file and example values"))

    # Link to resource
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')

    def __init__(self, *args, **kwargs):
        super(DataSet, self).__init__(*args, **kwargs)
        self.__original_image_line = self.image_line
        self.__original_image_dpi = self.image_dpi

    def __str__(self):
        return self.name

    def save(self, skip_img=False, *args, **kwargs):
        if not skip_img and self.__original_image_dpi != self.image_dpi or self.__original_image_line != self.image_line:
            self.__original_image_line = self.image_line
            self.__original_image_dpi = self.image_dpi
            self.plot()
        super(DataSet, self).save(*args, **kwargs)

    def plot(self):
        gcoord = SpatialReference(4326)  # WGS84
        mycoord = SpatialReference(23030)  # Proyección UTM ED50 Huso 30 N
        trans = CoordTransform(gcoord, mycoord)

        log.debug("Plot image for dataset '{}'".format(self.name))
        figure = io.BytesIO()
        fig = plt.figure()
        plt.axis('equal')
        plt.axis('off')
        for municipality in self.municipality_set.all():
            for poly in municipality.points:
                poly.transform(trans)
                x = [it[0] for it in poly.coords[0]]
                y = [it[1] for it in poly.coords[0]]
                plt.plot(x, y, lw=self.image_line)
        fig.suptitle(self.name)
        fig.savefig(figure, format='png', dpi=self.image_dpi)
        plt.close()

        self.image.delete()
        filename = "{}.png".format(self.name) if settings.DEBUG else str(uuid.uuid4())
        self.image.save(filename, ImageFile(figure))

