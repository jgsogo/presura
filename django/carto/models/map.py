# -*- coding: utf-8 -*-

from django.db import models

from model_utils import Choices

from datasets.models._plottable import PlottableCached
from datasets.utils import plottable
from .layer import Layer


def get_tiles():
    import tilemapbase.tiles
    import inspect
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
    colormap = models.CharField(max_length=20, default='hot')

    # basemap  https://github.com/MatthewDaws/TileMapBase

    def __str__(self):
        return self.name

    @property
    def tile_map_base(self):
        return tiles.get(self._tile_map_base, None)

    def get_shapes(self):
        for maplayer in self.maplayer_set.all():
            for item in maplayer.layer.get_shapes():
                yield item

    def savefig(self, showcmap=None, cmap=None, *args, **kwargs):
        return super(Map, self).savefig(showcmap=True, cmap=self.colormap, *args, **kwargs)


class MapLayer(models.Model):
    map = models.ForeignKey(Map, on_delete=models.CASCADE)
    layer = models.ForeignKey(Layer, on_delete=models.CASCADE)
    z_index = models.PositiveSmallIntegerField(default=0)

