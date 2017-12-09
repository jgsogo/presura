# -*- coding: utf-8 -*-

from django.db import models
# from django.contrib.gis.db import models

from model_utils import Choices
from django.contrib.gis.gdal import SpatialReference, CoordTransform
from datasets.models._plottable import PlottableCached
from django.core.validators import MaxValueValidator, MinValueValidator
from datasets.utils import plottable
from .layer import Layer
import tilemapbase
import inspect

tilemapbase.init(create=True)  # TODO: Just once


def get_tiles():
    ret = {}
    for name, obj in inspect.getmembers(tilemapbase.tiles):
        if isinstance(obj, tilemapbase.tiles.Tiles):
            ret[obj.name] = obj
    return ret

tiles = get_tiles()


class Map(PlottableCached):
    name = models.CharField(max_length=64)
    _tile_map_base = models.CharField(max_length=64, blank=True, null=True,
                                      choices=[(k, k) for k in tiles.keys()], )
    basemap_width = models.PositiveIntegerField(default=600)
    dpi = models.PositiveIntegerField(default=600)
    # bbox = models.MultiPointField(blank=True, null=True)

    # Colors
    draw_type = models.IntegerField(choices=Layer.DRAW_TYPE, default=Layer.DRAW_TYPE.line)
    colormap = models.CharField(max_length=20, default='hot')
    alpha = models.FloatField(default=1., validators=[MinValueValidator(0.0), MaxValueValidator(1.0)])
    lw = models.FloatField(default=0.1)

    def __str__(self):
        return self.name

    @property
    def tile_map_base(self):
        return tiles.get(self._tile_map_base, None)

    def get_bbox(self, tgt_srid):
        tgt_reference = SpatialReference(tgt_srid)
        bboxes = []
        for maplayer in self.maplayer_set.all():
            bbox = maplayer.layer.bbox
            trans = CoordTransform(SpatialReference(bbox.srid), tgt_reference)
            bbox.transform(trans)
            bboxes.append(bbox.extent)
        maximums = list(map(max, zip(*bboxes)))
        minimums = list(map(min, zip(*bboxes)))
        return minimums[0], minimums[1], maximums[2], maximums[3]

    def get_shapes(self):
        shape_properties = {'alpha': self.alpha,
                            'lw': self.lw,
                            'fill': self.draw_type == Layer.DRAW_TYPE.fill}
        for maplayer in self.maplayer_set.all():
            maplayer.layer.shape_properties = shape_properties
            for item in maplayer.layer.get_shapes():
                yield item

    def plot_basemap(self, ax, tgt_srid):
        xmin, ymin, xmax, ymax = self.get_bbox(tgt_srid=4326)
        extent = tilemapbase.Extent.from_lonlat(xmin, xmax, ymin, ymax)
        extent = extent.to_project_3857()
        plotter = tilemapbase.Plotter(extent, self.tile_map_base, width=self.basemap_width)
        plotter.plot(ax, self.tile_map_base, zorder=-1)

    def plot(self, ax, tgt_srid, cmap):
        super(Map, self).plot(ax, tgt_srid, cmap)
        if self.tile_map_base:
            self.plot_basemap(ax, tgt_srid)

    def savefig(self, showcmap=None, tgt_srid=None, dpi=300, cmap=None, *args, **kwargs):
        return super(Map, self).savefig(tgt_srid='epsg:3857', showcmap=True, dpi=self.dpi,
                                        cmap=self.colormap,
                                        *args, **kwargs)


class MapLayer(models.Model):
    map = models.ForeignKey(Map, on_delete=models.CASCADE)
    layer = models.ForeignKey(Layer, on_delete=models.CASCADE)
    z_index = models.PositiveSmallIntegerField(default=0)

