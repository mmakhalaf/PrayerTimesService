from django.contrib.gis.db import models

GENDER_CHOICES = (
    ("men", "Men Only"),
    ("women", "Women Only"),
    ("both", "Men / Women"),
    ("unknown", "Unknown"));


# Create your models here.
class Mosque(models.Model):
    id = models.IntegerField(primary_key=True);
    name = models.CharField(max_length=100, blank=False);
    address = models.TextField(blank=False);
    postcode = models.CharField(max_length=10, blank=False);
    capacity = models.IntegerField(default=-1);
    gender = models.CharField(choices=GENDER_CHOICES, max_length=10, default="unknown");
    longitude = models.FloatField(null=True);
    latitude = models.FloatField(null=True);
    location = models.PointField(default=None, geography=True);

    objects = models.GeoManager();

    class Meta:
        ordering = ('id',);
        app_label = 'PrayerTimesAPI';
