# -*- coding: utf-8 -*-

import argparse
import textwrap

from django.core.management.base import BaseCommand, CommandError
from django.utils.text import slugify

from ine.models import Resource
from ._actions import Action


def get_resources_available():
    qs = {it.pk: it.name for it in Resource.objects.available()}
    return qs


class CommandAction:
    def __init__(self, resource):
        self.resource = resource

    def exec(self):
        raise NotImplementedError("Action not implemented")


class Command(BaseCommand):
    help = 'Handle resources from INE'

    def add_arguments(self, parser):
        parser.add_argument('actions', nargs='+', type=str, choices=Action.list())
        parser.add_argument('--resource_ids', nargs='+', type=int,
                            required=True,
                            help='List of resources ids to apply action to')
        parser.add_argument('--override', dest='override', action='store_true', default=False)

        parser.formatter_class=argparse.RawDescriptionHelpFormatter
        resources = ['{} - {}'.format(key, value) for key, value in get_resources_available().items()]
        parser.epilog = textwrap.dedent("""
            Available resources are:
            ------------------------
            {}
        """.format('\n'.join(resources)))

    def get_resource_list(self, **options):
        resource_ids = options['resource_ids']

        # Check that given resources exists before running any of them.
        for id in resource_ids:
            if not Resource.objects.available().filter(pk=id).exists():
                raise CommandError("Resource with id '{!r}' does not exists".format(id))

        return Resource.objects.available().filter(pk__in=resource_ids)

    def handle(self, *args, **options):
        if len(options['actions']) > 1:
            self.stdout.write("(actions will be run in a predefined order)")

        # Sort actions given the order in Action.actions
        act_ids = [act.id for act in Action.actions if act.id in options['actions']]

        for act_id in act_ids:
            self.stdout.write("\n=== Action: {} ===".format(act_id))
            action = Action(act_id, self.stdout, self.stderr, override=options['override'])

            total = len(options['resource_ids'])
            for i, resource in enumerate(self.get_resource_list(**options), 1):
                self.stdout.write("[{}/{}] {!s}".format(i, total, resource))
                action.run(resource)

