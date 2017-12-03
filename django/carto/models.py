
from django.contrib.gis.db import models
from datasets.models import DataSet

class Layer(models.Model):
    name = models.CharField(max_length=64)
