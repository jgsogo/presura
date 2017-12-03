# -*- coding: utf-8 -*-

from django.core.management.base import BaseCommand, CommandError
from datasets.utils.importers import ine
from datasets.models import Commandline


class Command(BaseCommand):
    help = 'Import dataset from INE resource (ini file)'

    def add_arguments(self, parser):
        parser.add_argument('filenames', nargs='+', type=str)

    def handle(self, *args, **options):
        filenames = options["filenames"]

        for filename in filenames:
            cmd = Commandline.objects.new()
            cmd.info = "import_ine {}".format(filename)
            cmd.save()
            ine.import_resource(filename, cmd)
