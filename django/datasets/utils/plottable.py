# -*- coding: utf-8 -*-

import io
import logging
import numpy as np

import matplotlib
matplotlib.use('Agg')

from django.contrib.gis.gdal import SpatialReference, CoordTransform
import matplotlib.pyplot as plt
from matplotlib.patches import Circle, Wedge, Polygon
from matplotlib.collections import PatchCollection

log = logging.getLogger(__name__)

# TODO: Drawing rectangles... http://matthiaseisen.com/pp/patterns/p0203/


class Shape:
    srid = None
    shape = None
    value = 0.  # Need to set a value to get a color.
    alpha = 1.

    def __init__(self, srid, shape, value, alpha):
        self.spatial_ref = SpatialReference(srid)
        self.shape = shape
        self.value = value
        self.alpha = alpha

    def plot(self, target_reference, mapper, *args, **kwargs):
        raise NotImplementedError("Shape is abstract")


class ShapeLine(Shape):
    def plot(self, target_reference, mapper, *args, **kwargs):
        trans = CoordTransform(self.spatial_ref, target_reference)
        self.shape.transform(trans)
        for poly in self.shape:
            color = mapper.to_rgba(self.value)
            yield Polygon(poly.coords[0], closed=True, fill=False, color=color, alpha=self.alpha)


class ShapePolygon(Shape):
    def plot(self, target_reference, mapper, *args, **kwargs):
        trans = CoordTransform(self.spatial_ref, target_reference)
        self.shape.transform(trans)
        for poly in self.shape:
            color = mapper.to_rgba(self.value)
            yield Polygon(poly.coords[0], closed=True, fill=True, color=color, alpha=self.alpha)


class Plottable:
    shapes = None
    color_mapper = None

    def __init__(self, *args, **kwargs):
        super(Plottable, self).__init__(*args, **kwargs)
        self.use_colormap()

    def use_colormap(self, cmap='hot', maxvalue=1.0, minvalue=0.0):
        colormap = matplotlib.cm.get_cmap(cmap)
        norm = matplotlib.colors.Normalize(vmin=minvalue, vmax=maxvalue, clip=False)
        self.color_mapper = matplotlib.cm.ScalarMappable(norm=norm, cmap=colormap)

    def get_shapes(self):
        if self.shapes:
            return self.shapes
        raise NotImplementedError("Method 'get_shapes' or member attribute 'shapes' must be provided")

    def plot(self, tgt_srid):
        log.debug("Plottable::plot(fig, tgt_srid='{}')".format(tgt_srid))

        tgt_reference = SpatialReference(tgt_srid)

        patches = []
        shapes = self.get_shapes()
        for i, shape in enumerate(shapes):
            patches += shape.plot(target_reference=tgt_reference, mapper=self.color_mapper)
        return patches

    def savefig(self, tgt_srid, title=None, dpi=300):
        log.debug("Plottable::savefig(tgt_srid='{}', title='{}', dpi={})".format(tgt_srid, title, dpi))
        fig, ax = plt.subplots()
        patches = self.plot(fig, tgt_srid)

        for p in patches:
            ax.add_patch(p)

        self.color_mapper.set_array([])
        fig.colorbar(self.color_mapper)
        plt.axis('equal')
        plt.axis('off')

        if title:
            fig.suptitle(title)

        figure = io.BytesIO()
        fig.savefig(figure, format='png', dpi=dpi)
        plt.close()
        return figure
