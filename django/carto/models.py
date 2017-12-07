
import logging
from django.contrib.gis.db import models
from django.utils.translation import gettext as _
from django.core.validators import MaxValueValidator, MinValueValidator

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
    colormap = models.CharField(max_length=20, default='hot')
    alpha = models.FloatField(default=1., validators=[MinValueValidator(0.0), MaxValueValidator(1.0)])

    # Data
    data = models.ForeignKey(INEPadron, on_delete=models.CASCADE)
    category = models.CharField(max_length=128, blank=True, null=True, help_text=_("Category to plot"))
    period = models.PositiveIntegerField(blank=True, null=True)

    # Colors
    draw_type = models.IntegerField(choices=DRAW_TYPE, default=DRAW_TYPE.line)
    color_pattern = models.IntegerField(choices=COLOR_PATTERN, default=COLOR_PATTERN.random)

    # TODO: There is a lot to validate
    #   - the map correspond to the data
    #   - the category exists in data
    #   - period exists in data

    def __str__(self):
        return self.name

    def get_data(self):
        qs = self.data.padronitem_set.all()
        for item in qs:
            key, name = item.key_name()
            yield key, item

    def get_shapes(self):
        # Select model to draw
        WrapperModel = plottable.ShapePolygon if self.draw_type == Layer.DRAW_TYPE.fill else plottable.ShapeLine

        drawables = []
        shapes = {shape.key: shape for shape in self.basemap.shape_set.all()}
        values = []
        for key, item in self.get_data():
            shape = shapes.get(key, None)
            if shape:
                value = item.get(self.category, self.period)
                values.append(value)
                drawables.append(WrapperModel(shape.polygons.srid, shape.polygons, value=value, alpha=self.alpha))
            else:
                log.warning("Shape not found for data key '{}' => {}".format(key, item))

        # Normalize values
        vmax, vmin = max(values), min(values)
        self.use_colormap(cmap=self.colormap, maxvalue=vmax, minvalue=vmin)

        # TODO: Log those shapes not found in data
        data = {k: v for k, v in self.get_data()}
        for key, shape in shapes.items():
            if key not in data:
                print("Data not found for shape key '{}' => {}".format(key, shape))
                #drawables.append(WrapperModel(shape.polygons.srid, shape.polygons, vmax*2))

        return drawables

    def save_image(self, filename):
        bytes = self.savefig(tgt_srid=self.spatial_reference, title=self.name)
        with open(filename, 'wb') as f:
            bytes.seek(0)
            f.write(bytes.read())

