# -*- coding: utf-8 -*-

import argparse
import textwrap
import shapefile

from django.core.management.base import BaseCommand, CommandError


class Command(BaseCommand):
    help = 'Parse SHP file'

    def add_arguments(self, parser):
        parser.add_argument('files', nargs='+', type=str)

    def handle(self, *args, **options):
        for file in options['files']:
            sf = shapefile.Reader(file)
            fields = [it[0] for it in sf.fields][1:]  # TODO: Remove deletion flag
            print(fields)
            print(len(fields))

            for item in sf.shapeRecords():
                print(item.record)
                print(len(item.record))
                print(item.shape.points)
                exit()
