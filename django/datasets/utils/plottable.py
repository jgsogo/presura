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


def plot_polygon(ax, points, fill, color, alpha, zorder=1):
    poly = Polygon(points, closed=True, fill=fill, color=color, alpha=alpha, zorder=zorder)
    ax.add_patch(poly)


class Shape:
    @staticmethod
    def builder(**defaults):
        def creator(**kwargs):
            z = defaults.copy()
            z.update(**kwargs)
            return Shape(**z)
        return creator

    def __init__(self, srid, shape, **kwargs):
        self.spatial_ref = SpatialReference(srid)
        self.shape = shape
        self.value = kwargs.get('value', np.random.random())
        self.alpha = kwargs.get('alpha', 1.)
        self.fill = kwargs.get('fill', False)
        self.zorder = kwargs.get('zorder', 1)
        self.color = kwargs.get('color', None)
        self.lw = kwargs.get('lw', 0.1)

    def plot(self, target_reference, mapper):
        trans = CoordTransform(self.spatial_ref, target_reference)
        self.shape.transform(trans)
        color = self.color or mapper.to_rgba(self.value)
        for poly in self.shape:
            yield Polygon(poly.coords[0], closed=True, fill=self.fill,
                          color=color, alpha=self.alpha, zorder=self.zorder,
                          lw=self.lw)


class Plottable:

    def get_shapes(self):
        raise NotImplementedError("Method 'get_shapes' or member attribute 'shapes' must be provided")

    def get_max_min(self, values):
        vmax = max(values) if len(values) else 1.
        vmin = min(values) if len(values) else 0.
        return vmax, vmin

    @property
    def shapes(self):
        if not hasattr(self, '__shapes'):
            log.debug("Plottable::get_shapes()")
            shapes = list(self.get_shapes())
            setattr(self, '__shapes', shapes)
        return getattr(self, '__shapes')

    def get_colormap(self, cmap, force=False):
        if force or not hasattr(self, '__colormap'):
            colormap = matplotlib.cm.get_cmap(cmap)
            values = [shape.value for shape in self.shapes]
            vmax, vmin = self.get_max_min(values)
            log.debug("Plottable::get_colormap(cmap='{}', vmax='{}', vmin='{}')".format(cmap, vmax, vmin))
            norm = matplotlib.colors.Normalize(vmin=vmin, vmax=vmax, clip=False)
            color_mapper = matplotlib.cm.ScalarMappable(norm=norm, cmap=colormap)
            color_mapper.set_array([])
            setattr(self, '__colormap', color_mapper)
        return getattr(self, '__colormap')

    def get_patches(self, tgt_srid, cmap):
        log.debug("Plottable::get_patches(fig, tgt_srid='{}')".format(tgt_srid))
        tgt_reference = SpatialReference(tgt_srid)
        color_mapper = self.get_colormap(cmap=cmap)
        for shape in self.shapes:
            for patch in shape.plot(target_reference=tgt_reference, mapper=color_mapper):
                yield patch

    def plot(self, ax, tgt_srid, cmap):
        log.debug("Plottable::plot(ax. tgt_srid='{}')".format(tgt_srid))
        for p in self.get_patches(tgt_srid=tgt_srid, cmap=cmap):
            ax.add_patch(p)

    def savefig(self, tgt_srid, title=None, cmap='hsv', dpi=300, showcmap=True):
        log.debug("Plottable::savefig(tgt_srid='{}', title='{}', cmap='{}', dpi={})".format(tgt_srid, title, cmap, dpi))

        fig, ax = plt.subplots()
        self.plot(ax, tgt_srid, cmap)
        if showcmap:
            color_mapper = self.get_colormap(cmap=cmap)
            fig.colorbar(color_mapper)
        plt.axis('equal')
        plt.axis('off')

        if title:
            fig.suptitle(title)

        # Save to bytes and return
        figure = io.BytesIO()
        fig.savefig(figure, format='png', dpi=dpi)
        plt.close()
        return figure
