# -*- coding: utf-8 -*-

from django.core.management.base import BaseCommand, CommandError
from carto.models import Layer


class Command(BaseCommand):
    help = 'Plot layer'

    def add_arguments(self, parser):
        parser.add_argument('--filename', type=str, required=True)
        parser.add_argument('--layer-id', dest="layer_id", type=int, required=True)

    def handle(self, *args, **options):
        layer = Layer.objects.get(pk=options["layer_id"])
        layer.save_image(options["filename"])
