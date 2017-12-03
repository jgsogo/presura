# -*- coding: utf-8 -*-

from django.core.management.base import BaseCommand, CommandError
from datasets.models import DataSet


class Command(BaseCommand):
    help = 'Generate images for all datasets'

    def add_arguments(self, parser):
        parser.add_argument('--all', dest='all', action='store_true', default=False)

    def handle(self, *args, **options):
        qs = DataSet.objects.all()
        if not options['all']:
            self.stdout.write("Work only on datasets without image")
            qs = qs.filter(image__isnull=True)

        n = qs.count()
        for idx, dataset in enumerate(qs, 1):
            self.stdout.write("[{}/{}] {}".format(idx, n, dataset))
            dataset.save_plot()
            dataset.save()
