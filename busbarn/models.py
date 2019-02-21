# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

# Create your models here.

class Vehicle(models.Model):
    VEHICLE_CLASSES = (
        ('Long Bus', 'Long Bus'),
        ('Medium Bus', 'Medium Bus'),
        ('Short Bus', 'Short Bus'),
        ('Shuttle', 'Shuttle'),
        ('Trolly', 'Trolly'),
        ('Van' , 'Van'),
        ('Truck', 'Truck'),
        ('Car', 'Car'),
    )
    vin_number = models.CharField(max_length=17, unique=True, default=None)
    license_plate = models.CharField(max_length=10)
    vehicle_class = models.CharField(max_length=10, choices=VEHICLE_CLASSES)
    vehicle_name = models.CharField(max_length=30, default='default')
    remarks = models.TextField(blank=True)

    def __str__(self):
        return self.vehicle_name

class Mechanic(models.Model):
    name = models.CharField(max_length=30)
    phone = models.CharField(max_length=12)
    active = models.BooleanField(default=True)

    def __str__(self):
        return self.name
    
class Issue(models.Model):
    SEVERITY_OPTIONS = (
        ('Urgent', 'Urgent'),
        ('OOS', 'OOS'),
    )
    REASONS = (
        ('Driver Write-up', 'Driver Write-up'),
        ('PM Work', 'PM Work'),
        ('Other Scheduled', 'Other Scheduled'),
    )
    REPAIR_CODES = (
        ('Repaired or Tightened', 'Repaired or tightened'),
        ('Replaced', 'Replaced'),
        ('Checked, found OK', 'Checked, found OK'),
    )
    
    vehicle = models.ForeignKey(Vehicle, on_delete=models.CASCADE) # so... don't delete
    date_noted = models.DateTimeField('date noted')
    severity = models.CharField(max_length=12, choices=SEVERITY_OPTIONS)
    description = models.CharField(max_length=100)

    # mechanic = models.CharField(max_length=30, blank=True)
    mechanic = models.ForeignKey(
        Mechanic,
        blank=True, null=True, #Allows field to be blank in the form and database
        on_delete=models.PROTECT, #Preserves the record; prevents deleting mechanics with records
        limit_choices_to={'active': True} #Only shows active mechanics in the form
    ) 

    
    date_completed = models.DateTimeField('date completed', blank=True, null=True)
    remarks = models.TextField(blank=True)
    reason = models.CharField(max_length=21, choices=REASONS, default="Other scheduled")
    repair = models.CharField(max_length=21, choices=REPAIR_CODES, blank=True)

    def __str__(self):
        return self.description

    def println(self):
        line = self.vehicle.vehicle_name + " \t" + self.description + "\t"
        line = line + self.mechanic
        return line
