# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin

from .models import Vehicle
from .models import Issue

# Register your models here.
admin.site.register(Vehicle)
admin.site.register(Issue)
