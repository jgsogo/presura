
from django.contrib.gis.db import models


class ShapeItem(models.Model):
    area = models.FloatField()
    perimeter = models.FloatField()
    #bbox = models.PolygonField()
    points = models.PolygonField()

    class Meta:
        abstract = True


class Country(ShapeItem):
    name = models.CharField(max_length=40)


class CCAA(ShapeItem):
    name = models.CharField(max_length=60)
    country = models.ForeignKey(Country, on_delete=models.CASCADE)


class Province(ShapeItem):
    name = models.CharField(max_length=120)
    province = models.ForeignKey(CCAA, on_delete=models.CASCADE)


class Municipality(ShapeItem):
    name = models.CharField(max_length=255)
    province = models.ForeignKey(Province, on_delete=models.CASCADE, blank=True, null=True)
    ccaa = models.ForeignKey(CCAA, on_delete=models.CASCADE, blank=True, null=True)

