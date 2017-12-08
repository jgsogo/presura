# -*- coding: utf-8 -*-

from django.db import models

from model_utils import Choices

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


class Map(models.Model):
    """
    TILE_MAP_BASE = Choices((0, 'OSM', _("Open Stree Maps")),
                            (), ())
    """
    name = models.CharField(max_length=64)

    _tile_map_base = models.CharField(max_length=64, blank=True, null=True,
                                      choices=[(k, k) for k in tiles.keys()], )
    # bbox =
    # basemap  https://github.com/MatthewDaws/TileMapBase

    @property
    def tile_map_base(self):
        return tiles.get(self._tile_map_base, None)


class MapLayer(models.Model):
    map = models.ForeignKey(Map, on_delete=models.CASCADE)
    layer = models.ForeignKey(Map, on_delete=models.CASCADE, related_name='maps')
    z_index = models.PositiveSmallIntegerField(default=0)

