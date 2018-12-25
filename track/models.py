from django.db import models
from django.contrib.auth.models import User

class Toy(models.Model):
    toy_id = models.IntegerField(primary_key=True)
    create_time = models.DateTimeField(blank=True)
    name = models.CharField(max_length=128, blank=True, default=None)
    comments = models.TextField(blank=True, default=None)
    approved = models.CharField(max_length=1, default='Y')

class ToyLocation(models.Model):
    toy_location_id = models.AutoField(primary_key=True)
    toy = models.ForeignKey(Toy, on_delete=models.CASCADE, null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    link = models.TextField(blank=True, null=True)
    latitude = models.FloatField(blank=True, null=True)
    longitude = models.FloatField(blank=True, null=True)
    comments = models.TextField(blank=True, null=True)
    flickr_photo_id = models.BigIntegerField(blank=True, null=True)
    date_time = models.DateTimeField(blank=True, null=True)
    location = models.TextField(blank=True, null=True)
    approved = models.CharField(max_length=1, blank=True, null=True)

class ToyLocationLink(models.Model):
    toy_location_link_id = models.AutoField(primary_key=True)
    toy_location = models.ForeignKey(ToyLocation, models.DO_NOTHING, null=True)
    link = models.CharField(max_length=200, blank=True, null=True)

class ToyLocationPhoto(models.Model):
    toy_location_photo_id = models.AutoField(primary_key=True)
    toy_location = models.ForeignKey(ToyLocation, models.DO_NOTHING, null=True)
    flickr_photo_id = models.BigIntegerField(blank=True, null=True)
    flickr_thumbnail_url = models.TextField(blank=True, null=True)