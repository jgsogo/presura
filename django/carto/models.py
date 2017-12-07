
import logging
from django.contrib.gis.db import models
from django.utils.translation import gettext as _
from model_utils import Choices

from datasets.models import INEMap, INEPadron
from datasets.utils import plottable

log = logging.getLogger(__name__)


class Layer(plottable.Plottable, models.Model):
    DRAW_TYPE = Choices((0, 'line', _('Line')),
                        (1, 'fill', _('Filled')))
    SPATIAL_REFERENCE = Choices((4326, 'wgs84', 'WGS84'),
                                (23030, 'utmED50H30N', _("Proyección UTM ED50 Huso 30 N")))
    COLOR_PATTERN = Choices((0, 'random', _("Random")),)

    name = models.CharField(max_length=64)

    # Map
    basemap = models.ForeignKey(INEMap, on_delete=models.CASCADE)
    spatial_reference = models.IntegerField(choices=SPATIAL_REFERENCE, default=SPATIAL_REFERENCE.wgs84)

    # Data
    data = models.ForeignKey(INEPadron, on_delete=models.CASCADE)
    category = models.CharField(max_length=128, blank=True, null=True, help_text=_("Category to plot"))
    period = models.PositiveIntegerField(blank=True, null=True)

    # Colors
    draw_type = models.IntegerField(choices=DRAW_TYPE, default=DRAW_TYPE.line)
    color_pattern = models.IntegerField(choices=COLOR_PATTERN, default=COLOR_PATTERN.random)

    def __str__(self):
        return self.name

    def get_shapes(self):
        WrapperModel = plottable.ShapePolygon if self.draw_type == Layer.DRAW_TYPE.fill else plottable.ShapeLine
        for shape in self.basemap.shape_set.all():
            yield WrapperModel(shape.polygons.srid, shape.polygons)

    def save_image(self, filename):
        bytes = self.savefig(tgt_srid=self.spatial_reference, title=self.name)
        with open(filename, 'wb') as f:
            bytes.seek(0)
            f.write(bytes.read())

