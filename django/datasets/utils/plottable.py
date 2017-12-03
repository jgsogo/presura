# -*- coding: utf-8 -*-

import io
import logging
import matplotlib
matplotlib.use('Agg')
from django.contrib.gis.gdal import SpatialReference, CoordTransform
import matplotlib.pyplot as plt

log = logging.getLogger(__name__)


class Shape:
    srid = None
    shape = None
    color = None

    """
    def __init__(self, shape, srid):
        self.shape = shape
        self.spatial_reference = SpatialReference(srid)

    def transform(self, target_reference, clone=True):
        trans = CoordTransform(self.spatial_reference, target_reference)
        self.shape.transform(trans, clone=clone)
    """

    def plot(self, lw, target_reference, facecolor=None):
        spatial_ref = SpatialReference(self.srid)
        trans = CoordTransform(spatial_ref, target_reference)
        for poly in self.shape:
            poly.transform(trans)
            x = [it[0] for it in poly.coords[0]]
            y = [it[1] for it in poly.coords[0]]
            plt.plot(x, y, lw=lw, c=facecolor or self.color)


class Plottable:
    shapes = None
    colormap = 'hsv'

    def get_shapes(self):
        if self.shapes:
            return self.shapes
        raise NotImplementedError("Method 'get_shapes' or member attribute 'shapes' must be provided")

    def plot(self, fig, tgt_srid, lw=0.3):
        log.debug("Plottable::plot(fig, tgt_srid='{}')".format(tgt_srid))

        tgt_reference = SpatialReference(tgt_srid)

        shapes = self.get_shapes()
        # cmap = plt.cm.get_cmap(self.colormap, len(shapes))
        for i, shape in enumerate(shapes):
            # facecolor = cmap(i)
            shape.plot(lw=lw, target_reference=tgt_reference)

    def savefig(self, tgt_srid, title=None, dpi=300, lw=0.3):
        log.debug("Plottable::savefig(tgt_srid='{}', title='{}', dpi={}, lw={})".format(tgt_srid, title, dpi, lw))
        fig = plt.figure()
        plt.axis('equal')
        plt.axis('off')
        self.plot(fig, tgt_srid, lw=lw)
        if title:
            fig.suptitle(title)

        figure = io.BytesIO()
        fig.savefig(figure, format='png', dpi=dpi)
        plt.close()
        return figure

        """
        gcoord = SpatialReference(4326)  # WGS84
        mycoord = SpatialReference(23030)  # Proyección UTM ED50 Huso 30 N
        trans = CoordTransform(gcoord, mycoord)

        log.debug("Plot image for dataset '{}'".format(self.name))
        figure = io.BytesIO()
        fig = plt.figure()
        plt.axis('equal')
        plt.axis('off')
        for municipality in self.municipality_set.all():
            for poly in municipality.points:
                poly.transform(trans)
                x = [it[0] for it in poly.coords[0]]
                y = [it[1] for it in poly.coords[0]]
                plt.plot(x, y, lw=self.image_line)
        fig.suptitle(self.name)
        fig.savefig(figure, format='png', dpi=self.image_dpi)
        plt.close()

        self.image.delete()
        filename = "{}.png".format(self.name) if settings.DEBUG else str(uuid.uuid4())
        self.image.save(filename, ImageFile(figure))
        """
