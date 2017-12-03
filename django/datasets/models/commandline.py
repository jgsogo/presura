# -*- coding: utf-8 -*-

import getpass
import socket
from django.db import models


class CommandlineManager(models.Manager):
    def new(self, commit=False):
        item = self.model()
        item.user = getpass.getuser()
        item.hostname = socket.gethostname()
        if commit:
            item.save()
        return item


class Commandline(models.Model):
    datetime = models.DateTimeField(auto_now_add=True)
    user = models.CharField(max_length=64)
    hostname = models.CharField(max_length=64)
    info = models.TextField(blank=True, null=True)

    objects = CommandlineManager()

    def __str__(self):
        return "{}@{}".format(self.user, self.hostname)
