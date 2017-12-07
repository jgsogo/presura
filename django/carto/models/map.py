# -*- coding: utf-8 -*-

from django.db import models

from .layer import Layer


class Map(models.Model):
    name = models.CharField(max_length=64)
    # bbox =
    # basemap  https://github.com/MatthewDaws/TileMapBase


class MapLayer(models.Model):
    map = models.ForeignKey(Map, on_delete=models.CASCADE)
    layer = models.ForeignKey(Map, on_delete=models.CASCADE)
    z_index = models.PositiveSmallIntegerField(default=0)

