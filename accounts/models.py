from __future__ import unicode_literals

from django.db import models


class PermissionTable(models.Model):
    privilege = models.CharField(default='Placeholder', max_length=30)
