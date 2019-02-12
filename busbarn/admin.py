# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin

from .models import Vehicle, Issue, Mechanic


# Register your models here.
admin.site.register(Vehicle)
admin.site.register(Issue)
admin.site.register(Mechanic)
