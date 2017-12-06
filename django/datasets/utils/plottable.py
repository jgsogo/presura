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

    def __init__(self, srid, shape):
        self.spatial_ref = SpatialReference(srid)
        self.shape = shape

    def plot(self, target_reference, *args, **kwargs):
        raise NotImplementedError("Shape is abstract")


class ShapeLine(Shape):
    color = None
    lw = None

    def plot(self, target_reference, *args, **kwargs):
        trans = CoordTransform(self.spatial_ref, target_reference)
        self.shape.transform(trans)
        for poly in self.shape:
            yield Polygon(poly.coords[0], closed=True, fill=False)


class ShapePolygon(Shape):
    color = None

    def plot(self, target_reference, *args, **kwargs):
        trans = CoordTransform(self.spatial_ref, target_reference)
        self.shape.transform(trans)
        return [Polygon(poly.coords[0], closed=True, fill=True) for poly in self.shape]


class Plottable:
    shapes = None
    # colormap = 'hsv'

    def get_shapes(self):
        if self.shapes:
            return self.shapes
        raise NotImplementedError("Method 'get_shapes' or member attribute 'shapes' must be provided")

    def plot(self, fig, tgt_srid, lw=0.3):
        log.debug("Plottable::plot(fig, tgt_srid='{}')".format(tgt_srid))

        tgt_reference = SpatialReference(tgt_srid)

        patches = []
        shapes = self.get_shapes()
        # cmap = plt.cm.get_cmap(self.colormap, len(shapes))
        for i, shape in enumerate(shapes):
            # facecolor = cmap(i)
            patches += shape.plot(lw=lw, target_reference=tgt_reference)
        return patches

    def savefig(self, tgt_srid, title=None, dpi=300, lw=0.3):
        log.debug("Plottable::savefig(tgt_srid='{}', title='{}', dpi={}, lw={})".format(tgt_srid, title, dpi, lw))
        fig, ax = plt.subplots()
        patches = self.plot(fig, tgt_srid, lw=lw)

        for p in patches:
            ax.add_patch(p)
        """
        colors = 100 * np.random.rand(len(patches))
        p = PatchCollection(patches)  #, alpha=0.4)
        p.set_array(np.array(colors))
        ax.add_collection(p)
        fig.colorbar(p, ax=ax)
        """

        plt.axis('equal')
        plt.axis('off')

        if title:
            fig.suptitle(title)

        figure = io.BytesIO()
        fig.savefig(figure, format='png', dpi=dpi)
        plt.close()
        return figure
