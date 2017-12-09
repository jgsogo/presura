
import logging
import numpy as np
from django.contrib.gis.db import models
from django.utils.translation import gettext as _
from django.core.validators import MaxValueValidator, MinValueValidator
from django.contrib.gis.geos import GEOSGeometry, Polygon

from model_utils import Choices

from datasets.models import INEMap, INEPadron
from datasets.utils import plottable

log = logging.getLogger(__name__)


class Layer(plottable.Plottable, models.Model):
    DRAW_TYPE = Choices((0, 'line', _('Line')),
                        (1, 'fill', _('Filled')))
    SPATIAL_REFERENCE = Choices((4326, 'wgs84', 'WGS84'),
                                (23030, 'utmED50H30N', _("Proyección UTM ED50 Huso 30 N")))

    name = models.CharField(max_length=64)

    # Map
    basemap = models.ForeignKey(INEMap, on_delete=models.CASCADE)
    spatial_reference = models.IntegerField(choices=SPATIAL_REFERENCE, default=SPATIAL_REFERENCE.wgs84)

    # Data
    data = models.ForeignKey(INEPadron, on_delete=models.CASCADE)
    category = models.CharField(max_length=128, blank=True, null=True, help_text=_("Category to plot"))
    period = models.PositiveIntegerField(blank=True, null=True)
    per_area_unit = models.BooleanField(default=False)

    # Colors
    draw_type = models.IntegerField(choices=DRAW_TYPE, default=DRAW_TYPE.line)
    colormap = models.CharField(max_length=20, default='hot')
    alpha = models.FloatField(default=1., validators=[MinValueValidator(0.0), MaxValueValidator(1.0)])
    lw = models.FloatField(default=0.)

    # TODO: There is a lot to validate
    #   - the map correspond to the data
    #   - the category exists in data
    #   - period exists in data

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._shape_properties = None

    def __str__(self):
        return self.name

    @property
    def bbox(self):
        qs = self.basemap.shape_set.all().aggregate(extent=models.Extent('polygons'))
        poly = Polygon.from_bbox(qs['extent'])
        # TODO: srid for all shapes? May transform them when inserting
        poly.srid = self.basemap.shape_set.all()[0].polygons.srid
        return poly

    @property
    def shape_properties(self):
        if not self._shape_properties:
            self._shape_properties = {'alpha': self.alpha,
                                      'lw': self.lw,
                                      'fill': self.draw_type == Layer.DRAW_TYPE.fill,
                                      'zorder': 1}
        return self._shape_properties

    @shape_properties.setter
    def shape_properties(self, properties):
        self.shape_properties.update(properties)

    def get_data(self):
        qs = self.data.padronitem_set.all()
        for item in qs:
            key, name = item.key_name()
            yield key, item

    def get_shapes(self):
        log.debug("Layer::get_shapes - {}".format(self))
        # Select model to draw
        shape_builder = plottable.Shape.builder(**self.shape_properties)

        drawables = []
        shapes = {shape.key: shape for shape in self.basemap.shape_set.all()}
        values = []
        for key, item in self.get_data():
            shape = shapes.get(key, None)
            if shape:
                value = item.get(self.category, self.period)
                values.append(value)
                if self.per_area_unit:
                    value = value/shape.polygons.area  # TODO: en qué unidades estoy dividiendo?
                if value > 100000000.:
                    # TODO: ¿Qué hago con los outliers?
                    log.debug("\t OUTLIER!! {} - {} habs/u^2".format(item, value))
                drawables.append(shape_builder(srid=shape.polygons.srid, shape=shape.polygons, value=value))
            else:
                log.warning("Shape not found for data key '{}' => {}".format(key, item))

        # Log those shapes not found in data
        data = {k: v for k, v in self.get_data()}
        for key, shape in shapes.items():
            if key not in data:
                log.warning("Data not found for shape key '{}' => {}".format(key, shape))
                drawables.append(shape_builder(srid=shape.polygons.srid, shape=shape.polygons,
                                               value=0., alpha=1., color='b'))

        return drawables

    def save_image(self, filename):
        bytes = self.savefig(tgt_srid=self.spatial_reference, title=self.name,
                             cmap=self.colormap, showcmap=True)
        with open(filename, 'wb') as f:
            bytes.seek(0)
            f.write(bytes.read())

