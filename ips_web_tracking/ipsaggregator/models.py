from __future__ import unicode_literals

from django.db import models

# Create your models here.


class Shipment(models.Model):
    identifier = models.CharField(max_length=255, unique=True, db_index=True)
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)
    processed = models.BooleanField(default = False)
    info = models.CharField(max_length=4096, default='', blank=True, null=True)

    def __str__(self):
        return self.identifier


class ShipmentEvent(models.Model):
    shipment = models.ForeignKey(Shipment)
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)
    event_time = models.DateTimeField()
    country = models.CharField(max_length=1024)
    location = models.CharField(max_length=1024)
    event_type = models.CharField(max_length=1024)
    mail_category = models.CharField(max_length=1024)
    next_office = models.CharField(max_length=1024)
    extra_info_col1 = models.CharField(max_length=1024)
    extra_info_col2 = models.CharField(max_length=1024)

    def __str__(self):
        return str(self.id)